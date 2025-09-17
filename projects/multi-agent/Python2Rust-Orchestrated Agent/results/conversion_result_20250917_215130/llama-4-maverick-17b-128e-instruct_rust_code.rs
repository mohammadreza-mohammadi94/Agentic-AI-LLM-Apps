use std::time::Instant;

// Define a complex number struct to mimic Python's complex type
#[derive(Copy, Clone)]
struct Complex {
    re: f64,
    im: f64,
}

impl Complex {
    // Implement complex number operations
    fn new(re: f64, im: f64) -> Self {
        Complex { re, im }
    }

    fn abs(&self) -> f64 {
        (self.re * self.re + self.im * self.im).sqrt()
    }

    fn mul(&self, other: &Complex) -> Complex {
        Complex::new(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )
    }

    fn add(&self, other: &Complex) -> Complex {
        Complex::new(self.re + other.re, self.im + other.im)
    }
}

// Compute the Mandelbrot set for a given complex number
fn mandelbrot(c: Complex, max_iter: u32) -> u32 {
    let mut z = Complex::new(0.0, 0.0);
    let mut n = 0;
    while z.abs() <= 2.0 && n < max_iter {
        z = z.mul(&z).add(&c);
        n += 1;
    }
    n
}

// Compute the Mandelbrot set for a given image size
fn compute_mandelbrot(width: usize, height: usize, max_iter: u32) -> Vec<Vec<u32>> {
    let mut image = vec![vec![0; width]; height];
    for row in 0..height {
        for col in 0..width {
            let c = Complex::new(
                -2.0 + (col as f64 / width as f64) * 3.0,
                -1.5 + (row as f64 / height as f64) * 3.0,
            );
            let color = mandelbrot(c, max_iter);
            image[row][col] = color;
        }
    }
    image
}

fn main() {
    let start_time = Instant::now();

    let width = 80;
    let height = 40;
    let max_iter = 256;

    let image = compute_mandelbrot(width, height, max_iter);

    let chars = ".,-~:;=!*#$@";
    for row in image {
        let line: String = row
            .into_iter()
            .map(|val| {
                if val == max_iter {
                    ' '
                } else {
                    chars.chars().nth((val % chars.len() as u32) as usize).unwrap()
                }
            })
            .collect();
        println!("{}", line);
    }

    let end_time = start_time.elapsed().as_secs_f64();
    println!("\nRust Execution Time: {:.4} seconds", end_time);
}