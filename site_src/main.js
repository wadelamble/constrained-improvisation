const lightbox = document.querySelector("[data-lightbox]");
const lightboxInner = document.querySelector("[data-lightbox-inner]");
const lightboxClose = document.querySelector("[data-lightbox-close]");

function closeLightbox() {
  if (!lightbox || !lightboxInner) return;
  lightbox.setAttribute("aria-hidden", "true");
  lightboxInner.querySelectorAll("video").forEach((video) => video.pause());
  lightboxInner.querySelectorAll("img, video").forEach((node) => node.remove());
}

document.querySelectorAll("[data-popout]").forEach((button) => {
  button.addEventListener("click", () => {
    if (!lightbox || !lightboxInner) return;

    closeLightbox();
    const src = button.getAttribute("data-src");
    const kind = button.getAttribute("data-kind");
    const alt = button.getAttribute("data-alt") || "";

    let node;
    if (kind === "video") {
      node = document.createElement("video");
      node.controls = true;
      node.autoplay = true;
      node.playsInline = true;
      const source = document.createElement("source");
      source.src = src;
      source.type = "video/mp4";
      node.append(source);
    } else {
      node = document.createElement("img");
      node.src = src;
      node.alt = alt;
    }

    lightboxInner.append(node);
    lightbox.setAttribute("aria-hidden", "false");
  });
});

if (lightboxClose) {
  lightboxClose.addEventListener("click", closeLightbox);
}

if (lightbox) {
  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) closeLightbox();
  });
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeLightbox();
});
