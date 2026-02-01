use std::env;

fn main() {
    // Set OpenCV library path
    if let Ok(opencv_dir) = env::var("OPENCV_DIR") {
        println!("cargo:rustc-link-search=native={}/lib", opencv_dir);
    }
    
    // OpenCV configuration through pkg-config
    if pkg_config::Config::new()
        .atleast_version("4.0")
        .probe("opencv4")
        .is_err()
    {
        // Try OpenCV 3 if OpenCV 4 is not available
        if pkg_config::Config::new()
            .atleast_version("3.0")
            .probe("opencv")
            .is_err()
        {
            println!("cargo:warning=OpenCV not found. Please install manually.");
        }
    }
}