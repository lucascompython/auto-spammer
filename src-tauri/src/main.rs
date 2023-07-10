// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
#![no_main]

use enigo::KeyboardControllable;

#[tauri::command]
fn type_string(string: String) {
    let mut enigo = enigo::Enigo::new();
    enigo.key_sequence_parse(&string);
}

#[no_mangle]
pub extern "C" fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![type_string])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
