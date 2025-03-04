import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

def gradient_descent(func_expr, variable="x", start=0.0, alpha=0.1, tolerance=1e-6, max_iters=1000):
    """
    Finds a local minimum of a function using gradient descent.
    
    :param func_expr: Function as a string (e.g., "x**2 - 4*x + 4").
    :param variable: Variable in the function (default: "x").
    :param start: Initial guess for x.
    :param alpha: Learning rate (step size).
    :param tolerance: Stopping condition for small changes.
    :param max_iters: Max iterations before stopping.
    :return: Minimum x value, function value at minimum, and history of steps.
    """
    x = sp.Symbol(variable)
    func = sp.sympify(func_expr)
    derivative = sp.diff(func, x)

    # Convert symbolic derivative to a numerical function
    grad = sp.lambdify(x, derivative, "numpy")
    f = sp.lambdify(x, func, "numpy")

    x_val = start
    history = [(x_val, f(x_val))]

    for i in range(max_iters):
        step = alpha * grad(x_val)
        if np.isnan(step) or np.isinf(step):
             print("❌ Numerical instability detected. Try reducing the learning rate.")
             break
        if abs(step) < tolerance:  # Convergence check
            break
        x_val -= step
        history.append((x_val, f(x_val)))

    return x_val, f(x_val), history

def plot_gradient_descent(func_expr, variable="x", start=0.0, alpha=0.1, tolerance=1e-6, max_iters=1000):
    """
    Runs gradient descent and visualizes the optimization process.
    """
    x = sp.Symbol(variable)
    func = sp.sympify(func_expr)
    f = sp.lambdify(x, func, "numpy")

    min_x, min_f, history = gradient_descent(func_expr, variable, start, alpha, tolerance, max_iters)

    # Extract x and y values from history
    x_vals = np.linspace(min_x - 5, min_x + 5, 400)
    y_vals = f(x_vals)
    descent_x = [step[0] for step in history]
    descent_y = [step[1] for step in history]

    # Plot function
    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, label=f"f({variable}) = {func_expr}", linewidth=2)
    plt.scatter(descent_x, descent_y, color='red', label="Gradient Descent Steps", zorder=3)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.xlabel(variable)
    plt.ylabel("f(x)")
    plt.legend()
    plt.title("Gradient Descent Optimization")
    plt.grid(True)
    plt.show()

    print(f"\n✅ Minimum found at x = {min_x:.6f}, f(x) = {min_f:.6f}")

# Interactive User Input
def main():
    print("📉 Welcome to the Gradient Descent Optimizer 📉")
    expression = input("Enter a function to minimize (e.g., x**2 - 4*x + 4): ").strip()
    variable = input("Enter the variable (default is 'x'): ").strip() or "x"

    try:
        start = float(input("Enter starting x-value (default 0.0): ") or "0.0")
        alpha = float(input("Enter learning rate (default 0.1): ") or "0.1")
        tolerance = float(input("Enter tolerance (default 1e-6): ") or "1e-6")
        max_iters = int(input("Enter max iterations (default 1000): ") or "1000")

        plot_gradient_descent(expression, variable, start, alpha, tolerance, max_iters)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

