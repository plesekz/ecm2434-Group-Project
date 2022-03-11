use std::cell::Cell;
use std::rc::Rc;
use wasm_bindgen::closure::Closure;
use wasm_bindgen::prelude::*;
use wasm_bindgen::JsCast;

/** Setup event hooks*/
#[cfg(not(test))]
#[wasm_bindgen(start)]
pub fn main() -> Result<(), JsValue> {
    std::panic::set_hook(Box::new(console_error_panic_hook::hook)); /* Sets panics to display to console for debugging*/
    wasm_logger::init(wasm_logger::Config::default()); /* Sets logger to display to console */

    let mut manager = QRManager::new();
    manager.set_status_ids("runningStatus", "taskCount", "ScannedCount");
    manager.call_callback();

    /* Set all elements with class loadQR to call manager.load_file_list */
    let elems = manager.document.get_elements_by_class_name("loadQR");
    for elem in (0..elems.length())
        .flat_map(|i| elems.item(i))
        .flat_map(|elem| elem.dyn_into::<web_sys::HtmlInputElement>())
    {
        let manager = manager.clone();
        let elem_clone = elem.clone();
        let closure: Closure<dyn Fn()> = Closure::wrap(Box::new(move || {
            if let Some(files) = elem_clone.files() {
                manager.load_file_list(files);
            }
        }) as Box<dyn Fn()>);
        let function: &js_sys::Function = closure.as_ref().unchecked_ref();
        elem.set_onchange(Some(function));

        closure.forget();
    }
    /* Set elements with class cancelQR to call manager.stop) */
    let elems = manager.document.get_elements_by_class_name("cancelQR");
    let closure: Closure<dyn Fn()> =
        Closure::wrap(Box::new(move || manager.stop()) as Box<dyn Fn()>);
    let function: &js_sys::Function = closure.as_ref().unchecked_ref();
    for elem in (0..elems.length())
        .flat_map(|i| elems.item(i))
        .flat_map(|elem| elem.dyn_into::<web_sys::HtmlInputElement>())
    {
        elem.set_onclick(Some(function));
    }
    closure.forget();

    Ok(())
}

/**
Function to be called with status whenever it changes
*/
pub struct Callback(Box<dyn Fn(Status)>);

impl Default for Callback {
    fn default() -> Self {
        Self(Box::new(|_| {}))
    }
}

#[derive(Debug)]
enum QrError {
    InvalidQrID,
    UnknownQrID,
    UnknownServerError,
    JsError(JsValue),
}

impl std::fmt::Display for QrError {
    fn fmt(&self, fmt: &mut std::fmt::Formatter<'_>) -> Result<(), std::fmt::Error> {
        write!(fmt, "{:?}", self)
    }
}

impl std::error::Error for QrError {}

impl std::convert::From<JsValue> for QrError {
    fn from(val: JsValue) -> Self {
        Self::JsError(val)
    }
}

/**
Current image parsing progress to be displayed
*/
#[derive(Debug)]
pub struct Status {
    /** Whether there are currently any in progress tasks*/
    pub running: bool,
    /** Number of files scanned*/
    pub scanned: usize,
    /** Number of files left to scan*/
    pub tasks: usize,
}

/** Contains currently processed files and status*/
#[derive(Clone)]
pub struct QRManager {
    files: Rc<Cell<Vec<web_sys::File>>>,
    scan_count: Rc<Cell<usize>>,
    running: Rc<Cell<bool>>,
    age: Rc<Cell<usize>>,
    callback: Rc<Cell<Callback>>,
    window: web_sys::Window,
    document: web_sys::Document,
}

impl Default for QRManager {
    fn default() -> Self {
        Self::new()
    }
}

