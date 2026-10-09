from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from .forms import BooleanExpressionForm
from .logic_engine import LogicEngineError, analyze_expression
from .models import BooleanExpression


def home(request):
    return render(request, "home.html")


def analyzer(request):
    form = BooleanExpressionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        expression = form.cleaned_data["expression"]
        try:
            analysis = analyze_expression(expression)
            BooleanExpression.objects.create(
                original_expression=analysis["original_expression"],
                normalized_expression=analysis["normalized_expression"],
                simplified_expression=analysis["simplified_expression"],
                variables=", ".join(analysis["variables"]),
                expression_type=_canonical_type(analysis["expression_type"]),
                gate_count=analysis["gate_count"],
            )
            request.session["last_analysis"] = _serialize_analysis(analysis)
            return redirect("result")
        except LogicEngineError as exc:
            form.add_error("expression", str(exc))

    return render(request, "analyzer/analyzer.html", {"form": form})


def result(request):
    analysis = request.session.get("last_analysis")
    if not analysis:
        return redirect("analyzer")
    try:
        analysis = _serialize_analysis(analyze_expression(analysis["original_expression"]))
    except (KeyError, LogicEngineError):
        return redirect("analyzer")
    return render(request, "analyzer/result.html", {"analysis": analysis})


def history(request):
    expressions = BooleanExpression.objects.all()[:50]
    for expression in expressions:
        expression.expression_type = _(_canonical_type(expression.expression_type))
    return render(request, "analyzer/history.html", {"expressions": expressions})


def about(request):
    return render(request, "about.html")


def _serialize_analysis(analysis):
    data = analysis.copy()
    data.pop("parsed_expression", None)
    return data


def _canonical_type(value):
    return {"Tautology": "Tautologji", "Contradiction": "Kontradiktë", "Contingency": "Kontingjencë"}.get(value, value)
