from django.utils.translation import gettext as _
import base64
from io import BytesIO
import json
import urllib.error
import urllib.request
from pathlib import Path

from django.conf import settings
from django.utils.translation import get_language
from PIL import Image, ImageOps, UnidentifiedImageError


class OllamaConnectionError(Exception):
    """Gabim kur shërbimi lokal Ollama nuk përgjigjet."""


SYSTEM_PROMPT = """
You are a professional AI tutor for LogicLab, a university platform connecting Discrete Mathematics, Digital Logic, and Algorithms with Advanced Programming.
Your scope is strictly limited to:
- digital logic, discrete mathematics, Boolean algebra, truth tables, SOP/POS, simplification, and logic-gate circuits;
- algorithm analysis, Big O, Big Theta, Big Omega, nested loops, recursion, iteration, sorting, divide and conquer, greedy algorithms, dynamic programming, linked lists, and binary search.
Be concise, structured, and practical.
If the question or image is outside these topics, say that you can only help with LogicLab-related academic topics and ask for a course-related question.
When analyzing algorithms or pseudocode:
- identify the main structure: loops, recursion, divide and conquer, greedy choice, or memoization;
- explain the operation count using simple reasoning;
- give Big O, Big Theta, and Big Omega when they are well-defined;
- mention space complexity when the algorithm uses recursion stack, auxiliary arrays, or cache;
- connect the answer to LogicLab when relevant, for example truth-table generation is O(2^n).
When analyzing circuit images:
- identify only elements that are clearly visible: inputs, gates, wires, and outputs;
- propose a Boolean function only when the connections are readable;
- explain the relation to truth tables, SOP/POS, and simplification;
- do not invent details that are not visible in the image.
""".strip()


def generate_logic_explanation(user_question, context=None, image_path=None):
    response = generate_logic_response(user_question, context=context, image_path=image_path)
    return response["answer"]


def generate_logic_response(user_question, context=None, image_path=None):
    prompt = _build_user_prompt(user_question, context, bool(image_path))

    try:
        return {"answer": _call_ollama(prompt, image_path=image_path), "used_ollama": True}
    except OllamaConnectionError:
        return {"answer": _fallback_response(user_question, has_image=bool(image_path)), "used_ollama": False}


def analyze_logic_image(image_path, user_question="Analyze this logic circuit image."):
    return generate_logic_explanation(user_question=user_question, image_path=image_path)


def _build_user_prompt(user_question, context, has_image):
    question = (user_question or "").strip()
    if not question and has_image:
        question = "Analyze the logic circuit image and explain the gates, inputs, output, and possible Boolean function."
    elif not question:
        question = "Explain a concept from Boolean logic or algorithm analysis."

    context_text = f"\nContext from LogicLab:\n{context}" if context else ""
    image_text = "\nUse the attached image in the analysis." if has_image else ""
    algorithm_hint = ""
    if _looks_like_algorithm_question(question):
        algorithm_hint = (
            "\nAnalyze this as an Advanced Algorithms and Programming problem. "
            "Give the algorithm structure, time complexity, space complexity, and a short justification."
        )
    return f"{question}{context_text}{image_text}{algorithm_hint}"


def _looks_like_algorithm_question(question):
    lowered = question.lower()
    keywords = (
        "algorit", "big o", "big-o", "theta", "omega", "kompleksitet", "complexity",
        "for ", "while ", "rekursion", "recursive", "iteracion", "sort", "rendit",
        "quick", "merge", "insertion", "selection", "greedy", "dynamic", "programming",
        "divide", "conquer", "linked list", "binary search", "memoization",
    )
    return any(keyword in lowered for keyword in keywords)


