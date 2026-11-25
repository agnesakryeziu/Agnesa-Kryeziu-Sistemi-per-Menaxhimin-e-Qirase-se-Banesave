document.addEventListener("DOMContentLoaded", function () {

    const gallery = document.querySelector("[data-gallery]");
    const dialog = document.querySelector("[data-gallery-dialog]");

    if (!gallery || !dialog) {
        return;
    }

    const mainImage = gallery.querySelector("[data-gallery-main]");
    const thumbnails = Array.from(
        gallery.querySelectorAll("[data-gallery-thumb]")
    );

    const prev = gallery.querySelector("[data-gallery-prev]");
    const next = gallery.querySelector("[data-gallery-next]");
    const expand = gallery.querySelector("[data-gallery-expand]");
    const caption = gallery.querySelector("[data-gallery-caption]");
    const count = gallery.querySelector("[data-gallery-count]");

    const largeImage = dialog.querySelector("[data-gallery-large]");
    const closeButton = dialog.querySelector("[data-gallery-close]");
    const dialogPrev = dialog.querySelector("[data-gallery-dialog-prev]");
    const dialogNext = dialog.querySelector("[data-gallery-dialog-next]");
    const dialogCount = dialog.querySelector("[data-gallery-dialog-count]");

    if (!mainImage || !largeImage) {
        return;
    }

    let photos = thumbnails.map(function (thumb) {
        return {
            src: thumb.dataset.image,
            alt: thumb.dataset.alt || "Fotografia e baneses",
            caption: thumb.dataset.caption || ""
        };
    });

    if (photos.length === 0) {
        photos = [{
            src: mainImage.src,
            alt: mainImage.alt,
            caption: caption ? caption.textContent.trim() : ""
        }];
    }

    let currentIndex = thumbnails.findIndex(function (thumb) {
        return thumb.classList.contains("active");
    });

    if (currentIndex < 0) {
        currentIndex = 0;
    }

    function showPhoto(index) {

        currentIndex = (
            index + photos.length
        ) % photos.length;

        const photo = photos[currentIndex];

        mainImage.src = photo.src;
        mainImage.alt = photo.alt;

        largeImage.src = photo.src;
        largeImage.alt = photo.alt;

        thumbnails.forEach(function (thumb, i) {

            const active = i === currentIndex;

            thumb.classList.toggle("active", active);
            thumb.setAttribute("aria-pressed", String(active));

        });

        if (caption) {
            caption.textContent = photo.caption;
        }

        const counter = `${currentIndex + 1} / ${photos.length}`;

        if (count) {
            count.textContent = counter;
        }

        if (dialogCount) {
            dialogCount.textContent = counter;
        }
    }

    thumbnails.forEach(function (thumb, index) {

        thumb.addEventListener("click", function () {
            showPhoto(index);
        });

    });

    if (prev) {
        prev.addEventListener("click", function () {
            showPhoto(currentIndex - 1);
        });
    }

    if (next) {
        next.addEventListener("click", function () {
            showPhoto(currentIndex + 1);
        });
    }

    if (dialogPrev) {
        dialogPrev.addEventListener("click", function () {
            showPhoto(currentIndex - 1);
        });
    }

    if (dialogNext) {
        dialogNext.addEventListener("click", function () {
            showPhoto(currentIndex + 1);
        });
    }

    if (expand) {

        expand.addEventListener("click", function () {

            showPhoto(currentIndex);

            if (!dialog.open) {
                dialog.showModal();
            }

        });

    }

    if (closeButton) {
        closeButton.addEventListener("click", function () {
            dialog.close();
        });
    }

    dialog.addEventListener("click", function (event) {

        if (event.target === dialog) {
            dialog.close();
        }

    });

    dialog.addEventListener("keydown", function (event) {

        if (event.key === "ArrowLeft") {
            event.preventDefault();
            showPhoto(currentIndex - 1);
        }

        if (event.key === "ArrowRight") {
            event.preventDefault();
            showPhoto(currentIndex + 1);
        }

    });

    [prev, next, dialogPrev, dialogNext].forEach(function (button) {

        if (button && photos.length <= 1) {
            button.hidden = true;
            button.style.display = "none";
        }

    });

    showPhoto(currentIndex);

});