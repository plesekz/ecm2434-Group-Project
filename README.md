# ecm2434-Group-Project

## Dependencies
- django: `pip3 install django`
- polymorphic: `pip3 install django-polymorphic`
- cargo: `curl https://sh.rustup.rs -sSf | sh`
- wasm-pack: `cargo install wasm-pack`


## QR code support
To build

`wasm-pack build --target web -d ./TheGame/QRC/static/QRC  ./TheGame/qr-wasm`

To test

`wasm-pack test --firefox --chrome --headless ./TheGame/qr-wasm`

## Use

To run change directory to `./TheGame` then run `python3 manage.py runserver`
