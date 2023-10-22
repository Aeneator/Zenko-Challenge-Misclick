const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox")

let userMessage;

function addMapWithMarkersToChatbox(markerData) {
    // Create a chat message item with the map element
    const mapMessage = createChatLi("", "incoming"); // Empty message, you can customize this
    const mapContainer = document.createElement("div");
    mapContainer.id = "map";
    mapContainer.classList.add("small-map");
    mapMessage.appendChild(mapContainer); // Append the map container to the chat message
    chatbox.appendChild(mapMessage); // Append the chat message to the chatbox
    coordsX = 0;
    coordsY = 0;
    markerData.forEach(function (data) {
       coordsX += parseFloat(data.coordinates[0]);
       coordsY += parseFloat(data.coordinates[1]);
    });
    coordsX /= markerData.length;
    coordsY /= markerData.length;
    // Initialize the map
    const map = L.map(mapContainer, {
    zoomControl: false,
    }).setView([coordsX, coordsY], 15);

    // Add a tile layer from OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Add markers to the map
    markerData.forEach(function (data) {
    L.marker(data.coordinates).addTo(map).bindPopup(data.popupText);
    });
}


function handleKeyPress(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
    handleChat();
    }
}

function updatePage(inputValue) {
    $.ajax({
        url: "/update-data/",  // Replace with the URL of your update_data view
        type: "GET",
        dataType: "json",
        data: { text: inputValue },
        success: function(data) {
            const ulItem = document.querySelector(".chatbox");
            ulItem.lastElementChild.lastElementChild.textContent = data.message;
            if (data.markers) {
              addMapWithMarkersToChatbox(data.markers);
            }
            document.querySelector(".chat-input textarea").readOnly = false;
        }
    });
}

const createChatLi = (message, className) => {
  const chatLi = document.createElement("li");
  chatLi.classList.add("chat", className);

  if (message) {
    // Only include the paragraph element if there's non-empty message content
    chatLi.innerHTML = className === "outgoing" ? `<p>${message}</p>` : `<span class="material-symbols-outlined"><img src="${document.getElementsByClassName("bot-icon")[0].getAttribute("src")}"></span><p>${message}</p>`;

  } else {
    // If there's no message content, set the inner HTML to an empty string
    chatLi.innerHTML = `<span class="material-symbols-outlined"><img src="${document.getElementsByClassName("bot-icon")[0].getAttribute("src")}"></span>`;

  }
  return chatLi;
}

const handleChatInput = () => {
  userMessage = chatInput.value.trim();
  if (userMessage !== '') {
    sendChatBtn.style.visibility = 'visible';
  } else {
    sendChatBtn.style.visibility = 'hidden';
  }
}

chatInput.addEventListener("input", handleChatInput);

const handleChat = () => {
  userMessage = chatInput.value.trim();
  if(!userMessage) return;
   updatePage(userMessage);
    document.querySelector(".chat-input textarea").readOnly = true;
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));

  // Simulate the thinking dots animation
  const thinkingMessage = createChatLi(`<span class="thinking-dots"></span>`, "incoming");
  

  // Simulate the thinking dots animation
  const dotsSpan = thinkingMessage.querySelector(".thinking-dots");
  setTimeout(() => {
    chatbox.appendChild(thinkingMessage);
    dotsSpan.setAttribute("background","none");
    dotsSpan.setAttribute("color","black");
    dotsSpan.style.animation = "thinking-dots 1.5s infinite"; // Restart the animation
  }, 600); // Adjust the timing as needed
        document.querySelector(".chat-input textarea").value = "";
}

sendChatBtn.addEventListener("click", handleChat);