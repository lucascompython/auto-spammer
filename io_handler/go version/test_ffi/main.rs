// main.rs
use std::ffi::CString;
use std::ffi::OsStr;
use std::mem::MaybeUninit;
use std::os::raw::c_char;
use std::os::windows::ffi::OsStrExt;
use std::os::windows::ffi::OsStringExt;
use std::ptr;

extern "C" {
    fn print_num(num: i32);
}

fn main() {
    println!("[rust] start");
    unsafe { print_num(50) }
}
