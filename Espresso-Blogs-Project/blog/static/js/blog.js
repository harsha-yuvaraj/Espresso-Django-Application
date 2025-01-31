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

      const spinner = document.getElementById("spinnerIcon");
      spinner.classList.remove("hidden");

      let postId = parseInt(document.getElementById("post-body").getAttribute("data-post-id"));
      let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
      let apiEndpoint = document.getElementById("post-body").getAttribute("data-post-url");
      let postSummary = "";

      try{
          fetch(apiEndpoint, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken, 
            },
            body: JSON.stringify({
              post_id: postId,
          }), 
          }).then((response) => {
              if (!response.ok) 
                throw new Error("Error generating summary. Please try again later.");

              return response.json()

            }).then((data) => {
                spinner.classList.add("hidden");
                postSummary = data.summary || "Error generating summary. Please try again later. 😐";
                document.getElementById("myModal").style.display = "block";
                typeWriter("modalText", postSummary, 15);
              })
    } catch (error) {
      spinner.classList.add("hidden");
      alert("Error generating summary. Please try again later. 😐");
    } 

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
  