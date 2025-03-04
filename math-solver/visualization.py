import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

def find_optimal_x_range(expression, variable="x", margin=2):
    """
    Determines an optimal x-range based on critical points and inflection points.
    """
    x = sp.Symbol(variable)
    func_sym = sp.sympify(expression)
    derivative_sym = sp.diff(func_sym, x)
    second_derivative_sym = sp.diff(derivative_sym, x)
    
    critical_points = sp.solve(derivative_sym, x)
    inflection_points = sp.solve(second_derivative_sym, x)
    
    all_points = [float(p.evalf()) for p in critical_points + inflection_points if p.is_real]
    if all_points:
        x_min, x_max = min(all_points) - margin, max(all_points) + margin
    else:
        x_min, x_max = -10, 10  # Default range if no critical points found
    
    return x_min, x_max

def plot_function(expression, variable="x", x_range=None, point=None, integral_bounds=None, save_path="plot.png"):
    """
    Plots a function, its derivative, and optionally shades the integral area.
    """
    if x_range is None:
        x_range = find_optimal_x_range(expression, variable)
    
    x = sp.Symbol(variable)
    func_sym = sp.sympify(expression)
    derivative_sym = sp.diff(func_sym, x)
    
    func = sp.lambdify(x, func_sym, "numpy")
    derivative = sp.lambdify(x, derivative_sym, "numpy")
    
    x_vals = np.linspace(x_range[0], x_range[1], 400)
    y_vals = func(x_vals)
    dy_vals = derivative(x_vals)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_vals, y_vals, label=f"f({variable}) = {expression}", linewidth=2)
    ax.plot(x_vals, dy_vals, linestyle='dashed', label=f"f'({variable})", color='green')
    
    if point is not None:
        slope = derivative(point)
        tangent_y = slope * (x_vals - point) + func(point)
        ax.plot(x_vals, tangent_y, linestyle='dotted', color='red', label=f"Tangent at x={point}")
    
    if integral_bounds is not None:
        try:
            a, b = integral_bounds
            x_int = np.linspace(a, b, 100)
            y_int = func(x_int)
            ax.fill_between(x_int, y_int, alpha=0.3, color='gray', label=f"∫ from {a} to {b}")
        except Exception as e:
            print(f"❌ Error shading integral: {e}")
    
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_xlabel(variable)
    ax.set_ylabel("f(x)")
    ax.legend()
    ax.set_title("Function, Derivative, and Integral Visualization")
    ax.grid(True)
    
    plt.savefig(save_path)
    print(f"✅ Plot saved as '{save_path}'. Open it to view.")
    plt.close()

def main():
    print("📊 Welcome to the Interactive Math Visualizer! 📊")
    expression = input("Enter a function to visualize (e.g., x**3 - 6*x**2 + 4*x + 12): ").strip()
    variable = input("Enter the variable (default is 'x'): ").strip() or "x"
    
    point = input("Enter a point to show the tangent line (or press Enter to skip): ")
    point = float(point) if point else None
    
    integral_input = input("Enter two numbers (a b) to shade the integral area (or press Enter to skip): ")
    try:
        integral_bounds = tuple(map(float, integral_input.split())) if integral_input else None
        if integral_bounds and len(integral_bounds) != 2:
            raise ValueError("Please enter exactly two numbers separated by a space.")
    except ValueError as e:
        print(f"❌ Invalid integral bounds: {e}")
        integral_bounds = None
    
    plot_function(expression, variable, None, point, integral_bounds)

if __name__ == "__main__":
    main()
