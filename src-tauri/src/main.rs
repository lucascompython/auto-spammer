// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
#![no_main]

use enigo::{Keyboard, Mouse};
use std::sync::Mutex;
use tauri::{plugin::Plugin, Manager};
use tauri_plugin_global_shortcut::{self, Code};
use tauri_plugin_global_shortcut::{GlobalShortcutExt, Modifiers};

// Enigo state
struct EnigoState(Mutex<enigo::Enigo>);

#[tauri::command]
fn type_string(state: tauri::State<EnigoState>, string: String) {
    let mut enigo = state.0.lock().unwrap();

    // enigo.text(&string).unwrap();
    println!("ANTES: {}", string);
    enigo.text(&string).unwrap();

    enigo
        .key(enigo::Key::Return, enigo::Direction::Click)
        .unwrap();
    println!("DEPOIS: {}", string);
}

#[tauri::command]
fn type_char(ch: char) {
    let mut enigo = enigo::Enigo::new(&enigo::Settings::default()).unwrap();

    println!("{}", ch);

    enigo
        .key(enigo::Key::Unicode(ch), enigo::Direction::Click)
        .unwrap();
}

#[no_mangle]
fn main() {
    tauri::Builder::default()
        .setup(|app| {
            app.manage(EnigoState(Mutex::new(enigo::Enigo::new(
                &enigo::Settings::default(),
            )?)));

            #[cfg(desktop)]
            app.handle()
                .plugin(tauri_plugin_global_shortcut::Builder::new().build())?;

            #[cfg(debug_assertions)]
            {
                let window = app.get_webview_window("main").unwrap();
                window.open_devtools();
            };

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![type_string, type_char,])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
