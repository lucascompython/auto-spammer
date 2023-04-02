use std::{thread, time};
extern "C" {
    fn startHook();
    fn endHook();
}

fn main() {
    println!("Hello, world!");
    let millis = time::Duration::from_millis(10000);
    unsafe {
        let start = thread::spawn(move || {
            startHook();
        });
        println!("startHook() called, waiting 10 seconds");
        thread::sleep(millis);
        println!("10 seconds passed, calling endHook()");
        endHook();
        println!("endHook() called, waiting 2 seconds and then calling startHook() again");
        thread::sleep(time::Duration::from_millis(2000));
        println!("2 seconds passed, calling startHook() again");
        let start2 = thread::spawn(move || {
            startHook();
        });
        println!("startHook() called, waiting 10 seconds");
        thread::sleep(millis);
        println!("10 seconds passed, calling endHook()");
        endHook();

        start.join().unwrap();
        //start2.join().unwrap();
    }
}
