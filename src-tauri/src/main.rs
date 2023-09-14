// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
#![no_main]
use enigo::{KeyboardControllable, MouseControllable};
use tauri::Manager;

static mut CLICKER: bool = false;

#[tauri::command]
fn type_string(string: String) {
    let mut enigo = enigo::Enigo::new();
    enigo.key_sequence_parse(&string);
}

#[tauri::command]
fn autoclicker(speed: u64) {
    unsafe {
        CLICKER = !CLICKER;
        if CLICKER {
            std::thread::spawn(move || {
                let mut enigo = enigo::Enigo::new();
                while CLICKER {
                    enigo.mouse_click(enigo::MouseButton::Left);
                    std::thread::sleep(std::time::Duration::from_millis(speed));
                }
            });
        }
    }
}
#[no_mangle]
pub extern "C" fn main() -> usize {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![type_string, autoclicker])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
    0
}
