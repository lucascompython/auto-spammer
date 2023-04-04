fn main() {
    if cfg!(debug_assertions) {
        use std::env::consts::OS;
        use std::process::Command;
        let ext = if OS == "windows" { "dll" } else { "a" };
        Command::new("go")
            .args(&[
                "build",
                "-buildmode=c-shared",
                "-o",
                &format!("../../libio.{}", ext),
                "io.go",
            ])
            .current_dir("./src/io_handler")
            .status()
            .expect("failed to build io library");
        println!("cargo:rerun-if-changed=src/io_handler/io.go");
    }

    println!("cargo:rustc-link-search=native=./");
    println!("cargo:rustc-link-lib=dylib=io");
    tauri_build::build()
}
