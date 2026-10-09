from django.utils.translation import gettext as _
def factorial_recursive_trace(n):
    steps = []

    def factorial(value):
        steps.append(f"{_('Thirrje rekursive: factorial(')}{value})")
        if value <= 1:
            steps.append(_("Rasti bazë: factorial(1) = 1"))
            return 1
        result = value * factorial(value - 1)
        steps.append(f"{_('Kthehemi nga rekursioni: factorial(')}{value}) = {value} * factorial({value - 1}) = {result}")
        return result

    result = factorial(n)
    return {
        "result": result,
        "calls_count": len([step for step in steps if step.startswith("Thirrje")]),
        "steps": steps,
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "explanation": _("Versioni rekursiv përdor stack thirrjesh, prandaj kërkon hapësirë O(n)."),
    }


def factorial_iterative_trace(n):
    result = 1
    steps = []
    for value in range(1, n + 1):
        result *= value
        steps.append(f"{_('Iterimi ')}{value}{_(': shumëzojmë rezultatin me ')}{value}{_(', rezultati bëhet ')}{result}.")

    return {
        "result": result,
        "iterations_count": n,
        "steps": steps,
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "explanation": _("Versioni iterativ përdor një variabël akumuluese, prandaj hapësira mbetet konstante."),
    }


def expression_tree_demo():
    return {
        "expression": "(A & B) | (~A & C)",
        "tree": """OR
├── AND
│   ├── A
│   └── B
└── AND
    ├── NOT
    │   └── A
    └── C""",
        "explanation": (
            _("Në LogicLab, shprehjet Booleane mund të përfaqësohen si pemë. Për të gjeneruar hapat e qarkut, sistemi mund ta përshkojë këtë pemë në mënyrë rekursive.")
        ),
    }
