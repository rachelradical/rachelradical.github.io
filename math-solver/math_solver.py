import sympy as sp

def solve_symbolic_calculus(expression, variable, operation):
    """
    Solves symbolic calculus problems: derivatives or integrals.
    :param expression: Function as a string (e.g., "x**2 + 3*x + 5").
    :param variable: Variable to differentiate/integrate (e.g., "x").
    :param operation: "derivative" or "integral".
    :return: SymPy symbolic result.
    """
    x = sp.Symbol(variable)
    func = sp.sympify(expression)

    if operation == "derivative":
        result = sp.diff(func, x)
        operation_name = "Derivative"
    elif operation == "integral":
        result = sp.integrate(func, x)
        operation_name = "Integral"
    else:
        raise ValueError("Invalid operation. Choose 'derivative' or 'integral'.")

    return operation_name, result

# Interactive User Input
def main():
    print("🔢 Welcome to the Symbolic Math Solver 🔢")
    expression = input("Enter a function (e.g., x**2 + 3*x + 5): ").strip()
    variable = input("Enter the variable (default is 'x'): ").strip() or "x"
    
    operation = ""
    while operation not in ["derivative", "integral"]:
        operation = input("Would you like the derivative or integral? ").strip().lower()

    try:
        operation_name, result = solve_symbolic_calculus(expression, variable, operation)
        print(f"\n✅ {operation_name} of {expression} with respect to {variable}:")
        print(f"➡ {result}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
