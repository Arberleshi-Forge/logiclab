from django.utils.translation import gettext as _
from django.shortcuts import render

from .complexity_engine import COMPLEXITY_CASES, get_complexity_case
from .recursion_engine import expression_tree_demo, factorial_iterative_trace, factorial_recursive_trace
from .sorting_engine import SortingInputError, parse_number_list, run_sorting_algorithm
from .theory_data import THEORY_TOPICS


def dashboard(request):
    return render(request, "algorithms/dashboard.html")


def complexity_view(request):
    selected_case = request.POST.get("case_key", "triangular_nested")
    case = get_complexity_case(selected_case)
    return render(
        request,
        "algorithms/complexity.html",
        {"case": case, "cases": COMPLEXITY_CASES, "selected_case": selected_case},
    )


def sorting_view(request):
    input_text = request.POST.get("numbers", "8, 4, 7, 3, 2, 6")
    selected_algorithm = request.POST.get("algorithm", "insertion")
    error = None
    result = None

    try:
        numbers = parse_number_list(input_text)
        result = run_sorting_algorithm(numbers, selected_algorithm)
    except SortingInputError as exc:
        error = str(exc)

    algorithms = {
        "insertion": "Insertion Sort",
        "selection": "Selection Sort",
        "quick": "Quick Sort",
        "merge": "Merge Sort",
    }
    comparison_rows = [
        ("Insertion Sort", "O(n)", "O(n^2)", "O(n^2)", _("Lista të vogla ose pothuajse të renditura")),
        ("Selection Sort", "O(n^2)", "O(n^2)", "O(n^2)", _("Pak ndërrime, por shumë krahasime")),
        ("Quick Sort", "O(n log n)", "O(n log n)", "O(n^2)", _("I shpejtë në praktikë me ndarje të mira")),
        ("Merge Sort", "O(n log n)", "O(n log n)", "O(n log n)", _("Performancë e qëndrueshme")),
    ]
    return render(
        request,
        "algorithms/sorting.html",
        {
            "input_text": input_text,
            "selected_algorithm": selected_algorithm,
            "algorithms": algorithms,
            "result": result,
            "error": error,
            "comparison_rows": comparison_rows,
        },
    )


def recursion_view(request):
    raw_n = request.POST.get("n", "5")
    error = None
    try:
        n = int(raw_n)
        if n < 1 or n > 10:
            raise ValueError
    except ValueError:
        n = 5
        error = _("Përdor një numër të plotë nga 1 deri në 10.")

    return render(
        request,
        "algorithms/recursion.html",
        {
            "n": n,
            "error": error,
            "recursive": factorial_recursive_trace(n),
            "iterative": factorial_iterative_trace(n),
            "expression_tree": expression_tree_demo(),
        },
    )


def theory_view(request):
    return render(request, "algorithms/theory.html", {"topics": THEORY_TOPICS})
