function scrollTasks(direction) {
    const container = document.getElementById("tasksContainer");
    const card = container.querySelector(".task-card");
    if (!card) return;

    const scrollAmount =
        card.offsetWidth + parseInt(getComputedStyle(container).gap || 56);
    container.scrollBy({
        left: direction * scrollAmount,
        behavior: "smooth",
    });
}
function scrollProjects(direction) {
    const container = document.getElementById('projectsContainer');
    const scrollAmount = 300; // пикселей за один клик
    container.scrollBy({
        left: direction * scrollAmount,
        behavior: 'smooth'
    });
}
// alert("Привет");

document.addEventListener("DOMContentLoaded", function() {
    let form = document.getElementById('filter-form');
    const radios = form.querySelectorAll('input[type="radio"]');
    radios.forEach(radio => {
        radio.addEventListener('change', () => {
            form.submit();
        });
    });
});
