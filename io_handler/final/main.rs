use std::ffi::CString;
use std::os::raw::c_char;
use std::{thread, time};
extern "C" {
    fn startHook(json: &str);
    fn endHook();
}

fn main() {
    println!("Hello, world!");
    let millis = time::Duration::from_millis(10000);
    let json = r#"{
        "binds": {
            "F6": "ola",
            "F7": "autoclicker:10",
            "F8": "gang gang"
        }
    }"#;

    //let c_s = CString::new(json).unwrap();
    unsafe {
        let start = thread::spawn(move || {
            startHook(json);
        });
        println!("startHook() called, waiting 10 seconds");
        thread::sleep(millis);
        println!("10 seconds passed, calling endHook()");
        endHook();
        //println!("endHook() called, waiting 2 seconds and then calling startHook() again");
        //thread::sleep(time::Duration::from_millis(2000));
        //println!("2 seconds passed, calling startHook() again");
        //let start2 = thread::spawn(move || {
        //startHook(c_s);
        //});
        //println!("startHook() called, waiting 10 seconds");
        //thread::sleep(millis);
        //println!("10 seconds passed, calling endHook()");
        //endHook();

        start.join().unwrap();
        //start2.join().unwrap();
    }
}
