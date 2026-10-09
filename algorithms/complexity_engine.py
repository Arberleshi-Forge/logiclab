from django.utils.translation import gettext_lazy as _
COMPLEXITY_CASES = {
    "triangular_nested": {
        "title": _("Cikle të folezuara trekëndore"),
        "pseudocode": """for i = 1 to n:
    for j = 1 to i:
        for k = 1 to j:
            sum = sum + 1""",
        "explanation": (
            _("Ky algoritëm numëron kombinime të varura nga i dhe j. Numri total i operacioneve është proporcional me n(n+1)(n+2)/6, prandaj termi dominues është n^3.")
        ),
        "big_o": "O(n^3)",
        "big_theta": "Θ(n^3)",
        "big_omega": "Ω(n^3)",
        "efficiency_note": _("Rritja kubike bëhet shpejt e kushtueshme kur n rritet."),
    },
    "double_plus_linear": {
        "title": _("Cikle të dyfishta + cikël linear"),
        "pseudocode": """for i = 1 to n:
    for j = 1 to n:
        sum = sum + i * j

for k = 1 to n:
    sum = sum + k""",
        "explanation": (
            _("Pjesa e parë ka kompleksitet Θ(n^2), ndërsa pjesa e dytë ka kompleksitet Θ(n). Në analizën asimptotike ruhet termi dominues, prandaj kompleksiteti total është Θ(n^2).")
        ),
        "big_o": "O(n^2)",
        "big_theta": "Θ(n^2)",
        "big_omega": "Ω(n^2)",
        "efficiency_note": _("Cikli linear nuk e ndryshon klasën e kompleksitetit kur ekziston një pjesë kuadratike."),
    },
    "truth_table": {
        "title": _("Truth Table Generator në LogicLab"),
        "pseudocode": """for each combination in 2^n:
    evaluate boolean expression""",
        "explanation": (
            _("Për n variabla ekzistojnë 2^n kombinime të mundshme 0/1. Prandaj gjenerimi i tabelës së së vërtetës ka rritje eksponenciale.")
        ),
        "big_o": "O(2^n)",
        "big_theta": "Θ(2^n)",
        "big_omega": "Ω(2^n)",
        "efficiency_note": _("Ky është kufizimi kryesor pse LogicLab e mban tabelën të lexueshme për numër të kufizuar variablash."),
    },
}


def get_complexity_case(case_key):
    return COMPLEXITY_CASES.get(case_key, COMPLEXITY_CASES["triangular_nested"])
