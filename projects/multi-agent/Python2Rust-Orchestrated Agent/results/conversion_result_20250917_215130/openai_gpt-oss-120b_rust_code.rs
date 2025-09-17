use std::time::Instant;

/// Compute the number of iterations for a point `c` in the Mandelbrot set.
/// Returns the iteration count (0..=max_iter). If the point does not escape,
/// the function returns `max_iter`.
fn mandelbrot(c_re: f64, c_im: f64, max_iter: usize) -> usize {
    let mut z_re = 0.0_f64;
    let mut z_im = 0.0_f64;
    let mut n = 0usize;

    // Escape radius squared is 4 (i.e., |z| <= 2)
    while n < max_iter && (z_re * z_re + z_im * z_im) <= 4.0 {
        // z = z*z + c  (complex multiplication)
        let temp_re = z_re * z_re - z_im * z_im + c_re;
        let temp_im = 2.0 * z_re * z_im + c_im;
        z_re = temp_re;
        z_im = temp_im;
        n += 1;
    }
    n
}

/// Generate a 2‑D image (vector of rows) where each entry is the iteration count
/// for the corresponding pixel.
fn compute_mandelbrot(width: usize, height: usize, max_iter: usize) -> Vec<Vec<usize>> {
    // Pre‑allocate the image with the correct dimensions.
    let mut image = vec![vec![0usize; width]; height];

    for row in 0..height {
        // Map `row` to the imaginary axis: -1.5 .. +1.5
        let c_im = -1.5 + (row as f64 / height as f64) * 3.0;
        for col in 0..width {
            // Map `col` to the real axis: -2.0 .. +1.0
            let c_re = -2.0 + (col as f64 / width as f64) * 3.0;
            let iter = mandelbrot(c_re, c_im, max_iter);
            image[row][col] = iter;
        }
    }
    image
}

fn main() {
    // Measure execution time.
    let start = Instant::now();

    const WIDTH: usize = 80;
    const HEIGHT: usize = 40;
    const MAX_ITER: usize = 256;

    let image = compute_mandelbrot(WIDTH, HEIGHT, MAX_ITER);

    // Characters used for ASCII shading, from light to dark.
    let shades: Vec<char> = ".,-~:;=!*#$@".chars().collect();

    for row in image.iter() {
        let mut line = String::with_capacity(WIDTH);
        for &val in row.iter() {
            if val == MAX_ITER {
                line.push(' ');
            } else {
                // Cycle through the shading characters.
                let idx = val % shades.len();
                line.push(shades[idx]);
            }
        }
        println!("{}", line);
    }

    let duration = start.elapsed();
    println!(
        "\nRust Execution Time: {:.4} seconds",
        duration.as_secs_f64()
    );
}