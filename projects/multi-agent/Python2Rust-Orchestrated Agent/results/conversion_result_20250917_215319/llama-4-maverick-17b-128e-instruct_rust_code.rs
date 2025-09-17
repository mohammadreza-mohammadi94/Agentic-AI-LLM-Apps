use std::time::Instant;

// Define a complex number struct for simplicity
#[derive(Copy, Clone)]
struct Complex {
    re: f64,
    im: f64,
}

impl Complex {
    // Implement complex number multiplication and addition
    fn mul(self, other: Complex) -> Complex {
        Complex {
            re: self.re * other.re - self.im * other.im,
            im: self.re * other.im + self.im * other.re,
        }
    }

    fn add(self, other: Complex) -> Complex {
        Complex {
            re: self.re + other.re,
            im: self.im + other.im,
        }
    }

    // Calculate the magnitude squared of the complex number
    fn norm_sqr(self) -> f64 {
        self.re * self.re + self.im * self.im
    }
}

fn mandelbrot(c: Complex, max_iter: u32) -> u32 {
    let mut z = Complex { re: 0.0, im: 0.0 };
    let mut n = 0;
    while z.norm_sqr() <= 4.0 && n < max_iter {
        z = z.mul(z).add(c);
        n += 1;
    }
    n
}

fn compute_mandelbrot(width: usize, height: usize, max_iter: u32) -> Vec<Vec<u32>> {
    let mut image = vec![vec![0; width]; height];
    for row in 0..height {
        for col in 0..width {
            let c = Complex {
                re: -2.0 + (col as f64 / width as f64) * 3.0,
                im: -1.5 + (row as f64 / height as f64) * 3.0,
            };
            let color = mandelbrot(c, max_iter);
            image[row][col] = color;
        }
    }
    image
}

fn main() {
    let start_time = Instant::now();
    
    let width: usize = 80;
    let height: usize = 40;
    let max_iter: u32 = 256;
    
    let image = compute_mandelbrot(width, height, max_iter);
    
    let chars = ".,-~:;=!*#$@";
    for row in image {
        let line: String = row.into_iter().map(|val| {
            if val == max_iter {
                ' '
            } else {
                chars.chars().nth((val % chars.len() as u32) as usize).unwrap()
            }
        }).collect();
        println!("{}", line);
    }
        
    let end_time = start_time.elapsed().as_secs_f64();
    println!("\nRust Execution Time: {:.4} seconds", end_time);
}