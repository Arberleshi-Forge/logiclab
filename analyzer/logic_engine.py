from django.utils.translation import gettext as _
import ast
import itertools
import re

from sympy import Symbol
from sympy.logic.boolalg import And, Or, Not, Xor, BooleanFalse, BooleanTrue, SOPform, POSform, simplify_logic

from .circuit_generator import generate_circuit_data


class LogicEngineError(Exception):
    """Gabim i kontrolluar për analizimin e shprehjeve Booleane."""


MAX_VARIABLES = 6
TOKEN_PATTERN = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
RESERVED_WORDS = {"AND", "OR", "NOT", "XOR", "TRUE", "FALSE"}


def normalize_expression(expression):
    if not expression or not expression.strip():
        raise LogicEngineError(_("Shkruaj një shprehje Booleane për analizim."))

    if len(expression) > 300:
        raise LogicEngineError(_("Përdor &, |, ~, ^ ose AND, OR, NOT, XOR. Maksimumi 6 variabla."))

    normalized = expression.strip()
    replacements = {
        r"\bAND\b": "&",
        r"\bOR\b": "|",
        r"\bNOT\b": "~",
        r"\bXOR\b": "^",
    }
    for pattern, replacement in replacements.items():
        normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)

    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def get_variable_names(expression):
    normalized = normalize_expression(expression)
    names = []

    for token in TOKEN_PATTERN.findall(normalized):
        if token.upper() in RESERVED_WORDS:
            continue
        if token not in names:
            names.append(token)

    if not names:
        raise LogicEngineError(_("Shprehja duhet të përmbajë të paktën një variabël."))
    if len(names) > MAX_VARIABLES:
        raise LogicEngineError(_("Maksimumi i lejuar është 6 variabla që tabela të mbetet e lexueshme."))

    return sorted(names, key=str.lower)


def parse_boolean_expression(expression):
    normalized = normalize_expression(expression)
    variable_names = get_variable_names(normalized)
    if len(normalized) > 300:
        raise LogicEngineError(_("Përdor &, |, ~, ^ ose AND, OR, NOT, XOR. Maksimumi 6 variabla."))

    def convert(node):
        if isinstance(node, ast.Name) and node.id in variable_names:
            return Symbol(node.id)
        if isinstance(node, ast.Name) and node.id.lower() in ("true", "false"):
            return BooleanTrue() if node.id.lower() == "true" else BooleanFalse()
        if isinstance(node, ast.Constant) and type(node.value) is bool:
            return BooleanTrue() if node.value else BooleanFalse()
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Invert):
            return Not(convert(node.operand))
        if isinstance(node, ast.BinOp):
            operations = {ast.BitAnd: And, ast.BitOr: Or, ast.BitXor: Xor}
            operation = operations.get(type(node.op))
            if operation:
                return operation(convert(node.left), convert(node.right))
        raise ValueError("Unsupported Boolean syntax")

    try:
        return convert(ast.parse(normalized, mode="eval").body)
    except (SyntaxError, ValueError, TypeError, RecursionError) as exc:
        raise LogicEngineError(_("Sintaksa e shprehjes nuk është e vlefshme. Kontrollo operatorët dhe kllapat.")) from exc


def _bool_to_int(value):
    return 1 if bool(value) else 0


def generate_truth_table(expression):
    parsed = parse_boolean_expression(expression)
    variable_names = get_variable_names(expression)
    symbols = [Symbol(name) for name in variable_names]
    rows = []

    # Gjenerojmë çdo kombinim të mundshëm 0/1 për variablat e gjetura.
    for values in itertools.product([False, True], repeat=len(symbols)):
        assignment = dict(zip(symbols, values))
        result = parsed.subs(assignment)
        rows.append(
            {
                "values": {str(symbol): _bool_to_int(value) for symbol, value in assignment.items()},
                "result": _bool_to_int(result),
            }
        )

    return rows


def simplify_boolean_expression(expression):
    parsed = parse_boolean_expression(expression)
    try:
        simplified = simplify_logic(parsed, form="dnf", force=True)
    except Exception as exc:
        raise LogicEngineError(_("Shprehja nuk mund të thjeshtohet për shkak të sintaksës së pavlefshme.")) from exc
    return str(simplified)


def get_canonical_forms(expression):
    parsed = parse_boolean_expression(expression)
    variable_names = get_variable_names(expression)
    symbols = [Symbol(name) for name in variable_names]
    minterms = []
    maxterms = []

    # Mintermat dhe maxtermat nxirren nga tabela e së vërtetës.
    for bits in itertools.product([0, 1], repeat=len(symbols)):
        assignment = {symbol: bool(bit) for symbol, bit in zip(symbols, bits)}
        value = bool(parsed.subs(assignment))
        if value:
            minterms.append(list(bits))
        else:
            maxterms.append(list(bits))

    try:
        sop = SOPform(symbols, minterms) if minterms else BooleanFalse()
        pos = POSform(symbols, minterms) if minterms else BooleanFalse()
    except Exception as exc:
        raise LogicEngineError(_("Nuk u arrit të gjenerohen format kanonike SOP/POS.")) from exc

    return {"sop": str(sop), "pos": str(pos), "minterms": minterms, "maxterms": maxterms}


def classify_expression(expression):
    table = generate_truth_table(expression)
    results = [row["result"] for row in table]
    if all(value == 1 for value in results):
        return _("Tautologji")
    if all(value == 0 for value in results):
        return _("Kontradiktë")
    return _("Kontingjencë")


def analyze_expression(expression):
    normalized = normalize_expression(expression)
    parsed = parse_boolean_expression(normalized)
    variables = get_variable_names(normalized)
    truth_table = generate_truth_table(normalized)
    canonical = get_canonical_forms(normalized)
    circuit_data = generate_circuit_data(parsed)
    algorithm_analysis = {
        "variable_count": len(variables),
        "combination_count": 2 ** len(variables),
        "time_complexity": "O(2^n)",
        "space_complexity": "O(2^n)",
        "explanation": (
            _("Për çdo variabël shtohet një ndarje e re midis 0 dhe 1. Për këtë arsye, me n variabla kemi 2^n kombinime të mundshme.")
        ),
    }

    explanation = (
        _("Kjo shprehje përfaqëson një qark kombinacional. Nëse A është 1, dalja ndikohet nga B; nëse A është 0, dalja ndikohet nga C. Ky model i ngjan logjikës së një multiplekseri 2-me-1.")
        if normalized.replace(" ", "") == "(A&B)|(~A&C)"
        else _("Kjo shprehje përfaqëson një qark kombinacional ku dalja F përcaktohet nga kombinimi i hyrjeve.")
    )

    return {
        "original_expression": expression,
        "normalized_expression": normalized,
        "parsed_expression": parsed,
        "variables": variables,
        "truth_table": truth_table,
        "simplified_expression": simplify_boolean_expression(normalized),
        "sop": canonical["sop"],
        "pos": canonical["pos"],
        "expression_type": classify_expression(normalized),
        "gate_count": circuit_data["gate_count"],
        "circuit_steps": circuit_data["steps"],
        "dot_source": circuit_data["dot_source"],
        "explanation": explanation,
        "algorithm_analysis": algorithm_analysis,
    }
