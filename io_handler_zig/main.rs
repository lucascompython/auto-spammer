extern "C" {
    fn add(a: i32, b: i32) -> i32;
}

fn main() {
    println!("Hello, world!");
    let num = unsafe { add(1, 2) };
    println!("1 + 2 = {}", num);
}
