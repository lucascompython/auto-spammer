// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use enigo::Keyboard;
use tauri::{plugin::Plugin, Manager};

#[tauri::command]
fn type_string(string: String) {
    let mut enigo = enigo::Enigo::new(&enigo::Settings::default()).unwrap();
    // enigo.text(&string).unwrap();
    println!("Hello, World!");
    enigo.text("Hello, World!");
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_global_shortcut::Builder::new().build())
        .setup(|app| {
            // #[cfg(desktop)]
            // app.handle()
            //     .plugin(tauri_plugin_global_shortcut::Builder::new().build())?;
            // Ok(())
            #[cfg(debug_assertions)] // only include this code on debug builds
            {
                let window = app.get_webview_window("main").unwrap();
                window.open_devtools();
            }

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![type_string])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

// fn main() {
//     tauri::Builder::default()
//         // .plugin(tauri_plugin_shell::init())
//         .invoke_handler(tauri::generate_handler![greet])
//         .run(tauri::generate_context!())
//         .expect("error while running tauri application");
// }
