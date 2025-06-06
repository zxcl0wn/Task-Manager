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

// alert("Привет");