def _call_ollama(prompt, image_path=None):
    try:
        payload = {
            "model": settings.OLLAMA_MODEL,
            "stream": False,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT + "\nRespond in " + ("Albanian." if get_language() == "sq" else "English.")},
                _user_message(prompt, image_path),
            ],
            "options": {
                "temperature": 0.1,
                "top_p": 0.85,
                "num_ctx": settings.OLLAMA_NUM_CTX,
                "num_predict": settings.OLLAMA_NUM_PREDICT,
            },
        }
    except OSError as exc:
        raise OllamaConnectionError(str(exc)) from exc

    request = urllib.request.Request(
        f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=settings.OLLAMA_TIMEOUT) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise OllamaConnectionError(str(exc)) from exc

    message = data.get("message", {})
    content = (message.get("content") or "").strip()
    if not content:
        raise OllamaConnectionError(_("Ollama ktheu përgjigje bosh."))
    return content


def _user_message(prompt, image_path=None):
    message = {"role": "user", "content": prompt}
    if image_path:
        message["images"] = [_encode_image(image_path)]
    return message


def _encode_image(image_path):
    path = Path(image_path)
    try:
        with Image.open(path) as image:
            image = ImageOps.exif_transpose(image)
            image.thumbnail(
                (settings.OLLAMA_IMAGE_MAX_SIDE, settings.OLLAMA_IMAGE_MAX_SIDE),
                Image.Resampling.LANCZOS,
            )

            if image.mode not in ("RGB", "L"):
                image = image.convert("RGB")

            buffer = BytesIO()
            image.save(buffer, format="JPEG", quality=85, optimize=True)
            return base64.b64encode(buffer.getvalue()).decode("utf-8")
    except UnidentifiedImageError as exc:
        raise OSError(_("Imazhi nuk mund të lexohet.")) from exc


def _fallback_response(user_question, has_image=False):
    question = (user_question or "").lower()

    if has_image:
        return (
            _("Ollama is not reachable right now, so this is a demo response. The image was accepted by the system. With a vision-capable Ollama model, this module can identify inputs, gates, outputs, and propose a possible Boolean function for the circuit.")
        )
    if "truth table" in question or "tabela" in question:
        return _("A truth table lists every input combination and the corresponding output. For n variables, it contains 2^n rows.")
    if "simplification" in question or "thjeshtim" in question:
        return _("Boolean simplification reduces an expression without changing its logical function, often reducing the number of gates.")
    if "circuit" in question or "qark" in question:
        return _("A combinational circuit is built by connecting NOT, AND, OR, and XOR gates according to the Boolean expression structure.")
    if "boolean" in question:
        return _("Boolean algebra works with the values 0 and 1 and is a foundation of digital logic.")
    if "de morgan" in question or "morgan" in question:
        return _("De Morgan's laws transform NOT over AND into OR of negated inputs, and NOT over OR into AND of negated inputs.")
    if "truth table" in question or "tabel" in question or "2^n" in question:
        return _("Truth-table generation has time complexity O(2^n), because n Boolean variables produce 2^n possible 0/1 combinations.")
    if "big o" in question or "kompleksitet" in question or "complexity" in question:
        return _("For algorithm analysis, identify loops or recursion, find the dominant term, and express it with Big O, Big \u0398, and Big \u03a9. For example, two nested loops usually give \u0398(n^2).")
    if "rekursion" in question or "recursive" in question:
        return _("Recursion solves a problem by calling itself on smaller inputs. Time often depends on the number of calls, while space includes the recursion stack.")
    if "quick" in question or "merge" in question or "sort" in question or "rendit" in question:
        return _("Sorting algorithms are compared by best, average, and worst cases. Merge Sort is O(n log n) in all cases, while Quick Sort is O(n log n) on average but O(n^2) in the worst case.")
    if "greedy" in question:
        return _("A greedy algorithm makes the best local choice at each step. It works when local optimal choices lead to a globally optimal solution.")
    if "dynamic" in question or "programming" in question or "memoization" in question:
        return _("Dynamic Programming stores subproblem results to avoid repeated work. Memoization is the top-down version of this idea.")

    return (
        _("This is the Tutor AI demo fallback. For professional analysis, start Ollama and ask about Boolean logic, digital circuits, or algorithm analysis.")
    )
