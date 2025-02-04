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
  
  // Close the sidebar
  document
  .getElementById("close-sidebar")
  .addEventListener("click", function () {
    document.getElementById("sidebar").classList.add("collapse-sidebar");
    document.getElementById("content").classList.add("expand-content");
    document.getElementById("sidebar-icon").style.display = "inline-block";
    setSidebarState('true');
  });  

  // Open the sidebar
  document
  .getElementById("sidebar-icon")
  .addEventListener("click", function () {
    document.getElementById("sidebar").classList.remove("collapse-sidebar");
    document.getElementById("content").classList.remove("expand-content");
    document.getElementById("sidebar-icon").style.display = "none";
    setSidebarState('false');
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
              if (!response.ok) {
                  spinner.classList.add("hidden");

                  if(response.status === 429){
                    alert("Whoa, you’ve hit your 10-summary limit for today! Time to roll up your sleeves 😎 and dive into the full articles!");
                  }
                  else{
                    alert("Error generating summary. Please try again later. 😐");
                  }

                  // break here to prevent further execution
                  return;
              }

              return response.json()

            }).then((data) => {
                
                if (!data) 
                  return;

                spinner.classList.add("hidden");
                postSummary = data.summary || "No summary available.";
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
  
// Set the sidebar state in sessionStorage
function setSidebarState(isCollapsed) {
  sessionStorage.setItem('sidebarCollapsed', isCollapsed);
}

// Get the sidebar state from sessionStorage
function getSidebarState() {
  return sessionStorage.getItem('sidebarCollapsed') === 'true';  // default to false if not set
}

window.onload = function() {
  const isCollapsed = getSidebarState();

  if (isCollapsed) {
      document.getElementById('close-sidebar').click();
  }
  else {
      document.getElementById('sidebar-icon').click();
  }
};


