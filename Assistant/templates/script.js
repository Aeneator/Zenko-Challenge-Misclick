const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox")

let userMessage;

const createChatLi = (message, className) => {
  const chatLi = document.createElement("li");
  chatLi.classList.add("chat", className);
  let chatContent = className === "outgoing" ? `<p>${message}</p>` : `<span class="material-symbols-outlined">smart_toy</span><p>${message}</p>`;
  chatLi.innerHTML = chatContent;
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
}

sendChatBtn.addEventListener("click", handleChat);