document.addEventListener("DOMContentLoaded", function () {
    const gallery = document.querySelector("[data-gallery]");

    if (!gallery) {
        return;
    }

    const mainImage = gallery.querySelector("[data-gallery-main]");
    const caption = gallery.querySelector("[data-gallery-caption]");
    const counter = gallery.querySelector("[data-gallery-count]");
    const thumbnails = Array.from(
        gallery.querySelectorAll("[data-gallery-thumb]")
    );

    const previousButton = gallery.querySelector("[data-gallery-prev]");
    const nextButton = gallery.querySelector("[data-gallery-next]");
    const expandButton = gallery.querySelector("[data-gallery-expand]");

    const dialog = document.querySelector("[data-gallery-dialog]");
    const largeImage = dialog?.querySelector("[data-gallery-large]");
    const closeButton = dialog?.querySelector("[data-gallery-close]");

    let currentIndex = 0;

    if (thumbnails.length === 0) {
        previousButton.hidden = true;
        nextButton.hidden = true;
        expandButton.hidden = true;
        return;
    }

    if (thumbnails.length === 1) {
        previousButton.hidden = true;
        nextButton.hidden = true;
    }

    function showPhoto(index) {
        currentIndex = (
            index + thumbnails.length
        ) % thumbnails.length;

        const selected = thumbnails[currentIndex];
        const imageUrl = selected.dataset.image;
        const imageAlt = selected.dataset.alt;
        const imageCaption = selected.dataset.caption;

        mainImage.src = imageUrl;
        mainImage.alt = imageAlt;

        caption.textContent = imageCaption;
        counter.textContent = `${currentIndex + 1} / ${thumbnails.length}`;

        thumbnails.forEach(function (thumbnail, position) {
            const active = position === currentIndex;

            thumbnail.classList.toggle("active", active);
            thumbnail.setAttribute("aria-pressed", String(active));
        });

        selected.scrollIntoView({
            behavior: "smooth",
            block: "nearest",
            inline: "nearest"
        });

        if (dialog?.open && largeImage) {
            largeImage.src = imageUrl;
            largeImage.alt = imageAlt;
        }
    }

    thumbnails.forEach(function (thumbnail, index) {
        thumbnail.addEventListener("click", function () {
            showPhoto(index);
        });
    });

    previousButton.addEventListener("click", function () {
        showPhoto(currentIndex - 1);
    });

    nextButton.addEventListener("click", function () {
        showPhoto(currentIndex + 1);
    });

    expandButton.addEventListener("click", function () {
        if (!dialog || !largeImage) {
            return;
        }

        if (typeof dialog.showModal !== "function") {
            return;
        }

        largeImage.src = mainImage.src;
        largeImage.alt = mainImage.alt;
        dialog.showModal();
    });

    closeButton?.addEventListener("click", function () {
        dialog.close();
    });

    dialog?.addEventListener("click", function (event) {
        if (event.target === dialog) {
            dialog.close();
        }
    });

    document.addEventListener("keydown", function (event) {
        if (!dialog?.open) {
            return;
        }

        if (event.key === "ArrowLeft") {
            showPhoto(currentIndex - 1);
        }

        if (event.key === "ArrowRight") {
            showPhoto(currentIndex + 1);
        }
    });

    showPhoto(0);
});