impl QRManager {
    /** Creates new instance*/
    pub fn new() -> Self {
        let window = web_sys::window().expect("no global `window` exists");
        let document = window.document().expect("should have a document on window");
        Self {
            files: Default::default(),
            scan_count: Default::default(),
            running: Default::default(),
            age: Default::default(),
            callback: Default::default(),
            window,
            document,
        }
    }
    /** Sets callback to display status by updating elements with specified ids*/
    pub fn set_status_ids(
        &mut self,
        running_id: &str,
        tasks_left_id: &str,
        scanned_count_id: &str,
    ) {
        let running_elem = self.document.get_element_by_id(&running_id);
        let tasks_left_elem = self.document.get_element_by_id(&tasks_left_id);
        let scanned_elem = self.document.get_element_by_id(&scanned_count_id);
        self.set_callback(Callback(Box::new(move |status| {
            if let Some(elem) = &running_elem {
                let new = status.running.to_string();
                elem.set_inner_html(&new);
            }
            if let Some(elem) = &tasks_left_elem {
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
            if let Some(elem) = &scanned_elem {
                let new = status.scanned.to_string();
                elem.set_inner_html(&new);
            }
        })));
    }
    /** Called whenever status changes*/
    pub fn call_callback(&self) {
        let status = self.get_status();
        let callback = self.callback.take();
        callback.0(status);
        self.callback.set(callback);
    }
    /** Adds files to list of pending files, and spawns new progess task */
    pub fn load_file_list(&self, new_files: web_sys::FileList) {
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
    /** Generates current status with active files count, parsed count, and running status*/
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
    /** Stops any image parsing tasks, and empties file list*/
    pub fn stop(&self) {
        let _ = self.files.take();

        log::info!("Stopping")
    }
    /** Changes which function is called when status changes*/
    pub fn set_callback(&mut self, callback: Callback) {
        self.callback.set(callback);
    }
    /**
    Task that parses images in list, stops whenever a newer task is spawned
    */
    async fn process(self) {
        log::info!("New task");
        let age = self.age.get();
        let mut decoder = quircs::Quirc::default();

        while age == self.age.get() {
            /* Check if any new task has been spawned */
            self.call_callback();
            let mut files = self.files.take();
            let file = files.pop();
            self.files.set(files);
            self.running.set(true);
            let file = if let Some(file) = file { file } else { break };
            match load_qr(&mut decoder, file).await {
                Ok(codes) => {
                    for code in codes {
                        let code: Result<usize, _> = code
                            .and_then(|code| Ok(code.parse().map_err(|_| QrError::InvalidQrID)?));
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
                                let msg = format!("Error: {:?}", err);
                                log::error!("{}", &msg);
                                self.window.alert_with_message(&msg).unwrap();
                            }
                        }
                    }
                }
                Err(err) => {
                    log::error!("Error: {:?}", err)
                }
            }

            self.scan_count.set(self.scan_count.get() + 1);

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
    /** Sends QR data to backend and returns resources */
    async fn retrieve_res(&self, data: &usize) -> Result<Vec<(String, usize)>, QrError> {
        let promise = self
            .window
            .fetch_with_str(&format!("/qr/retrieveRes?data={}", data));
        let result = wasm_bindgen_futures::JsFuture::from(promise).await;
        let result = result?;
        let response: web_sys::Response = result.into();
        log::info!("{}", response.ok());
        log::info!("{}", response.status());
        log::info!("{}", response.status_text());
        if !response.ok() {
            return Err(match response.status() {
                501 => QrError::UnknownQrID,
                _ => QrError::UnknownServerError,
            });
        }
        let json_promise = response.json()?;
        let result = wasm_bindgen_futures::JsFuture::from(json_promise).await?;
        let object: js_sys::Object = result.dyn_into()?;
        let values: Vec<_> = js_sys::Object::values(&object)
            .iter()
            .flat_map(|val| val.dyn_into::<js_sys::Array>())
            .flat_map(|val| {
                let mut iter = val.iter();
                let name: String = iter.next()?.as_string()?;
                let amount = iter.next()?.as_f64()? as usize;
                Some((name, amount))
            })
            .collect();
        Ok(values)
    }
    /** Creates new task*/
    fn spawn_task(&self) {
        self.age.set(self.age.get().wrapping_add(1));
        let manager = self.clone();
        wasm_bindgen_futures::spawn_local(manager.process());
    }
}

/**
Use html <img> tag to parse image, and convert to canvas to extract pixels

Faster as it uses the browsers native image parser, but not always supported
*/
async fn browser_load_image(file: web_sys::File) -> Result<image::GrayImage, JsValue> {
    let blob = web_sys::Blob::from(file);

    let url: String = web_sys::Url::create_object_url_with_blob(&blob)?;
    let img = web_sys::HtmlImageElement::new()?;
    img.set_src(&url);
    wasm_bindgen_futures::JsFuture::from(img.decode()).await?; /* Wait for image to finish parsing before continuing*/
    log::info!("Decoded image");

    let width = img.natural_width();
    let height = img.natural_height();
    log::info!("Size: {:?}", (width, height));
    let canvas = web_sys::window()
        .unwrap()
        .document()
        .unwrap()
        .create_element("canvas")?;
    let canvas = canvas.dyn_into::<web_sys::HtmlCanvasElement>()?;
    canvas.set_width(width);
    canvas.set_height(height);
    let ctx = canvas
        .get_context("2d")?
        .ok_or("Failed to create context")?;
    let ctx = ctx.dyn_into::<web_sys::CanvasRenderingContext2d>()?;

    let window = web_sys::window().unwrap();

    let bitmap = wasm_bindgen_futures::JsFuture::from(
        window.create_image_bitmap_with_html_image_element(&img)?,
    )
    .await?;
    let bitmap = bitmap.dyn_into::<web_sys::ImageBitmap>()?;
    log::info!("bitmap: {:?}", bitmap);

    ctx.draw_image_with_image_bitmap(&bitmap, 0.0, 0.0)?;

    log::info!("Created Canvas: {:?}", ctx);

    let data = ctx
        .get_image_data(0.0, 0.0, width as f64, height as f64)?
        .data()
        .0;

    let img = image::RgbaImage::from_raw(width, height, data);
    let img = img.ok_or("Invalid image")?;

    let img: image::DynamicImage = image::DynamicImage::from(img);
    return Ok(img.into_luma8());
}

/**
Use rust image library to parse image

Slower as wasm is slower than native, but always supported
*/
async fn lib_load_image(file: web_sys::File) -> Result<image::GrayImage, JsValue> {
    let buffer = wasm_bindgen_futures::JsFuture::from(file.array_buffer())
        .await
        .map_err(|e| format!("{:?}", e))?;
    let buffer: js_sys::Uint8Array = js_sys::Uint8Array::new(&buffer);

    let buffer: Vec<u8> = buffer.to_vec();
    /*If extension says image type skip guessing the type, creates slight performance improvement*/
    let img = if let Some(format) = match file.name() {
        name if name.ends_with(".jpeg") => Some(image::ImageFormat::Jpeg),
        name if name.ends_with(".jpg") => Some(image::ImageFormat::Jpeg),
        name if name.ends_with(".png") => Some(image::ImageFormat::Png),
        _ => None,
    } {
        image::load_from_memory_with_format(&buffer, format)
    } else {
        image::load_from_memory(&buffer)
    };
    let img = img.map_err(|e| format!("Error: {:?}", e))?;

    Ok(img.into_luma8())
}

/**
Loads the image data from javascript file input

If browser supports extracting data from canvas uses that, otherwise uses an image parsing library
*/
async fn load_image(file: web_sys::File) -> Result<image::GrayImage, JsValue> {
    log::info!("Loading image: {}", file.name());

    let canvas = web_sys::window()
        .unwrap()
        .document()
        .unwrap()
        .create_element("canvas")?;
    let canvas = canvas.dyn_into::<web_sys::HtmlCanvasElement>()?;
    canvas.set_width(100);
    canvas.set_height(100);

    let ctx = canvas
        .get_context("2d")?
        .ok_or("Failed to create context")?;
    let ctx = ctx.dyn_into::<web_sys::CanvasRenderingContext2d>()?;
    /*Creates an empty canvas and checks if all pixels are zero*/
    if ctx
        .get_image_data(0.0, 0.0, 10.0, 10.0)?
        .data()
        .0
        .iter()
        .all(|pixel| *pixel == 0)
    {
        /*Canvas is working correctly so use faster native technique*/
        log::info!("Trusty");
        browser_load_image(file).await
    } else {
        /*Non zero pixels means that the browser has some form of anti-canvas fingerprinting defense which means can't use canvas to parse image*/
        log::info!("Unreliable");
        lib_load_image(file).await
    }

    /*if img.height() > 1000 {
        img = img.thumbnail(1000, 1000);
    }*/

    //Ok(img)
}

/** Extracts all QR codes from javascript file input

Parses image and then uses quircs to identify QR codes
*/
async fn load_qr(
    decoder: &mut quircs::Quirc,
    file: web_sys::File,
) -> Result<
    impl std::iter::Iterator<Item = Result<String, Box<dyn std::error::Error>>> + '_,
    Box<dyn std::error::Error>,
> {
    let img = load_image(file).await.map_err(|e| format!("{:?}", e))?;
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
}

#[cfg(test)]
mod tests {

    wasm_bindgen_test_configure!(run_in_browser);
    use crate::*;
    use wasm_bindgen_test::*;
    #[wasm_bindgen_test]
    pub async fn load_qr_test() {
        let data: &[(&[u8], &str, &[_])] = &[
            (
                &include_bytes!("../test_images/IMG_20220303_131339.jpg")[..],
                "../test_images/IMG_20220303_131339.jpg",
                &[Ok("1041758308".to_string())],
            ),
            (
                &include_bytes!("../test_images/IMG_20220311_173540.jpg")[..],
                "../test_images/IMG_20220311_173540.jpg",
                &[Ok("3653067026".to_string())],
            ),
        ];

        for (image_data, name, desired) in data {
            let array = js_sys::Array::new();
            array.set(0, js_sys::Uint8Array::from(*image_data).dyn_into().unwrap());
            let file = web_sys::File::new_with_blob_sequence(&array, name).unwrap();
            let mut decoder = quircs::Quirc::default();
            let vals: Vec<_> = load_qr(&mut decoder, file)
                .await
                .unwrap()
                .map(|val| val.map_err(|e| e.to_string()))
                .collect();
            assert_eq!(&vals, desired);
        }
    }
}
