from oso import Oso
from polar import Variable, Expression

from flask import Flask, render_template

sdf_header = """
float sdf(vec3 p) {
    float x = p.x;
    float y = p.y;
    float z = p.z;

"""

sdf_footer = """
    return _this;
}
"""


def compile(exp):
    if isinstance(exp, float):
        return str(exp)
    if isinstance(exp, Variable):
        # This is incredibly stupid, we need a way to get a variables name...
        return exp.split()[0]
    elif isinstance(exp, Expression):
        if exp.operator == "And":
            args = [compile(arg) for arg in exp.args]
            sdf_body = "    " + "    ".join(args)

            return f"{sdf_header}{sdf_body}{sdf_footer}"

        elif exp.operator == "Mul":
            assert len(exp.args) == 3
            lhs = compile(exp.args[0])
            rhs = compile(exp.args[1])
            assert isinstance(exp.args[2], Variable)
            result = compile(exp.args[2])
            return f"float {result} = {lhs} * {rhs};\n"

        elif exp.operator == "Add":
            assert len(exp.args) == 3
            lhs = compile(exp.args[0])
            rhs = compile(exp.args[1])
            assert isinstance(exp.args[2], Variable)
            result = compile(exp.args[2])
            return f"float {result} = {lhs} + {rhs};\n"

        elif exp.operator == "Sub":
            assert len(exp.args) == 3
            lhs = compile(exp.args[0])
            rhs = compile(exp.args[1])
            assert isinstance(exp.args[2], Variable)
            result = compile(exp.args[2])
            return f"float {result} = {lhs} - {rhs};\n"

        elif exp.operator == "Sqrt":
            assert len(exp.args) == 2
            arg = compile(exp.args[0])
            assert isinstance(exp.args[1], Variable)
            result = compile(exp.args[1])
            return f"float {result} = sqrt({arg});\n"

        else:
            raise Exception("Unhandled operator")
    else:
        raise Exception("Unimplemented type")


app = Flask(__name__)


@app.route("/")
def index():
    oso = Oso()
    oso.load_file("scene.polar")

    results = list(
        oso.query_rule(
            "sdf", Variable("x"), Variable("y"), Variable("z"), Variable("ans")
        )
    )
    expressions = [result["bindings"]["ans"] for result in results]
    assert len(expressions) == 1

    sdf_function = compile(expressions[0])
    print(sdf_function)

    # sdf_function = """
    # float sphere(vec3 pos, vec3 center, float radius) {
    #     return length(pos - center) - radius;
    # }

    # float box(vec3 pos, vec3 center, vec3 size, float corner) {
    #     return length(max(abs(pos-center)-size, 0.0))-corner;
    # }

    # float unite(float a, float b) { return min(a,b); }
    # float subtract(float a, float b) { return max(-a,b); }
    # float intersect(float a, float b) { return max(a,b); }

    # // This is what we're going to generate from the polar partial.
    # float sdf(vec3 p) {
    #     float s = sphere(p, vec3(0.), 1.25);
    #     float b = box(p, vec3(0.), vec3(1.), 0.);
    #     return subtract(s, b);
    # }
    # """

    return render_template("app.html", sdf_function=sdf_function)