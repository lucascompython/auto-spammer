// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
#![no_main]

use enigo::Keyboard;
use tauri::{plugin::Plugin, Manager};
use tauri_plugin_global_shortcut::{self, Code};
use tauri_plugin_global_shortcut::{GlobalShortcutExt, Modifiers};

#[tauri::command]
fn type_string(string: String) {
    let mut enigo = enigo::Enigo::new(&enigo::Settings::default()).unwrap();
    // enigo.text(&string).unwrap();
    println!("Hello, World!");
    enigo.text("Hello, World!").unwrap();
}

#[no_mangle]
fn main() {
    tauri::Builder::default()
        // .plugin(tauri_plugin_global_shortcut::init())
        .setup(|app| {
            // #[cfg(desktop)]
            // app.handle()
            //     .plugin(tauri_plugin_global_shortcut::Builder::new().build())?;
            // Ok(())

            #[cfg(desktop)]
            app.handle().plugin(
                tauri_plugin_global_shortcut::Builder::with_handler(move |_app, shortcut| {
                    let mut enigo = enigo::Enigo::new(&enigo::Settings::default()).unwrap();
                    if shortcut.matches(Modifiers::empty(), Code::KeyO) {
                        enigo.text("view monitor").unwrap();
                        // std::thread::sleep(std::time::Duration::from_millis(100));
                        //press enter
                        enigo
                            .key(enigo::Key::Return, enigo::Direction::Click)
                            .unwrap();
                    } else if shortcut.matches(Modifiers::empty(), Code::KeyP) {
                        enigo.text("switch").unwrap();
                        // sleep for 1 second
                        // std::thread::sleep(std::time::Duration::from_millis(100));
                        //press enter
                        enigo
                            .key(enigo::Key::Return, enigo::Direction::Click)
                            .unwrap();
                    }
                })
                .build(),
            )?;

            #[cfg(debug_assertions)] // only include this code on debug builds
            {
                let window = app.get_webview_window("main").unwrap();
                window.open_devtools();
            };
            app.global_shortcut().register("o")?;
            app.global_shortcut().register("p")?;

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
