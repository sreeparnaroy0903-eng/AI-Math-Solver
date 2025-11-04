from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from sympy import symbols, sympify, diff, integrate, simplify, solve, Matrix, Eq

app = Flask(__name__)
CORS(app)

x = symbols('x')

# Derivative steps
def derivative_steps(expr, var):
    steps = []
    terms = expr.as_ordered_terms()
    if len(terms) > 1:
        steps.append("The expression is a sum of terms, so we differentiate each term:")
        for i, term in enumerate(terms, 1):
            steps.append(f"Step {i}: The derivative of {term} is {diff(term, var)}.")
        steps.append(f"Final Result: {diff(expr, var)}")
    else:
        term = terms[0]
        term_derivative = diff(term, var)
        if term.is_Mul:
            steps.append(f"The expression is a product, so we apply the product rule:")
        elif term.is_Pow:
            steps.append(f"The expression is a power, so we apply the power rule:")
        else:
            steps.append(f"The derivative of {term} is {term_derivative}.")
        steps.append(f"Final Result: {term_derivative}")
    return steps

# Integral steps
def integral_steps(expr, var):
    steps = []
    terms = expr.as_ordered_terms()
    if len(terms) > 1:
        steps.append("The integral is a sum, so we integrate each term:")
        for i, term in enumerate(terms, 1):
            steps.append(f"Step {i}: ∫{term} dx = {integrate(term, var)}")
        steps.append(f"Final Result: {integrate(expr, var)}")
    else:
        steps.append(f"Step 1: ∫{expr} dx = {integrate(expr, var)}")
        steps.append(f"Final Result: {integrate(expr, var)}")
    return steps

@app.route('/solve', methods=['POST'])
def solve_problem():
    data = request.get_json()
    problem_type = data.get('type')
    values = data.get('values')
    steps = []
    result = None

    try:
        if problem_type == "derivative":
            expr_str = values.get('expression', '').replace('^', '**')
            expr = sympify(expr_str)
            steps = derivative_steps(expr, x)
            result = str(diff(expr, x))

        elif problem_type == "integral":
            expr_str = values.get('expression', '').replace('^', '**')
            expr = sympify(expr_str)
            steps = integral_steps(expr, x)
            result = str(integrate(expr, x))

        elif problem_type == "simplify":
            expr_str = values.get('expression', '').replace('^', '**')
            expr = sympify(expr_str)
            simplified = simplify(expr)
            steps.append(f"Simplified expression: {simplified}")
            result = str(simplified)

        elif problem_type == "solve_quadratic":
            a = float(values.get('a',0))
            b = float(values.get('b',0))
            c = float(values.get('c',0))
            eq = Eq(a*x**2 + b*x + c, 0)
            sol = solve(eq, x)
            steps.append(f"The quadratic equation {a}x^2 + {b}x + {c} = 0 has solutions:")
            for i, s in enumerate(sol,1):
                steps.append(f"Step {i}: x = {s}")
            result = str(sol)

        elif problem_type == "solve_linear":
            a = float(values.get('a',0))
            b = float(values.get('b',0))
            eq = Eq(a*x + b, 0)
            sol = solve(eq, x)
            steps.append(f"The linear equation {a}x + {b} = 0 has solution:")
            steps.append(f"x = {sol[0]}")
            result = str(sol[0])

        elif problem_type == "arithmetic":
            expr_str = values.get('expression', '')
            expr = sympify(expr_str)
            steps.append(f"Calculating {expr}...")
            result = str(expr)

        elif problem_type == "percentage":
            total = float(values.get('total',0))
            part = float(values.get('part',0))
            percent = (part/total)*100
            steps.append(f"Percentage = (part / total) * 100 = ({part}/{total})*100 = {percent}%")
            result = f"{percent}%"

        elif problem_type == "matrix":
            matrix_vals = values.get('matrix', [])
            mat = Matrix(matrix_vals)
            steps.append("The matrix is:")
            steps.append(str(mat))
            result = str(mat)

        else:
            steps.append("Invalid problem type")
            result = "Error"

    except Exception as e:
        return jsonify({'error': str(e)})

    # ✅ Convert ** to ^ for human-friendly display
    if result is not None:
        result = str(result).replace('**', '^')
    steps = [s.replace('**', '^') for s in steps]

    return jsonify({'steps': steps, 'result': result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))