document.addEventListener("DOMContentLoaded", function () {
  const dropArea = document.querySelector(".drag-area");

  if (dropArea) {
    const buttonClick = dropArea.querySelector(".button-upload");
    const imageInput = document.getElementById("imageInput");
    const imagePreview = document.getElementById("imagePreview");
    const originalImageContainer = document.getElementById(
      "originalImageContainer"
    );

    const wrap = dropArea.querySelector(".wrap");

    buttonClick.onclick = () => imageInput.click();

    imageInput.addEventListener("change", handleFile);
    dropArea.addEventListener("dragover", handleDragOver);
    dropArea.addEventListener("dragleave", handleDragLeave);
    dropArea.addEventListener("drop", handleDrop);

    function handleFile(event) {
      const file = event.target.files[0];
      if (file) {
        displayFile(file);
      }
    }

    function handleDragOver(event) {
      event.preventDefault();
      dropArea.classList.add("active");
      dragText.textContent = "Release to Upload";
    }

    function handleDragLeave() {
      dropArea.classList.remove("active");
      dragText.textContent = "Drag & Drop";
    }

    function handleDrop(event) {
      event.preventDefault();
      const file = event.dataTransfer.files[0];
      if (file) {
        imageInput.files = event.dataTransfer.files;
        displayFile(file);
      }
    }

    function displayFile(file) {
      const fileType = file.type;
      const validExtensions = ["image/jpeg", "image/jpg", "image/png"];
      if (validExtensions.includes(fileType)) {
        const fileReader = new FileReader();
        fileReader.onload = () => {
          const fileURL = fileReader.result;
          if (imagePreview) {
            imagePreview.src = fileURL;
            imagePreview.style.display = "block";
            originalImageContainer.style.display = "block";
          } else {
            const imgElement = document.createElement("img");
            imgElement.src = fileURL;
            // imgElement.style.height = "500px";
            // imgElement.style.width = "auto";
            imgElement.classList.add("img-preview");
            dropArea.appendChild(imgElement);
            wrap.style.display = "none";
            sessionStorage.setItem("imageSrc", fileURL);
            console.error("Element with ID 'imagePreview' not found.");
          }
          sessionStorage.setItem("imageSrc", fileURL);
          dropArea.classList.remove("active");
          dragText.textContent = "Drag & Drop";
          wrap.style.display = "none";

          setTimeout(() => {
            location.reload();
          }, 1000);
        };
        fileReader.readAsDataURL(file);
      } else {
        alert("This is not an Image File");
        dropArea.classList.remove("active");
        dragText.textContent = "Drag & Drop";
      }
    }
  } else {
    removeButton = document.getElementById("removeButton");
    removeButton.onclick = () => {
      sessionStorage.removeItem("imageSrc");
      window.location.href = "/";
    };
    window.addEventListener("load", handleLoad);
    const preprocessedImagePreview = document.getElementById(
      "preprocessedImagePreview"
    );
    const preprocessedImageContainer = document.getElementById(
      "preprocessedImageContainer"
    );
    function handleLoad() {
      console.log("Loaded");
      const savedImageSrc = sessionStorage.getItem("imageSrc");
      if (savedImageSrc) {
        imagePreview.src = savedImageSrc;
        imagePreview.style.display = "block";
        originalImageContainer.style.display = "block";
      }

      if ("{{ preprocessed_image_path }}") {
        preprocessedImageContainer.style.display = "block";
        preprocessedImagePreview.style.display = "block";
      } else {
        preprocessedImageContainer.style.display = "none";
        preprocessedImagePreview.style.display = "none";
      }
    }
    console.error("Element with class 'drag-area' not found.");
  }
});
