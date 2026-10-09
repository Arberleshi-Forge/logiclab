from django.utils.translation import gettext as _
class SortingInputError(ValueError):
    """Gabim i kontrolluar për listën hyrëse të renditjes."""


def parse_number_list(input_text):
    if not input_text or not input_text.strip():
        raise SortingInputError(_("Shkruaj të paktën një numër për renditje."))

    try:
        numbers = [int(part.strip()) for part in input_text.split(",") if part.strip()]
    except ValueError as exc:
        raise SortingInputError(_("Lista duhet të përmbajë vetëm numra të ndarë me presje.")) from exc

    if not numbers:
        raise SortingInputError(_("Lista duhet të përmbajë të paktën një numër."))
    if len(numbers) > 12:
        raise SortingInputError(_("Përdor maksimumi 12 numra që hapat të mbeten të lexueshëm."))
    return numbers


def _result(original, numbers, steps, comparisons, swaps, shifts, best, average, worst, explanation):
    return {
        "original_list": original,
        "sorted_list": numbers,
        "steps": steps,
        "comparisons": comparisons,
        "swaps": swaps,
        "shifts": shifts,
        "best_case": best,
        "average_case": average,
        "worst_case": worst,
        "explanation": explanation,
    }


def _add_step(steps, description, array):
    steps.append({"step": len(steps) + 1, "description": description, "array": array.copy()})


def insertion_sort_steps(numbers):
    original = numbers.copy()
    arr = numbers.copy()
    steps = []
    comparisons = 0
    shifts = 0

    _add_step(steps, _("Fillojmë me listën fillestare."), arr)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        _add_step(steps, f"{_('Zgjedhim elementin ')}{key}{_(' dhe kërkojmë pozicionin e duhur.')}", arr)

        # Insertion Sort zhvendos majtas elementet më të mëdha se çelësi.
        while j >= 0:
            comparisons += 1
            if arr[j] <= key:
                break
            arr[j + 1] = arr[j]
            shifts += 1
            _add_step(steps, f"{_('Zhvendosim ')}{arr[j]}{_(' një pozicion djathtas.')}", arr)
            j -= 1
        arr[j + 1] = key
        _add_step(steps, f"{_('Vendosim elementin ')}{key}{_(' në pozicionin e duhur.')}", arr)

    return _result(
        original,
        arr,
        steps,
        comparisons,
        swaps=0,
        shifts=shifts,
        best="O(n)",
        average="O(n^2)",
        worst="O(n^2)",
        explanation=_("Insertion Sort është efikas për lista të vogla ose pothuajse të renditura."),
    )


def selection_sort_steps(numbers):
    original = numbers.copy()
    arr = numbers.copy()
    steps = []
    comparisons = 0
    swaps = 0

    _add_step(steps, _("Fillojmë kërkimin e minimumit për çdo pozicion."), arr)
    for i in range(len(arr)):
        min_index = i
        for j in range(i + 1, len(arr)):
            comparisons += 1
            if arr[j] < arr[min_index]:
                min_index = j
        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            swaps += 1
            _add_step(steps, f"{_('Ndërrojmë minimumin ')}{arr[i]}{_(' me elementin në pozicionin ')}{i}.", arr)
        else:
            _add_step(steps, f"{_('Pozicioni ')}{i}{_(' është tashmë i saktë.')}", arr)

    return _result(
        original,
        arr,
        steps,
        comparisons,
        swaps=swaps,
        shifts=0,
        best="O(n^2)",
        average="O(n^2)",
        worst="O(n^2)",
        explanation=_("Selection Sort bën pak ndërrime, por gjithmonë kërkon minimumin në pjesën e parenditur."),
    )


def quick_sort_steps(numbers):
    original = numbers.copy()
    arr = numbers.copy()
    steps = []
    stats = {"comparisons": 0, "swaps": 0}

    def quicksort(low, high):
        if low >= high:
            return

        # Quick Sort përdor divide and conquer: zgjedh pivot, ndan listën dhe rendit pjesët rekursivisht.
        pivot = arr[high]
        _add_step(steps, f"{_('Zgjedhim pivotin ')}{pivot}{_(' për segmentin ')}{arr[low:high + 1]}.", arr)
        i = low - 1
        for j in range(low, high):
            stats["comparisons"] += 1
            if arr[j] <= pivot:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    stats["swaps"] += 1
                    _add_step(steps, f"{_('Vendosim ')}{arr[i]}{_(' në anën e majtë të pivotit.')}", arr)
        if i + 1 != high:
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            stats["swaps"] += 1
        pivot_index = i + 1
        _add_step(steps, f"{_('Pivot ')}{pivot}{_(' vendoset në pozicionin final ')}{pivot_index}.", arr)
        quicksort(low, pivot_index - 1)
        quicksort(pivot_index + 1, high)

    quicksort(0, len(arr) - 1)
    if not steps:
        _add_step(steps, _("Lista ka një element dhe është tashmë e renditur."), arr)

    return _result(
        original,
        arr,
        steps,
        stats["comparisons"],
        swaps=stats["swaps"],
        shifts=0,
        best="O(n log n)",
        average="O(n log n)",
        worst="O(n^2)",
        explanation=_("Quick Sort është algoritëm rekursiv divide and conquer; rasti më i keq ndodh kur ndarjet janë shumë të pabalancuara."),
    )


def merge_sort_steps(numbers):
    original = numbers.copy()
    arr = numbers.copy()
    steps = []
    stats = {"comparisons": 0}

    def merge_sort(values):
        if len(values) <= 1:
            return values

        # Merge Sort ndan listën në dy pjesë dhe i bashkon të renditura.
        middle = len(values) // 2
        left = merge_sort(values[:middle])
        right = merge_sort(values[middle:])
        _add_step(steps, f"{_('Ndahet lista në ')}{left}{_(' dhe ')}{right}{_(', pastaj bashkohet me rend.')}", arr)

        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            stats["comparisons"] += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    sorted_values = merge_sort(arr)
    _add_step(steps, _("Bashkimi final jep listën e renditur."), sorted_values)

    return _result(
        original,
        sorted_values,
        steps,
        stats["comparisons"],
        swaps=0,
        shifts=0,
        best="O(n log n)",
        average="O(n log n)",
        worst="O(n log n)",
        explanation=_("Merge Sort ka performancë të qëndrueshme sepse ndarja dhe bashkimi ruajnë kompleksitetin O(n log n)."),
    )


def run_sorting_algorithm(numbers, algorithm):
    algorithms = {
        "insertion": insertion_sort_steps,
        "selection": selection_sort_steps,
        "quick": quick_sort_steps,
        "merge": merge_sort_steps,
    }
    return algorithms.get(algorithm, insertion_sort_steps)(numbers)
