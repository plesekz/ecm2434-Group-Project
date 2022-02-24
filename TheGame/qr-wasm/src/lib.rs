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

async fn load_qr(file: web_sys::File, index: u32, total: u32) {
    let img = match load_image(file).await {
        Ok(img) => img,
        Err(err) => {
            let err = format!("Encountered Error: {:?}", err);
            web_sys::window().unwrap().alert_with_message(&err).unwrap();
            return;
        }
    };

    let mut decoder = quircs::Quirc::default();
    let codes = decoder.identify(img.width() as usize, img.height() as usize, &img);

    for code in codes {
        if let Ok(code) = code {
            if let Ok(decoded) = code.decode() {
                if let Ok(data) = std::str::from_utf8(&decoded.payload) {
                    let msg = format!("Data {}", data);
                    web_sys::console::log_1(&wasm_bindgen::JsValue::from_str(&msg));
                    web_sys::window().unwrap().alert_with_message(&msg).unwrap();
                }
            }
        }
    }
    let msg = format!("Parsed Image {}/{}", index, total);
    web_sys::console::log_1(&wasm_bindgen::JsValue::from_str(&msg));
    return;
    web_sys::window().unwrap().alert_with_message(&msg).unwrap();

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

#[wasm_bindgen]
pub async fn load_qr_list(files: web_sys::FileList) {
    let len = files.length();
    web_sys::console::log_1(&wasm_bindgen::JsValue::from_str(&format!("Loading {} files", len)));
    for i in 0..len {
        if let Some(file) = files.get(i) {
            load_qr(file, i, len).await;
        }
    }
}
