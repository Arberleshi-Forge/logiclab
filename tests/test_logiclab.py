from unittest.mock import patch
import json

from django.conf import settings
from django.test import TestCase, SimpleTestCase, override_settings
from django.utils.translation import override
from sympy import Symbol, sympify

from analyzer.logic_engine import analyze_expression, LogicEngineError
from algorithms.sorting_engine import run_sorting_algorithm
from chatbot.ai_engine import _call_ollama


@override_settings(ALLOWED_HOSTS=["testserver"])
class LanguageTests(TestCase):
    paths = ["/", "/about/", "/analyzer/", "/history/", "/algorithms/",
             "/algorithms/sorting/", "/algorithms/recursion/", "/algorithms/complexity/",
             "/algorithms/theory/", "/chatbot/", "/uploads/"]

    def test_pages_support_both_languages(self):
        for language, expected in [("en", "Home"), ("sq", "Kryefaqja")]:
            for path in self.paths:
                with self.subTest(language=language, path=path):
                    response = self.client.get(path, HTTP_ACCEPT_LANGUAGE=language)
                    self.assertContains(response, expected)
                    self.assertContains(response, f'<html lang="{language}">')

    def test_cookie_overrides_browser_and_keeps_current_page(self):
        response = self.client.post("/i18n/setlang/", {"language": "sq", "next": "/algorithms/"})
        self.assertRedirects(response, "/algorithms/")
        self.assertContains(self.client.get("/", HTTP_ACCEPT_LANGUAGE="en"), "Kryefaqja")
        self.client.post("/i18n/setlang/", {"language": "en", "next": "/"})
        self.assertContains(self.client.get("/", HTTP_ACCEPT_LANGUAGE="sq"), "Home")

    def test_unrecognized_browser_language_falls_back_to_english(self):
        self.assertContains(self.client.get("/", HTTP_ACCEPT_LANGUAGE="ja"), "Home")

    def test_external_language_redirect_is_rejected(self):
        response = self.client.post("/i18n/setlang/", {"language": "en", "next": "https://example.com/"})
        self.assertEqual(response.url, "/")

    def test_language_post_requires_csrf(self):
        from django.test import Client
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post("/i18n/setlang/", {"language": "en"}).status_code, 403)

    def test_form_errors_and_saved_results_follow_language(self):
        self.client.post("/i18n/setlang/", {"language": "sq"})
        response = self.client.post("/analyzer/", {"expression": "A + B"})
        self.assertContains(response, "Sintaksa e shprehjes")
        self.client.post("/analyzer/", {"expression": "(A & B) | (~A & C)"})
        self.assertContains(self.client.get("/result/"), "Hyrje: A")
        self.client.post("/i18n/setlang/", {"language": "en"})
        self.assertContains(self.client.get("/result/"), "Input: A")
        self.assertContains(self.client.get("/history/"), "Contingency")
        self.assertContains(self.client.post("/analyzer/", {"expression": "A + B"}), "Invalid expression syntax")

    def test_imported_theory_and_complexity_are_not_frozen_in_one_language(self):
        for language, expected in [("en", "Triangular Nested Loops"), ("sq", "Cikle të folezuara trekëndore"), ("en", "Triangular Nested Loops")]:
            self.client.cookies.clear()
            self.assertContains(self.client.get("/algorithms/complexity/", HTTP_ACCEPT_LANGUAGE=language), expected)


class BooleanTests(SimpleTestCase):
    def test_sop_and_pos_match_truth_table(self):
        for expression in ["A | ~A", "A & ~A", "A & B", "A | B", "A ^ B", "(A & B) | (~A & C)"]:
            with self.subTest(expression=expression):
                result = analyze_expression(expression)
                for form in [result["sop"], result["pos"]]:
                    parsed = sympify(form)
                    for row in result["truth_table"]:
                        values = {Symbol(key): bool(value) for key, value in row["values"].items()}
                        self.assertEqual(bool(parsed if isinstance(parsed, bool) else parsed.subs(values)), bool(row["result"]))

    def test_calls_attributes_and_other_python_syntax_are_rejected(self):
        expressions = ["__import__('os').system('id')", "A.__class__", "A[0]", "A + B", "A ** B", "lambda: A", "[A]"]
        for expression in expressions:
            with self.subTest(expression=expression), self.assertRaises(LogicEngineError):
                analyze_expression(expression)

    def test_text_operators_preserve_results(self):
        self.assertEqual(analyze_expression("(A AND B) OR (NOT A AND C)")["truth_table"], analyze_expression("(A & B) | (~A & C)")["truth_table"])

    def test_variable_and_length_limits(self):
        for expression in ["A|B|C|D|E|F|G", "A" + " " * 301 + "|B"]:
            with self.assertRaises(LogicEngineError):
                analyze_expression(expression)

    def test_sort_traces_switch_language_without_changing_sorted_values(self):
        for algorithm in ["insertion", "selection", "quick", "merge"]:
            with override("en"):
                english = run_sorting_algorithm([3, 1, 2], algorithm)
            with override("sq"):
                albanian = run_sorting_algorithm([3, 1, 2], algorithm)
            self.assertEqual(english["sorted_list"], albanian["sorted_list"])
            self.assertNotEqual(english["steps"][0]["description"], albanian["steps"][0]["description"])

    def test_tutor_prompt_uses_selected_language(self):
        for language, expected in [("en", "Respond in English."), ("sq", "Respond in Albanian.")]:
            with override(language), patch("chatbot.ai_engine.urllib.request.urlopen") as urlopen:
                urlopen.return_value.__enter__.return_value.read.return_value = b'{"message":{"content":"answer"}}'
                self.assertEqual(_call_ollama("question"), "answer")
                payload = json.loads(urlopen.call_args.args[0].data)
                self.assertIn(expected, payload["messages"][0]["content"])
