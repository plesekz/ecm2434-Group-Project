use std::cell::Cell;
use std::rc::Rc;
use wasm_bindgen::prelude::*;

// Called when the wasm module is instantiated
#[wasm_bindgen(start)]
pub fn main() -> Result<(), JsValue> {
    std::panic::set_hook(Box::new(console_error_panic_hook::hook));
    wasm_logger::init(wasm_logger::Config::default());

    // Use `web_sys`'s global `window` function to get a handle on the global
    // window object.
    let window = web_sys::window().expect("no global `window` exists");
    let document = window.document().expect("should have a document on window");
    let body = document.body().expect("document should have a body");

    // Manufacture the element we're gonna append
    let val = document.create_element("p")?;
    val.set_inner_html("Hello from Rust!");

    web_sys::console::log_1(&wasm_bindgen::JsValue::from_str(
        &document.document_uri().unwrap(),
    ));

    body.append_child(&val)?;

    Ok(())
}

pub struct Callback(Box<dyn Fn(Status)>);

impl Default for Callback {
    fn default() -> Self {
        Self(Box::new(|_| {}))
    }
}

#[derive(Default, Clone)]
#[wasm_bindgen]
pub struct QRManager {
    files: Rc<Cell<Vec<web_sys::File>>>,
    running: Rc<Cell<bool>>,
    age: Rc<Cell<usize>>,
    callback: Rc<Cell<Callback>>,
}

#[derive(Debug)]
#[wasm_bindgen]
pub struct Status {
    running: bool,
    scanned: usize,
    tasks: usize,
}

impl QRManager {
    pub fn set_callback(&mut self, callback: Callback) {
        self.callback.set(callback);
    }

    async fn process(self) {
        log::info!("New task");
        let age = self.age.get();
        let mut decoder = quircs::Quirc::default();
        while age == self.age.get() {
            let mut files = self.files.take();
            let file = files.pop();
            self.files.set(files);
            self.running.set(true);
            if let Some(file) = file {
                load_qr(&mut decoder, file).await;
            } else {
                break;
            }
            self.call_callback();
            log::info!("Status: {:?}", self.get_status());
        }
        if age == self.age.get() {
            log::info!("Finished files");
            self.running.set(false);
        } else {
            log::info!("Newer loader");
        }
        self.call_callback();
    }
    fn spawn_task(&mut self) {
        self.age.set(self.age.get().wrapping_add(1));
        let manager = self.clone();
        wasm_bindgen_futures::spawn_local(manager.process());
    }
}

#[wasm_bindgen]
impl QRManager {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        Self::default()
    }

    #[wasm_bindgen]
    pub fn set_status_ids(
        &mut self,
        running_id: String,
        tasks_left_id: String,
        scanned_count_id: String,
    ) {
        let window = web_sys::window().expect("no global `window` exists");
        let document = window.document().expect("should have a document on window");
        self.set_callback(Callback(Box::new(move |status| {
            if let Some(elem) = document.get_element_by_id(&running_id) {
                let new = status.running.to_string();
                elem.set_inner_html(&new);
            }
            if let Some(elem) = document.get_element_by_id(&tasks_left_id) {
                let new = status.tasks.to_string();
                elem.set_inner_html(&new);
            }
            if let Some(elem) = document.get_element_by_id(&scanned_count_id) {
                let new = status.scanned.to_string();
                elem.set_inner_html(&new);
            }
        })));
    }

    #[wasm_bindgen]
    pub fn call_callback(&self) {
        let status = self.get_status();
        let callback = self.callback.take();
        callback.0(status);
        self.callback.set(callback);
    }

    #[wasm_bindgen]
    pub fn load_file_list(&mut self, new_files: web_sys::FileList) {
        {
            let mut files = self.files.take();
            for i in 0..new_files.length() {
                if let Some(file) = new_files.get(i) {
                    files.push(file);
                }
            }
            self.files.set(files);
        }
        self.spawn_task();
        log::info!("{:?}", self.get_status());
    }

    #[wasm_bindgen]
    pub fn get_status(&self) -> Status {
        let files = self.files.take();
        let tasks = files.len();
        self.files.set(files);
        Status {
            running: self.running.get(),
            scanned: 0,
            tasks,
        }
    }

    #[wasm_bindgen]
    pub fn stop(&mut self) {
        self.running.set(false);
        let _ = self.files.take();

        log::info!("Stopping")
    }
}

async fn load_image(file: web_sys::File) -> Result<image::GrayImage, Box<dyn std::error::Error>> {
    let buffer = wasm_bindgen_futures::JsFuture::from(file.array_buffer())
        .await
        .map_err(|e| format!("{:?}", e))?;
    let buffer: js_sys::Uint8Array = js_sys::Uint8Array::new(&buffer);
    let buffer: Vec<u8> = buffer.to_vec();
    let mut img = image::load_from_memory(&buffer)?;
    if img.height() > 1000 {
        img = img.thumbnail(1000, 1000);
    }

    //Ok(img)
    Ok(img.into_luma8())
}

async fn load_qr(decoder: &mut quircs::Quirc, file: web_sys::File) {
    let img = match load_image(file).await {
        Ok(img) => img,
        Err(err) => {
            let err = format!("Encountered Error: {:?}", err);
            web_sys::window().unwrap().alert_with_message(&err).unwrap();
            return;
        }
    };
    log::info!("Loaded image");

    let codes = decoder.identify(img.width() as usize, img.height() as usize, &img);

    for code in codes {
        let code: Result<quircs::Code, String> = code.map_err(|err| err.to_string());
        let data: Result<quircs::Data, String> =
            code.and_then(|code| code.decode().map_err(|err| err.to_string()));
        let decoded: Result<Vec<u8>, String> = data.map(|decoded| decoded.payload);
        let msg: String = decoded
            .and_then(|decoded| {
                std::str::from_utf8(&decoded)
                    .map_err(|err| err.to_string())
                    .map(|data| format!("Data {}", data))
            })
            .unwrap_or_else(|err| format!("Error {}", err));
        log::info!("{}", &msg);
        web_sys::window().unwrap().alert_with_message(&msg).unwrap();
    }

    /* let decoder = bardecoder::default_decoder();




    let results = decoder.decode(&img);
    for result in results {
        if let Ok(data) = result{
            web_sys::console::log_1(&wasm_bindgen::JsValue::from_str(&format!("Data {}", data)));
            web_sys::window().unwrap().alert_with_message(&format!("Data: {:?}", data)).unwrap();
        }
    }*/

    /*let mut img = rqrr::PreparedImage::prepare_from_greyscale(
        img.width() as usize,
        img.height() as usize,
        |x, y| img.get_pixel(x as u32, y as u32).0[0],
    );
    let grids = img.detect_grids();

    web_sys::console::log_1(&wasm_bindgen::JsValue::from_str(&format!(
        "Found {} grids",
        grids.len()
    )));
    for grid in grids.iter() {
        let msg = match grid.decode() {
            Ok((_metadata, data)) => format!("Data {}", data),
            Err(err) => format!("Error {}", err),
        };

        web_sys::console::log_1(&wasm_bindgen::JsValue::from_str(&msg));
        web_sys::window().unwrap().alert_with_message(&msg).unwrap();
    }*/
}
