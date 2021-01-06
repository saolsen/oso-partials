from oso import Oso
from polar import Variable, Expression

from flask import Flask, render_template

from toposort import toposort, toposort_flatten


def compile_sdf(bindings):
    def binop2(op, exp, this):
        statement = {"depends": []}

        assert len(exp.args) == 3

        lhs = exp.args[0]
        if isinstance(exp.args[0], Variable):
            lhs = lhs.split()[0]
            if lhs == "_this":
                lhs = this
            statement["depends"].append(lhs)
        else:
            assert isinstance(exp.args[0], float)
            lhs = exp.args[0]

        rhs = exp.args[1]
        if isinstance(exp.args[1], Variable):
            rhs = rhs.split()[0]
            if rhs == "_this":
                rhs = this
            statement["depends"].append(rhs)
        else:
            assert isinstance(exp.args[1], float)
            rhs = exp.args[1]

        result = exp.args[2]
        if isinstance(exp.args[2], Variable):
            result = result.split()[0]
            if result == "_this":
                result = this
            statement["defines"] = result
            statement["set"] = f"float {result} = {lhs} {op} {rhs};\n"
        else:
            assert isinstance(exp.args[1], float)
            statement["defines"] = None
        statement["check"] = f"if (({lhs} {op} {rhs}) != {result}) {{ break; }}\n"

        return statement

    def callop1(op, exp, this):
        statement = {"depends": []}

        assert len(exp.args) == 2
        lhs = exp.args[0]
        if isinstance(exp.args[0], Variable):
            lhs = lhs.split()[0]
            if lhs == "_this":
                lhs = this
            statement["depends"].append(lhs)
        else:
            assert isinstance(exp.args[0], float)
            lhs = exp.args[0]

        result = exp.args[1]
        if isinstance(exp.args[1], Variable):
            result = result.split()[0]
            if result == "_this":
                result = this
            statement["defines"] = result
            statement["set"] = f"float {result} = {op}({lhs});\n"
        else:
            assert isinstance(exp.args[1], float)
            statement["defines"] = None
        statement["check"] = f"if ({op}({lhs}) != {result}) {{ break; }}\n"

        return statement

    def callop2(op, exp, this):
        statement = {"depends": []}

        assert len(exp.args) == 3
        lhs = exp.args[0]
        if isinstance(exp.args[0], Variable):
            lhs = lhs.split()[0]
            if lhs == "_this":
                lhs = this
            statement["depends"].append(lhs)
        else:
            assert isinstance(exp.args[0], float)
            lhs = exp.args[0]

        rhs = exp.args[1]
        if isinstance(exp.args[1], Variable):
            rhs = rhs.split()[0]
            if rhs == "_this":
                rhs = this
            statement["depends"].append(rhs)
        else:
            assert isinstance(exp.args[1], float)
            rhs = exp.args[1]

        result = exp.args[2]
        if isinstance(exp.args[2], Variable):
            result = result.split()[0]
            if result == "_this":
                result = this
            statement["defines"] = result
            statement["set"] = f"float {result} = {op}({lhs},{rhs});\n"
        else:
            assert isinstance(exp.args[2], float)
            statement["defines"] = None
        statement["check"] = f"if ({op}({lhs},{rhs}) != {result}) {{ break; }}\n"

        return statement

    def comp(op, exp, this):
        statement = {"depends": [], "defines": None}

        assert len(exp.args) == 3
        lhs = exp.args[0]
        if isinstance(exp.args[0], Variable):
            lhs = lhs.split()[0]
            if lhs == "_this":
                lhs = this
            statement["depends"].append(lhs)
        else:
            assert isinstance(exp.args[0], float)
            lhs = exp.args[0]
        rhs = exp.args[1]
        if isinstance(exp.args[1], Variable):
            rhs = rhs.split()[1]
            if rhs == "_this":
                rhs = this
            statement["depends"].append(rhs)
        else:
            assert isinstance(exp.args[1], float)

        statement["check"] = f"if (!({lhs} {op} {rhs})) {{ break; }}\n"

        return statement

    def statements(bindings):
        stmnts = [
            {
                "defines": "x",
                "depends": [],
                "set": "float x = p.x;",
                "check": "if (!(x == p.x) {{ break; }}",
            },
            {
                "defines": "y",
                "depends": [],
                "set": "float y = p.x;",
                "check": "if (!(y == p.y) {{ break; }}",
            },
            {
                "defines": "z",
                "depends": [],
                "set": "float z = p.x;",
                "check": "if (!(z == p.z) {{ break; }}",
            },
        ]

        for k, v in bindings.items():
            if isinstance(v, float):
                stmnts.append(
                    {
                        "defines": k,
                        "depends": [],
                        "set": f"float {k} = {v};",
                        "check": f"if (!({k} == {v}) {{ break; }}",
                    }
                )
            if isinstance(v, Expression):
                assert v.operator == "And"
                for exp in v.args:
                    if exp.operator == "Mul":
                        stmnts.append(binop2("*", exp, k))

                    elif exp.operator == "Add":
                        stmnts.append(binop2("+", exp, k))

                    elif exp.operator == "Sub":
                        stmnts.append(binop2("-", exp, k))

                    elif exp.operator == "Sqrt":
                        stmnts.append(callop1("sqrt", exp, k))

                    elif exp.operator == "Abs":
                        stmnts.append(callop1("abs", exp, k))

                    elif exp.operator == "Max":
                        stmnts.append(callop2("max", exp, k))

                    elif exp.operator == "Min":
                        stmnts.append(callop2("min", exp, k))

                    elif exp.operator == "Geq":
                        stmnts.append(comp(">=", exp, k))

                    elif exp.operator == "Leq":
                        stmnts.append(comp("<=", exp, k))

                    elif exp.operator == "Gt":
                        stmnts.append(comp(">", exp, k))

                    elif exp.operator == "Lt":
                        stmnts.append(comp("<", exp, k))

        return stmnts

    cases = []

    for i, b in enumerate(bindings):
        print("bindings")
        print(b)

        stmnts = statements(b)
        print(stmnts)

        idx = {}
        graph = {}
        for i, s in enumerate(stmnts):
            if s["defines"]:
                idx[s["defines"]] = i
                graph[s["defines"]] = set(s["depends"])

        order = toposort_flatten(graph)
        print(order)

        body = []
        added = set()
        for k in order:
            i = idx[k]
            body.append(stmnts[i]["set"])
            added.add(i)

        for i, stmnt in enumerate(stmnts):
            for d in stmnt["depends"]:
                if d not in order:
                    pass

        for i, stmnt in enumerate(stmnts):
            if i not in added:
                depends = stmnt["depends"]
                # # NOTE: Cheating
                # if all([x in order for x in depends]):
                body.append(stmnt["check"])

        body = "            ".join(body)
        case = f"        case {i}: {{\n{body}            result = min(result, ans);\n        }}"
        cases.append(case)

    case_statements = "\n".join(cases)
    switch_statement = f"        switch (i) {{\n{case_statements}\n        default: break;\n        }}\n"
    loop = f"    for(int i=0; i<{len(bindings)}; i++) {{\n{switch_statement}    }}\n"
    sdf_function = f"float sdf(vec3 p) {{\n    float result = 3.402823e+38;\n    float x = p.x;\n    float y = p.y;\n    float z = p.z;\n{loop}    return result;\n}}\n"
    return sdf_function


app = Flask(__name__)

print("compiling polar")
oso = Oso()
oso.load_file("scene.polar")

results = list(
    oso.query_rule("sdf", Variable("x"), Variable("y"), Variable("z"), Variable("ans"))
)
expressions = [result["bindings"] for result in results]
print("compiling glsl")
sdf_function = compile_sdf(expressions)
print(sdf_function)


@app.route("/")
def index():
    return render_template("app.html", sdf_function=sdf_function)