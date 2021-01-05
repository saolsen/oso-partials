from oso import Oso
from polar import Variable, Expression

from flask import Flask, render_template


def compile_sdf(bindings):
    cases = []
    for i, b in enumerate(bindings):
        x_exp = b["x"]
        x_body = compile_body(x_exp, "x")
        y_exp = b["y"]
        y_body = compile_body(y_exp, "y")
        z_exp = b["z"]
        z_body = compile_body(z_exp, "z")
        ans_exp = b["ans"]
        ans_body = compile_body(ans_exp, "ans")
        case = f"        case {i}: {{\n{x_body}{y_body}{z_body}{ans_body}            result = min(result, ans);\n        }}"
        cases.append(case)
    case_statements = "\n".join(cases)
    switch_statement = f"        switch (i) {{\n{case_statements}\n        default: break;\n        }}\n"
    loop = f"    for(int i=0; i<{len(bindings)}; i++) {{\n{switch_statement}    }}\n"
    sdf_function = f"float sdf(vec3 p) {{\n    float result = 3.402823e+38;\n    float x = p.x;\n    float y = p.y;\n    float z = p.z;\n{loop}    return result;\n}}\n"
    return sdf_function


def compile_body(exp, this_var):
    if isinstance(exp, float):
        if this_var == "ans":
            return f"            float ans = {exp};\n"
        else:
            return f"            if (!({this_var} == {exp})) {{ break; }}\n"
    elif isinstance(exp, Variable):
        return ""
    else:
        assert isinstance(exp, Expression)
        body = compile(exp, this_var)
        if isinstance(body, list):
            body = "            " + "            ".join(body)
        else:
            body = "            " + body
        return body


def compile(exp, this_var):
    if isinstance(exp, int):
        raise Exception("No ints, only floats")
    if isinstance(exp, float):
        return str(exp)
    if isinstance(exp, Variable):
        # This is incredibly stupid, we need a way to get a variables name...
        name = exp.split()[0]
        if name not in ["x", "y", "z", "_this"]:
            name = "_" + this_var + name
        if name == "_this":
            return this_var
        return name
    elif isinstance(exp, Expression):
        if exp.operator == "And":
            args = [compile(arg, this_var) for arg in exp.args]
            return args

        elif exp.operator == "Mul":
            assert len(exp.args) == 3
            lhs = compile(exp.args[0], this_var)
            rhs = compile(exp.args[1], this_var)
            assert isinstance(exp.args[2], Variable)
            result = compile(exp.args[2], this_var)
            return f"float {result} = {lhs} * {rhs};\n"

        elif exp.operator == "Add":
            assert len(exp.args) == 3
            lhs = compile(exp.args[0], this_var)
            rhs = compile(exp.args[1], this_var)
            assert isinstance(exp.args[2], Variable)
            result = compile(exp.args[2], this_var)
            return f"float {result} = {lhs} + {rhs};\n"

        elif exp.operator == "Sub":
            assert len(exp.args) == 3
            lhs = compile(exp.args[0], this_var)
            rhs = compile(exp.args[1], this_var)
            assert isinstance(exp.args[2], Variable)
            result = compile(exp.args[2], this_var)
            return f"float {result} = {lhs} - {rhs};\n"

        elif exp.operator == "Sqrt":
            assert len(exp.args) == 2
            arg = compile(exp.args[0], this_var)
            assert isinstance(exp.args[1], Variable)
            result = compile(exp.args[1], this_var)
            return f"float {result} = sqrt({arg});\n"

        elif exp.operator == "Abs":
            assert len(exp.args) == 2
            arg = compile(exp.args[0], this_var)
            assert isinstance(exp.args[1], Variable)
            result = compile(exp.args[1], this_var)
            return f"float {result} = abs({arg});\n"

        elif exp.operator == "Max":
            assert len(exp.args) == 3
            lhs = compile(exp.args[0], this_var)
            rhs = compile(exp.args[1], this_var)
            assert isinstance(exp.args[2], Variable)
            result = compile(exp.args[2], this_var)
            return f"float {result} = max({lhs}, {rhs});\n"

        elif exp.operator == "Min":
            assert len(exp.args) == 3
            lhs = compile(exp.args[0], this_var)
            rhs = compile(exp.args[1], this_var)
            assert isinstance(exp.args[2], Variable)
            result = compile(exp.args[2], this_var)
            return f"float {result} = min({lhs}, {rhs});\n"

        elif exp.operator == "Geq":
            assert len(exp.args) == 2
            lhs = compile(exp.args[0], this_var)
            rhs = compile(exp.args[1], this_var)
            return f"if (!({lhs} >= {rhs})) {{ break; }}\n"

        elif exp.operator == "Leq":
            assert len(exp.args) == 2
            lhs = compile(exp.args[0], this_var)
            rhs = compile(exp.args[1], this_var)
            return f"if (!({lhs} <= {rhs})) {{ break; }}\n"

        elif exp.operator == "Gt":
            assert len(exp.args) == 2
            lhs = compile(exp.args[0], this_var)
            rhs = compile(exp.args[1], this_var)
            return f"if (!({lhs} > {rhs})) {{ break; }}\n"

        elif exp.operator == "Lt":
            assert len(exp.args) == 2
            lhs = compile(exp.args[0], this_var)
            rhs = compile(exp.args[1], this_var)
            return f"if (!({lhs} < {rhs})) {{ break; }}\n"

        else:
            raise Exception("Unhandled operator")
    else:
        raise Exception("Unimplemented type")


app = Flask(__name__)

print("compiling")
oso = Oso()
oso.load_file("scene.polar")

results = list(
    oso.query_rule("sdf", Variable("x"), Variable("y"), Variable("z"), Variable("ans"))
)
expressions = [result["bindings"] for result in results]
sdf_function = compile_sdf(expressions)
print(sdf_function)


@app.route("/")
def index():
    return render_template("app.html", sdf_function=sdf_function)