from django.utils.translation import gettext as _
from pathlib import Path

from chatbot.ai_engine import analyze_logic_image


def analyze_uploaded_image(image_path):
    path = Path(image_path)
    prompt = (
        "Analyze this logic circuit image in professional English. Describe the inputs, gates, wires, output, "
        "and the possible Boolean function. If the image is unclear, state which parts are missing."
    )

    if path.exists():
        return analyze_logic_image(str(path), prompt)

    return (
        _("Imazhi u ruajt, por rruga lokale nuk u gjet për analizë automatike. Kontrollo konfigurimin e MEDIA_ROOT dhe provo përsëri.")
    )
