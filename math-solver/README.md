# Math Solver Project

## Overview
This project consists of three Python scripts designed to perform and visualize mathematical computations. The goal is to provide an interactive and visually intuitive way to explore optimization, calculus, and function behavior.

## Project Components

### 1. Gradient Descent Optimizer (`gradient_descent.py`)
This script implements gradient descent to find local minima of a function. Users can input their desired function, starting point, learning rate, and other parameters. The algorithm iteratively updates the variable to minimize the function.

**Features:**
- Symbolic differentiation using SymPy
- Iterative optimization with adjustable learning rate and tolerance

### 2. Math Solver (`mathsolver.py`)
This script computes **derivatives** and **integrals** symbolically using SymPy. It allows users to input a function and choose whether they want to differentiate or integrate it.

**Features:**
- Symbolic differentiation and integration
- User-friendly input handling
- Output of exact symbolic results

### 3. Function Visualization (`visualization.py`)
This script generates and saves function plots, including:
- The original function
- Its first derivative
- Tangent line at a specified point
- Integral shading for a given range

Since this script runs in a non-GUI environment, plots are saved as image files (`plot.png`) instead of being displayed interactively.

**Features:**
- Automatic determination of an optimal x-range based on critical points and inflection points
- Visualization of derivatives and integral shading
- Saves plots as static images for easy reference

## How to Run
### **Prerequisites:**
Ensure you have Python installed along with the necessary dependencies:
```sh
pip install numpy sympy matplotlib
```

### **Running Each Script:**
- **Gradient Descent Optimizer:**
  ```sh
  python gradient_descent.py
  ```
  Follow the prompts to input a function and parameters for optimization.

- **Math Solver:**
  ```sh
  python mathsolver.py
  ```
  Enter a function and specify whether to compute its derivative or integral.

- **Function Visualization:**
  ```sh
  python visualization.py
  ```
  Follow the prompts to enter a function and optional settings for tangent lines and integral shading. The output will be saved as `plot.png`.



