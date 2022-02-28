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

async fn load_qr(decoder: &mut quircs::Quirc, file: web_sys::File, index: u32, total: u32) {
    let img = match load_image(file).await {
        Ok(img) => img,
        Err(err) => {
            let err = format!("Encountered Error: {:?}", err);
            web_sys::window().unwrap().alert_with_message(&err).unwrap();
            return;
        }
    };

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
        web_sys::console::log_1(&wasm_bindgen::JsValue::from_str(&msg));
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
    web_sys::console::log_1(&wasm_bindgen::JsValue::from_str(&format!(
        "Parsed Image {}/{}",
        index + 1,
        total
    )));
}

#[wasm_bindgen]
pub async fn load_qr_list(files: web_sys::FileList) {
    let len = files.length();
    web_sys::console::log_1(&wasm_bindgen::JsValue::from_str(&format!(
        "Loading {} files",
        len
    )));

    let mut decoder = quircs::Quirc::default();

    for i in 0..len {
        if let Some(file) = files.get(i) {
            load_qr(&mut decoder, file, i, len).await;
        }
    }
    web_sys::window()
        .unwrap()
        .alert_with_message(&format!("Loaded {} files", len))
        .unwrap();
}
