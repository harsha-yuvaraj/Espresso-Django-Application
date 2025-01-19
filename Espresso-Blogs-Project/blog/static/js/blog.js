document.addEventListener('DOMContentLoaded', function () {
    const copyLinkElements = document.querySelectorAll('.copy-post-link');

    copyLinkElements.forEach(function (copyLink) {
        copyLink.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent the link from doing anything

            const urlToCopy = copyLink.getAttribute('data-url'); // Get the data-url value

            // Use the Clipboard API to copy the URL to the clipboard
            navigator.clipboard.writeText(urlToCopy)
                .then(() => {
                    alert('Link copied to clipboard!');
                })
                .catch(err => {
                    alert('Error copying link: ', err);
                });
        });
    });
});
