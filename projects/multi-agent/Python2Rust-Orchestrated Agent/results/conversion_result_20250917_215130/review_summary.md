# Python to Rust Conversion Review

**Date:** 2025-09-17 21:51
**Judge Model:** `qwen-3-coder-480b`

## Original Python Code

```python

import time

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n

def compute_mandelbrot(width, height, max_iter):
    image = [[0] * width for _ in range(height)]
    for row in range(height):
        for col in range(width):
            c = complex(-2.0 + (col / width) * 3.0, -1.5 + (row / height) * 3.0)
            color = mandelbrot(c, max_iter)
            image[row][col] = color
    return image

if __name__ == "__main__":
    start_time = time.time()
    
    WIDTH, HEIGHT = 80, 40
    MAX_ITER = 256
    
    image = compute_mandelbrot(WIDTH, HEIGHT, MAX_ITER)
    
    chars = ".,-~:;=!*#$@"
    for row in image:
        line = ""
        for val in row:
            if val == MAX_ITER:
                line += " "
            else:
                line += chars[val % len(chars)]
        print(line)
        
    end_time = time.time()
    print(f"\nPython Execution Time: {end_time - start_time:.4f} seconds")

```

--- 

## Judge's Review of Submissions

Here is the consolidated review of the three Rust submissions, evaluated based on **execution result**, **performance**, and **idiomatic style**.

---

### ✅ **Winner: `openai/gpt-oss-120b`**

**Rating: 9.5 / 10**

**Critique:**

- **Execution Result:** ✅ Compiles and runs flawlessly. Output matches the Python reference exactly.
- **Performance:** ✅ Excellent. Uses direct `f64` arithmetic without unnecessary abstractions. Pre-allocates the image vector efficiently. Fastest execution time among the working submissions.
- **Idiomatic Style:** ✅ Very clean and idiomatic Rust. Uses appropriate types (`usize` for counts and indices), includes helpful comments and documentation, and leverages iterators effectively. The use of `Vec<char>` for the shading characters is a good touch for performance and clarity.

**Minor Improvements:**
- Could use `char` directly instead of collecting into a `Vec<char>` if only random access is needed (though the performance gain is negligible and the current approach is acceptable).
- Minor nitpick: `2‑D` in the comment should be `2-D` (non-breaking hyphen used).

---

### 🟨 **Runner-up: `llama-4-maverick-17b-128e-instruct`**

**Rating: 7.5 / 10**

**Critique:**

- **Execution Result:** ✅ Compiles and runs correctly. Output matches the reference.
- **Performance:** ⚠️ Adequate but not optimal. Introduces a custom `Complex` struct with method calls (`mul`, `add`, `abs`) which adds overhead compared to direct arithmetic. While not a major bottleneck for this small size, it's less efficient than inline computation.
- **Idiomatic Style:** ⚠️ Generally idiomatic, but the custom `Complex` struct and manual implementations are overkill for this simple use case. The use of `into_iter()` and `map()` in the rendering loop is clean, though the `unwrap()` call on `chars.nth()` could be avoided by using a pre-collected vector or direct indexing.

**Improvements:**
- Replace the `Complex` struct with direct `f64` computations for better performance.
- Avoid `unwrap()` by pre-collecting the characters into a `Vec<char>` or using `.as_bytes()[index] as char`.

---

### ❌ **Failed Submission: `llama-3.3-70b-versatile`**

**Rating: 2 / 10**

**Critique:**

- **Execution Result:** ❌ Fails to compile due to an invalid crate name (`temp_llama_3.3_70b_versatile`). This is a fundamental tooling issue, not a code logic problem, but it renders the submission unusable.
- **Performance:** ⚠️ Would likely be acceptable if it compiled. Logic mirrors the Python version closely, using tuple-based complex number representation and direct arithmetic.
- **Idiomatic Style:** ⚠️ Reasonable use of `String::new()` and `push()`, but the character lookup uses `.nth().unwrap()`, which is inefficient and unsafe. A pre-collected `Vec<char>` or direct byte indexing would be better.

**Improvements:**
- Fix the crate name issue (e.g., rename the file or use `#![crate_name = "..."]`).
- Replace `chars.chars().nth(val as usize % chars.len()).unwrap()` with a more efficient and safe character lookup.

---

### 🏆 Final Rankings:

1. **`openai/gpt-oss-120b`** – 9.5/10 ✅ Fast, correct, idiomatic.
2. **`llama-4-maverick-17b-128e-instruct`** – 7.5/10 ✅ Correct output, but suboptimal performance due to abstraction.
3. **`llama-3.3-70b-versatile`** – 2/10 ❌ Fails to compile due to tooling error; logic otherwise acceptable but inefficient.

---