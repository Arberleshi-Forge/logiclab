from django.utils.translation import gettext as _
from sympy import Symbol
from sympy.logic.boolalg import And, Not, Or, Xor


def count_gates_from_expression(parsed_expression):
    counts = {"NOT": 0, "AND": 0, "OR": 0, "XOR": 0}

    def walk(node):
        if isinstance(node, Not):
            counts["NOT"] += 1
        elif isinstance(node, And):
            counts["AND"] += 1
        elif isinstance(node, Or):
            counts["OR"] += 1
        elif isinstance(node, Xor):
            counts["XOR"] += 1

        for arg in getattr(node, "args", []):
            walk(arg)

    walk(parsed_expression)
    return counts


def generate_circuit_steps(expression):
    steps = []

    def walk(node):
        if isinstance(node, Symbol):
            label = f"{_('Hyrje: ')}{node}"
            steps.append(label)
            return str(node)

        if isinstance(node, Not):
            child = walk(node.args[0])
            label = f"{_('Portë NOT mbi ')}{child}"
            steps.append(label)
            return f"~({child})"

        if isinstance(node, And):
            inputs = [walk(arg) for arg in node.args]
            label = f"{_('Portë AND që bashkon ')}{_(' dhe ').join(inputs)}"
            steps.append(label)
            return f"({' & '.join(inputs)})"

        if isinstance(node, Or):
            inputs = [walk(arg) for arg in node.args]
            label = f"{_('Portë OR që bashkon ')}{_(' dhe ').join(inputs)}"
            steps.append(label)
            return f"({' | '.join(inputs)})"

        if isinstance(node, Xor):
            inputs = [walk(arg) for arg in node.args]
            label = f"{_('Portë XOR që bashkon ')}{_(' dhe ').join(inputs)}"
            steps.append(label)
            return f"({' ^ '.join(inputs)})"

        return str(node)

    # Leximi rekursiv prodhon hapat nga hyrjet drejt daljes finale F.
    walk(expression)
    steps.append(_("Portë dalëse për rezultatin final F"))
    return steps


def generate_dot_source(expression):
    lines = [
        "digraph LogicLab {",
        "  rankdir=LR;",
        "  node [shape=box, style=rounded];",
    ]
    counter = {"value": 0}

    def next_id(prefix):
        counter["value"] += 1
        return f"{prefix}_{counter['value']}"

    def walk(node):
        if isinstance(node, Symbol):
            node_id = next_id("in")
            lines.append(f'  {node_id} [label="{node}", shape=circle];')
            return node_id

        gate_name = None
        if isinstance(node, Not):
            gate_name = "NOT"
        elif isinstance(node, And):
            gate_name = "AND"
        elif isinstance(node, Or):
            gate_name = "OR"
        elif isinstance(node, Xor):
            gate_name = "XOR"

        if gate_name:
            gate_id = next_id(gate_name.lower())
            lines.append(f'  {gate_id} [label="{gate_name}"];')
            for arg in node.args:
                child_id = walk(arg)
                lines.append(f"  {child_id} -> {gate_id};")
            return gate_id

        fallback_id = next_id("expr")
        lines.append(f'  {fallback_id} [label="{node}"];')
        return fallback_id

    final_node = walk(expression)
    lines.append('  F [label="F", shape=doublecircle];')
    lines.append(f"  {final_node} -> F;")
    lines.append("}")
    return "\n".join(lines)


def generate_circuit_data(expression):
    return {
        "gate_count": count_gates_from_expression(expression),
        "steps": generate_circuit_steps(expression),
        "dot_source": generate_dot_source(expression),
    }
