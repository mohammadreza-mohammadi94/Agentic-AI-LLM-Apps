// Import the necessary libraries
use std::time::Instant;

// Define a function to calculate the number of iterations for a given complex number
fn mandelbrot(c: (f64, f64), max_iter: u32) -> u32 {
    // Initialize the variables
    let mut z = (0.0, 0.0);
    let mut n = 0;
    
    // Continue iterating until the magnitude of z exceeds 2 or we reach the maximum number of iterations
    while (z.0 * z.0 + z.1 * z.1) <= 4.0 && n < max_iter {
        // Update z using the quadratic recurrence formula
        let temp = z.0 * z.0 - z.1 * z.1 + c.0;
        z.1 = 2.0 * z.0 * z.1 + c.1;
        z.0 = temp;
        // Increment the iteration count
        n += 1;
    }
    n
}

// Define a function to compute the Mandelbrot set for a given width, height, and maximum number of iterations
fn compute_mandelbrot(width: u32, height: u32, max_iter: u32) -> Vec<Vec<u32>> {
    // Create a 2D vector to store the image
    let mut image: Vec<Vec<u32>> = vec![vec![0; width as usize]; height as usize];
    
    // Iterate over each pixel in the image
    for row in 0..height {
        for col in 0..width {
            // Map the pixel coordinates to a complex number
            let c = (
                -2.0 + (col as f64 / width as f64) * 3.0,
                -1.5 + (row as f64 / height as f64) * 3.0,
            );
            // Calculate the number of iterations for the current complex number
            let color = mandelbrot(c, max_iter);
            // Store the result in the image
            image[row as usize][col as usize] = color;
        }
    }
    image
}

fn main() {
    // Record the start time
    let start_time = Instant::now();
    
    // Define the image dimensions and maximum number of iterations
    let width = 80;
    let height = 40;
    let max_iter = 256;
    
    // Compute the Mandelbrot set
    let image = compute_mandelbrot(width, height, max_iter);
    
    // Define a string of characters to use for rendering the image
    let chars = ".,-~:;=!*#$@";
    
    // Render the image to the console
    for row in image {
        let mut line = String::new();
        for val in row {
            if val == max_iter {
                line.push(' ');
            } else {
                // Use the modulo operator to cycle through the characters
                line.push(chars.chars().nth(val as usize % chars.len()).unwrap());
            }
        }
        println!("{}", line);
    }
    
    // Record the end time and print the execution time
    let end_time = Instant::now();
    println!("\nRust Execution Time: {:.4} seconds", end_time.duration_since(start_time).as_secs_f64());
}