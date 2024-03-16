document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("container");
  const searchParams = new URLSearchParams(window.location.search);
  // const FadeTime = 
  // console.log(FadeTime)
  // Function to fetch images from the server

  // function fetchImages() {
  //   fetch("http://127.0.0.1:5000/getimages")
  //     .then(response => response.json())
  //     .then(data => {
  //       data.images.forEach(image => {
  //         createSticker(image.src);
  //       });
  //     })
  //     .catch(error => {
  //       console.error('Error fetching images:', error);
  //     });
  // }

  // ^ replace the above with WS:
  // Create a WebSocket connection
  const socket = new WebSocket("ws://127.0.0.1:5000/frontendws"); //cSpell: disable-line

  // Handle WebSocket connection open event
  socket.onopen = function () {
    document.getElementById("overlay").style.display = "none";
    console.log("WebSocket connection established");
  };

  // Handle WebSocket message event
  socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    if (data.hasOwnProperty("spec_message")) {
      if (!data.spec_message.includes("HIDE-ERROR-STRING")) {
        document.getElementById("errtext").innerHTML = data.spec_message
        document.getElementById("overlay").style.display = "block";
      }

      else {
        document.getElementById("overlay").style.display = "none";
      }
    }
    if (data.hasOwnProperty("images")) {
      data.images.forEach(image => {
        createSticker(image.src);
      })
    }
  };

  // Handle WebSocket connection close event
  socket.onclose = function () {
    document.getElementById("errtext").innerHTML = "Discord overlay not connected<br>(refresh the source)!"
    document.getElementById("overlay").style.display = "block";
    console.log("WebSocket connection closed");
  };
  // Function to create a sticker
  function createSticker(src) {
    let FadeTime = searchParams.has("FadeTime") ? parseFloat(searchParams.get("FadeTime")) : 5.5
    FadeTime = Math.random() + FadeTime
    const sticker = document.createElement("img");
    sticker.src = src;
    sticker.classList.add("sticker");
    sticker.style.setProperty("animation", "fadeInOut " + FadeTime + "s ease-in-out")
    //console.log(sticker.style.getPropertyValue("animation"))
    // Set initial position
    sticker.style.left = Math.random() * (container.offsetWidth - 350) + "px";
    sticker.style.top = Math.random() * (container.offsetHeight - 350) + "px";

    container.appendChild(sticker);
    setTimeout(() => {
      container.removeChild(sticker);
    }, (FadeTime * 1000) + 500); // Fading duration is 1 second
    // Start fading out after 3 seconds
    //   setTimeout(() => {
    //     sticker.style.opacity = 0;
    //     // Remove the sticker from the DOM after fading out
    //     setTimeout(() => {
    //       container.removeChild(sticker);
    //     }, 100); // Fading duration is 1 second
    //   }, 5500);
  }

  // Fetch images every 5 seconds
  // setInterval(fetchImages, 2000);

  // Function to move stickers
  // function moveStickers() {
  //   const stickers = container.querySelectorAll('.sticker');
  //   stickers.forEach(sticker => {
  //     sticker.style.left = Math.random() * (container.offsetWidth - sticker.offsetWidth) + "px";
  //     sticker.style.top = Math.random() * (container.offsetHeight - sticker.offsetHeight) + "px";
  //   });
  // }

  // Move stickers initially and then periodically
  // moveStickers();
  // setInterval(moveStickers, 2000); // Adjust interval as needed
});
