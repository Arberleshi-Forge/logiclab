from django.core.files.storage import default_storage
from django.shortcuts import render

from .ai_engine import generate_logic_response
from .forms import ChatbotForm


def chatbot(request):
    answer = None
    question = ""
    uploaded_image_url = None
    used_ollama = False

    if request.method == "POST":
        form = ChatbotForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.cleaned_data.get("question", "").strip()
            image = form.cleaned_data.get("image")
            image_path = None

            if image:
                # Imazhi ruhet në media/chatbot_images që modeli vizual i Ollama ta lexojë si base64.
                saved_path = default_storage.save(f"chatbot_images/{image.name}", image)
                image_path = default_storage.path(saved_path)
                uploaded_image_url = default_storage.url(saved_path)

            response = generate_logic_response(question, image_path=image_path)
            answer = response["answer"]
            used_ollama = response["used_ollama"]
            form = ChatbotForm()
    else:
        form = ChatbotForm()

    return render(
        request,
        "chatbot/chatbot.html",
        {
            "form": form,
            "question": question,
            "answer": answer,
            "uploaded_image_url": uploaded_image_url,
            "used_ollama": used_ollama,
        },
    )
