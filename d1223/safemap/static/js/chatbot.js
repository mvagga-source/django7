document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("chatbot-btn");
  const popup = document.getElementById("chatbot-popup");
  const closeBtn = document.getElementById("chatbot-close");

  const input = document.getElementById("chat-input");
  const sendBtn = document.getElementById("chat-send");
  const messages = document.getElementById("chatbot-messages");

  btn.addEventListener("click", () => {
    popup.classList.toggle("open");
  });

  closeBtn.addEventListener("click", () => {
    popup.classList.remove("open");
  });

  function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    const userMsg = document.createElement("div");
    userMsg.className = "msg user";
    userMsg.textContent = text;
    messages.appendChild(userMsg);

    input.value = "";
    messages.scrollTop = messages.scrollHeight;

    setTimeout(() => {
      const botMsg = document.createElement("div");
      botMsg.className = "msg bot";
      botMsg.textContent = "아직 AI 연결 전입니다 🤖";
      messages.appendChild(botMsg);
      messages.scrollTop = messages.scrollHeight;
    }, 400);
  }

  sendBtn.addEventListener("click", sendMessage);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});