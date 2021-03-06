# ecm2434-Group-Project

![SoE](/Documents/SoElogo4.png)

Scavengers of Exeter is a sci-fi based IRL exploraion game.

## Dependencies
### Required to Run
- django: Used for the webserver `pip3 install django`
- polymorphic: Used for improved django models `pip3 install django-polymorphic`
- qrcode: Used to generate QR codes: `pip3 install qrcode`
- pillow: Required for qrcode `pip3 install pillow`
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
Change directory to `./TheGame` for all of the below commands
### First run
Create database by running `python3 manage.py migrate`

Initialise defaults by running `python3 manage.py shell -c "import first_run"`

### Using DJango runserver

Run `python3 manage.py runserver`

### Using External Server

Not yet complete

Collect statics using `python3 manage.py collectstatic`
