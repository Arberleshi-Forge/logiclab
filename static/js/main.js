document.addEventListener("DOMContentLoaded", function () {
    const tooltips = document.querySelectorAll("[data-bs-toggle='tooltip']");
    tooltips.forEach((item) => new bootstrap.Tooltip(item));
});
