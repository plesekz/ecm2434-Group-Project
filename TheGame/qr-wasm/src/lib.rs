use std::cell::Cell;
use std::rc::Rc;
use wasm_bindgen::prelude::*;
// Called when the wasm module is instantiated
#[wasm_bindgen(start)]
pub fn main() -> Result<(), JsValue> {
    std::panic::set_hook(Box::new(console_error_panic_hook::hook));
    wasm_logger::init(wasm_logger::Config::default());
    Ok(())
}

pub struct Callback(Box<dyn Fn(Status)>);

impl Default for Callback {
    fn default() -> Self {
        Self(Box::new(|_| {}))
    }
}

#[derive(Clone)]
#[wasm_bindgen]
pub struct QRManager {
    files: Rc<Cell<Vec<web_sys::File>>>,
    scan_count: Rc<Cell<usize>>,
    running: Rc<Cell<bool>>,
    age: Rc<Cell<usize>>,
    callback: Rc<Cell<Callback>>,
    window: web_sys::Window,
    document: web_sys::Document,
}

#[derive(Debug)]
#[wasm_bindgen]
pub struct Status {
    pub running: bool,
    pub scanned: usize,
    pub tasks: usize,
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
            self.call_callback();
            let mut files = self.files.take();
            let file = files.pop();
            self.files.set(files);
            self.running.set(true);
            if let Some(file) = file {
                match load_qr(&mut decoder, file).await {
                    Ok(codes) => {
                        for code in codes {
                            match code {
                                Ok(code) => {
                                    let result = self.retrieve_res(&code).await;
                                    log::info!("result: {:?}", result);
                                    let msg = match result {
                                        Ok(res) => format!("Result: {:?}", res),
                                        Err(err) => format!("Error: {:?}", err),
                                    };
                                    self.window.alert_with_message(&msg).unwrap();
                                }
                                Err(err) => {
                                    log::error!("Error: {:?}", err);
                                }
                            }
                        }
                    }
                    Err(err) => {
                        log::error!("Error: {:?}", err)
                    }
                }

                self.scan_count.set(self.scan_count.get() + 1);
            } else {
                break;
            }
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

    async fn retrieve_res(&self, data: &str) -> Result<String, String> {
        let promise = self
            .window
            .fetch_with_str(&format!("/retrieveRes?data={:?}", data));
        let result = wasm_bindgen_futures::JsFuture::from(promise).await;
        let result = result.map_err(|err| format!("Error: {:?}", err))?;
        let response: web_sys::Response = result.into();
        log::info!("{}", response.ok());
        log::info!("{}", response.status());
        log::info!("{}", response.status_text());
        let text_promise = response.text().map_err(|err| format!("Error: {:?}", err))?;
        let result = wasm_bindgen_futures::JsFuture::from(text_promise).await;
        let result = result.map_err(|err| format!("Error: {:?}", err))?;
        let text: String = result
            .as_string()
            .ok_or_else(|| format!("Failed to convert to string: {:?}", result))?;
        Ok(format!("{:?}", text))
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
        let window = web_sys::window().expect("no global `window` exists");
        let document = window.document().expect("should have a document on window");
        Self {
            files: Default::default(),
            scan_count: Default::default(),
            running: Default::default(),
            age: Default::default(),
            callback: Default::default(),
            window: window,
            document: document,
        }
    }

    #[wasm_bindgen]
    pub fn set_status_ids(
        &mut self,
        running_id: String,
        tasks_left_id: String,
        scanned_count_id: String,
    ) {
        let manager = self.clone();
        self.set_callback(Callback(Box::new(move |status| {
            if let Some(elem) = manager.document.get_element_by_id(&running_id) {
                let new = status.running.to_string();
                elem.set_inner_html(&new);
            }
            if let Some(elem) = manager.document.get_element_by_id(&tasks_left_id) {
                let new = status.tasks.to_string();
                let width = status.tasks as f32 / (status.scanned + status.tasks).max(1) as f32;
                let width = 100.0 - width * 100.0;
                if let Err(err) =
                    elem.set_attribute("style", &format!("width: {}%", width as usize))
                {
                    log::error!("{:?}", err);
                }
                elem.set_inner_html(&new);
            }
            if let Some(elem) = manager.document.get_element_by_id(&scanned_count_id) {
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
            if files.is_empty() {
                self.scan_count.set(0);
            }
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
            scanned: self.scan_count.get(),
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

async fn load_qr(
    decoder: &mut quircs::Quirc,
    file: web_sys::File,
) -> Result<
    impl std::iter::Iterator<Item = Result<String, Box<dyn std::error::Error>>> + '_,
    Box<dyn std::error::Error>,
> {
    let img = load_image(file).await?;
    log::info!("Loaded image");

    let codes = decoder.identify(img.width() as usize, img.height() as usize, &img);

    Ok(codes.map(|code| {
        let code = code?;
        let decoded = code.decode()?;
        let payload = decoded.payload;
        let msg = std::str::from_utf8(&payload)?;
        log::info!("{}", &msg);
        Ok(msg.to_owned())
    }))

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
