from django.core.files.storage import default_storage
from django.shortcuts import render

from .forms import CircuitImageForm
from .image_analyzer import analyze_uploaded_image


def upload(request):
    uploaded_image = None

    if request.method == "POST":
        form = CircuitImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save(commit=False)
            uploaded_image.save()
            image_path = default_storage.path(uploaded_image.image.name)
            uploaded_image.ai_explanation = analyze_uploaded_image(image_path)
            uploaded_image.save(update_fields=["ai_explanation"])
    else:
        form = CircuitImageForm()

    return render(request, "uploads/upload.html", {"form": form, "uploaded_image": uploaded_image})
