// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

//use std::thread;
//use std::time::Duration;

//extern "C" {
//fn startHook(json: &str);
//fn endHook();
//}

// Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

fn main() {
    //let handle = thread::spawn(move || {
    //unsafe {
    //startHook(r#"{"binds": {"F6": "ola", "F7": "autoclicker:10", "F8": "gang gang"}}"#);
    //};
    //});
    //println!("Waiting 10 secs with the hook");
    //thread::sleep(Duration::from_secs(10));
    //println!("10 secs passed, calling endHook()");
    //unsafe { endHook() };

    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
