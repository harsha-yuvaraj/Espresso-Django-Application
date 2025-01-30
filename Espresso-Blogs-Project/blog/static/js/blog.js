document.addEventListener("DOMContentLoaded", function () {
  const copyLinkElements = document.querySelectorAll(".copy-post-link");

  copyLinkElements.forEach(function (copyLink) {
    copyLink.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent the link from doing anything

      const urlToCopy = copyLink.getAttribute("data-url"); // Get the data-url value

      // Use the Clipboard API to copy the URL to the clipboard
      navigator.clipboard
        .writeText(urlToCopy)
        .then(() => {
          alert("Link copied to clipboard!");
        })
        .catch((err) => {
          alert("Error copying link: ", err);
        });
    });
  });

  // Open the modal
  document
    .getElementById("openModalBtn")
    .addEventListener("click", function () {
      document.getElementById("myModal").style.display = "block";
      let postText = document.getElementById("post-body").innerText;
      typeWriter("modalText", postText, 20);
    });

  // Close the modal
  document
    .getElementById("closeModalBtn")
    .addEventListener("click", function () {
      document.getElementById("modalText").innerHTML = "";
      document.getElementById("myModal").style.display = "none";
    });
});

let typewriterTimeout; // Store the timeout reference

function typeWriter(elementId, text, speed) {
    let i = 0;
    let textElement = document.getElementById(elementId);
    textElement.innerHTML = "";

    function type() {
      if (i < text.length) {
        textElement.innerHTML += text.charAt(i);
        i++;
        typewriterTimeout = setTimeout(type, speed);
      }
    }
    
    clearTimeout(typewriterTimeout);
    type();
  }
  