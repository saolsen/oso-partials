from dataclasses import dataclass
from oso import Oso
from polar import Variable

oso = Oso()

oso.load_file("hello.polar")

results = list(oso.query_rule("sdf", Variable("x"), Variable("y"), Variable("z"), Variable("ans")))
ans = [result['bindings']['ans'] for result in results]

print(ans)
print(len(ans))