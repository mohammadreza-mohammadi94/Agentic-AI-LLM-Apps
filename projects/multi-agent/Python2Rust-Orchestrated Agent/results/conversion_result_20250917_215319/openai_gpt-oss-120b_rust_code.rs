use std::time::Instant;

/// Compute the number of iterations for a point `c` in the Mandelbrot set.
///
/// This mirrors the Python `mandelbrot` function. We work with the real and
/// imaginary parts directly to avoid pulling in an external complex number crate.
fn mandelbrot(c_re: f64, c_im: f64, max_iter: usize) -> usize {
    let mut z_re = 0.0_f64;
    let mut z_im = 0.0_f64;
    let mut n = 0;

    // `abs(z) <= 2` is equivalent to `z_re*z_re + z_im*z_im <= 4`.
    while z_re * z_re + z_im * z_im <= 4.0 && n < max_iter {
        // z = z*z + c  (complex multiplication)
        let new_re = z_re * z_re - z_im * z_im + c_re;
        let new_im = 2.0 * z_re * z_im + c_im;
        z_re = new_re;
        z_im = new_im;
        n += 1;
    }
    n
}

/// Compute the Mandelbrot set for a given image size.
///
/// Returns a 2‑D vector where each entry holds the iteration count for that pixel.
fn compute_mandelbrot(width: usize, height: usize, max_iter: usize) -> Vec<Vec<usize>> {
    // Pre‑allocate the image with zeros (same as Python's list comprehension).
    let mut image = vec![vec![0usize; width]; height];

    for row in 0..height {
        for col in 0..width {
            // Map pixel coordinates to the complex plane.
            // Python: complex(-2.0 + (col / width) * 3.0,
            //                -1.5 + (row / height) * 3.0)
            let c_re = -2.0 + (col as f64 / width as f64) * 3.0;
            let c_im = -1.5 + (row as f64 / height as f64) * 3.0;
            let color = mandelbrot(c_re, c_im, max_iter);
            image[row][col] = color;
        }
    }
    image
}

fn main() {
    let start = Instant::now();

    const WIDTH: usize = 80;
    const HEIGHT: usize = 40;
    const MAX_ITER: usize = 256;

    let image = compute_mandelbrot(WIDTH, HEIGHT, MAX_ITER);

    // Characters used to render the ASCII art, identical to the Python version.
    let chars: Vec<char> = ".,-~:;=!*#$@".chars().collect();

    for row in image.iter() {
        let mut line = String::with_capacity(WIDTH);
        for &val in row.iter() {
            if val == MAX_ITER {
                line.push(' ');
            } else {
                // Wrap the index around the length of `chars`.
                let idx = val % chars.len();
                line.push(chars[idx]);
            }
        }
        println!("{}", line);
    }

    let duration = start.elapsed();
    println!("\nRust Execution Time: {:.4} seconds", duration.as_secs_f64());
}