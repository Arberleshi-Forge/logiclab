# LogicLab

A collaborative university web application connecting discrete mathematics, digital logic, algorithms and web development. Explore Boolean expressions, truth tables, logic circuits and algorithm traces through an interface available in **English and Albanian**.

## Explore the application

- **Boolean analyzer:** normalize expressions, enumerate truth tables, simplify logic, calculate SOP/POS forms and classify expressions.
- **Circuit explorer:** inspect gate counts, recursive construction steps and generated Graphviz DOT source.
- **Algorithm lab:** visualize Insertion, Selection, Quick and Merge Sort; compare recursive and iterative factorial calculations; study selected complexity examples.
- **AI Tutor:** integrate a locally hosted Ollama model for academic questions and circuit images. This is an integration with an existing model, not a model trained by the project team.
- **Language selection:** switch between SQ and EN. Your choice is remembered; the browser language is used initially, with English as the fallback.

## Run locally

Python 3.9 or newer is required for the currently verified dependency set. A virtual environment is recommended.

```sh
git clone https://github.com/Arberleshi-Forge/logiclab.git
cd logiclab
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Open **http://127.0.0.1:8000/**. On Windows, activate with `.venv\Scripts\activate` instead. SQLite is created locally by migrations; no existing user database or uploaded media is included.

### Optional AI Tutor

Install Ollama from its official website and obtain a compatible model:

```sh
ollama pull granite3.2-vision:2b
ollama serve
```

If Ollama is already running, a second `ollama serve` is unnecessary. Settings are documented in `.env.example`. Without Ollama, the site still runs and the tutor displays clearly labeled predefined fallback responses; these do not analyze an uploaded image. Model-generated responses are not guaranteed to be correct or to follow every instruction.

## Technology and structure

Python · Django · SymPy · SQLite · HTML · CSS · JavaScript · Bootstrap · Ollama

```text
logiclab/       Django settings, root URLs and WSGI entry point
analyzer/       Boolean analysis and circuit construction
algorithms/     Sorting, recursion, complexity examples and theory
chatbot/        Ollama integration and optional image input
uploads/        Circuit image uploads
locale/         English and Albanian translation catalogs
static/         Styles and browser scripts
templates/      Server-rendered pages
tests/          Language, Boolean correctness and parser regression tests
```

Computation modules are separated from Django views and templates. The Boolean parser accepts a restricted grammar: variables, TRUE/FALSE, parentheses and AND/OR/NOT/XOR (`&`, `|`, `~`, `^`). Python calls, attributes and arithmetic are rejected. Expressions are limited to 300 characters and six variables.

## Verification

```sh
python manage.py check
python manage.py test tests
```

Translation sources and compiled catalogs are included. After changing messages, use Django's `makemessages` and `compilemessages` commands with GNU gettext installed. Both language catalogs are maintained explicitly because the original message IDs are Albanian and the default UI fallback is English. See [Django's translation documentation](https://docs.djangoproject.com/en/4.2/topics/i18n/translation/).

## Project background

Created collaboratively by a university student group, including Arbër Leshi, as an interdisciplinary coursework project. Development used AI-assisted tools; the repository does not attribute all implementation to one person. Original academic documentation is in [DOKUMENTIM_AKADEMIK.md](DOKUMENTIM_AKADEMIK.md).

## Hosting status

This repository provides source code and local setup instructions. **A public application deployment is not yet configured.** GitHub Pages cannot run this Django backend.

Before exposing a live service, configure supported Python/Django versions, environment-based secrets, DEBUG=False, explicit hosts and HTTPS, production static/media handling, persistent storage, upload limits and abuse controls. Analysis history is currently shared across visitors; decide its intended privacy behavior before launch. Ollama needs its own reachable service and sufficient resources. These deployment requirements have not been production-verified.

Local `.env`, SQLite databases, uploaded images, virtual environments and IDE files are excluded from version control. No open-source license has been selected by the contributors.
