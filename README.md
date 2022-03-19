# ecm2434-Group-Project

## Dependencies
### Required to Run
- django: Used for the webserver `pip3 install django`
- polymorphic: Used for improved django models `pip3 install django-polymorphic`
- qrcode: Used to generate QR codes: `pip3 install qrcode`
### Required for building wasm files
- cargo: Used to compile Rust for QR decoder `curl https://sh.rustup.rs -sSf | sh`
- wasm-pack: Used to build wasm and js for QR decoder `cargo install wasm-pack`


## QR code support
### Use precompiled artifacts
Currently precompiled wasm and js files are included in git, so it will work by default

### To build

`wasm-pack build --target web -d ./TheGame/QRC/static/QRC  ./TheGame/qr-wasm`

### To test

`wasm-pack test --firefox --chrome --headless ./TheGame/qr-wasm`

## Use
### Using DJango runserver

Change directory to `./TheGame` then run `python3 manage.py runserver`

### Using External Server

Not yet complete

Collect statics using `python3 manage.py collectstatic`