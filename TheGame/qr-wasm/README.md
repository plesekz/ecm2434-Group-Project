Dependencies:
- cargo
- wasm-pack (`cargo install wasm-pack`)

To build

`wasm-pack build --target web -d ./TheGame/QRC/static/QRC  ./TheGame/qr-wasm`

To test

`wasm-pack test --firefox --chrome --headless ./TheGame/qr-wasm`
