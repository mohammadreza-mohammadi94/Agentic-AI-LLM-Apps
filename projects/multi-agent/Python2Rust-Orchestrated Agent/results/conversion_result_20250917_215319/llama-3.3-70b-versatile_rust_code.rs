// Import the necessary libraries
use std::time::Instant;

// Define a function to calculate the number of iterations for a given complex number
fn mandelbrot(c: (f64, f64), max_iter: u32) -> u32 {
    // Initialize the variables
    let mut z = (0.0, 0.0);
    let mut n = 0;
    
    // Loop until the magnitude of z exceeds 2 or the maximum number of iterations is reached
    while (z.0 * z.0 + z.1 * z.1) <= 4.0 && n < max_iter {
        // Update z using the Mandelbrot formula
        let temp = z.0 * z.0 - z.1 * z.1 + c.0;
        z.1 = 2.0 * z.0 * z.1 + c.1;
        z.0 = temp;
        
        // Increment the iteration counter
        n += 1;
    }
    
    // Return the number of iterations
    n
}

// Define a function to compute the Mandelbrot set
fn compute_mandelbrot(width: usize, height: usize, max_iter: u32) -> Vec<Vec<u32>> {
    // Initialize the image with zeros
    let mut image: Vec<Vec<u32>> = vec![vec![0; width]; height];
    
    // Iterate over each pixel in the image
    for row in 0..height {
        for col in 0..width {
            // Map the pixel coordinates to a complex number
            let c = (
                -2.0 + (col as f64 / width as f64) * 3.0,
                -1.5 + (row as f64 / height as f64) * 3.0,
            );
            
            // Calculate the number of iterations for the complex number
            let color = mandelbrot(c, max_iter);
            
            // Store the result in the image
            image[row][col] = color;
        }
    }
    
    // Return the computed image
    image
}

// Define the main function
fn main() {
    // Record the start time
    let start_time = Instant::now();
    
    // Define the image dimensions and maximum number of iterations
    const WIDTH: usize = 80;
    const HEIGHT: usize = 40;
    const MAX_ITER: u32 = 256;
    
    // Compute the Mandelbrot set
    let image = compute_mandelbrot(WIDTH, HEIGHT, MAX_ITER);
    
    // Define the characters to use for rendering the image
    let chars: &str = ".,-~:;=!*#$@";
    
    // Render the image to the console
    for row in image {
        let mut line = String::new();
        for val in row {
            if val == MAX_ITER {
                line.push(' ');
            } else {
                // Use the modulus operator to ensure the index is within bounds
                line.push(chars.chars().nth(val as usize % chars.len()).unwrap());
            }
        }
        println!("{}", line);
    }
    
    // Record the end time and print the execution time
    let end_time = Instant::now();
    println!("\nRust Execution Time: {:.4} seconds", (end_time - start_time).as_secs_f64());
}