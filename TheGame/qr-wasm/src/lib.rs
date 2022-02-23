use wasm_bindgen::prelude::*;

// Called when the wasm module is instantiated
#[wasm_bindgen(start)]
pub fn main() -> Result<(), JsValue> {
    std::panic::set_hook(Box::new(console_error_panic_hook::hook));

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

#[wasm_bindgen]
pub fn add(a: u32, b: u32) -> u32 {
    a + b
}

async fn load_image(file: web_sys::File) -> Result<image::GrayImage, Box<dyn std::error::Error>> {
    let buffer = wasm_bindgen_futures::JsFuture::from(file.array_buffer())
        .await
        .map_err(|e| format!("{:?}", e))?;
    let buffer = js_sys::Uint8Array::new(&buffer);
    let buffer: Vec<u8> = buffer.to_vec();
    let img = image::io::Reader::new(std::io::Cursor::new(buffer))
        .with_guessed_format()
        .expect("Cursor io never fails");
    let img = img.decode()?;
    //let img = image::load_from_memory(&buffer)?;
    //Ok(img)
    Ok(img.into_luma8())
}

#[wasm_bindgen]
pub async fn load_qr(file: web_sys::File) {
    let img = match load_image(file).await {
        Ok(img) => img,
        Err(err) => {
            let err = format!("Encountered Error: {:?}", err);

            web_sys::console::log_1(&wasm_bindgen::JsValue::from_str(&err));
            web_sys::window().unwrap().alert_with_message(&err).unwrap();
            return;
        }
    };

    eprintln!("Hey");

    let mut decoder = quircs::Quirc::default();
    let codes = decoder.identify(img.width() as usize, img.height() as usize, &img);

    for code in codes {
        let code = code.expect("failed to extract qr code");
        let decoded = code.decode().expect("failed to decode qr code");
        let data = std::str::from_utf8(&decoded.payload).unwrap();

        web_sys::console::log_1(&wasm_bindgen::JsValue::from_str(&format!("Data {}", data)));
        web_sys::window()
            .unwrap()
            .alert_with_message(&format!("Data: {:?}", data))
            .unwrap();
    }
    
    
    web_sys::console::log_1(&wasm_bindgen::JsValue::from_str("Parsed Image"));

    web_sys::window()
        .unwrap()
        .alert_with_message("Parsed Image")
        .unwrap();

    /* let decoder = bardecoder::default_decoder();




    let results = decoder.decode(&img);
    for result in results {
        if let Ok(data) = result{
            web_sys::console::log_1(&wasm_bindgen::JsValue::from_str(&format!("Data {}", data)));
            web_sys::window().unwrap().alert_with_message(&format!("Data: {:?}", data)).unwrap();
        }
    }*/
    /*

    let mut img = rqrr::PreparedImage::prepare(img);
    let grids = img.detect_grids();

    web_sys::console::log_1(&wasm_bindgen::JsValue::from_str(&format!(
        "Found {} grids",
        grids.len()
    )));
    for grid in grids.iter() {
        if let Ok((_metadata, data)) = grid.decode() {
            web_sys::console::log_1(&wasm_bindgen::JsValue::from_str(&format!("Data {}", data)));

            web_sys::window().unwrap().alert_with_message(&format!("Data: {:?}", data)).unwrap();
        }
    }*/
}
