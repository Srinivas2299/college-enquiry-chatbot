import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./style.css";

function App() {
  const [open, setOpen] = useState(false);

  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "Hello! 👋 How can I help you?"
    }
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // =========================================================
  // SEND MESSAGE
  // =========================================================

  const sendMessage = async () => {
    const question = input.trim();

    if (!question || loading) {
      return;
    }

    // Add user's message to chat
    setMessages((previousMessages) => [
      ...previousMessages,
      {
        role: "user",
        text: question
      }
    ]);

    // Clear input
    setInput("");

    // =======================================================
    // NORMALIZE USER INPUT
    // =======================================================

    const normalizedQuestion = question
      .toLowerCase()
      .replace(/[!?.,]/g, "")
      .trim();

    // =======================================================
    // FRONTEND-ONLY RESPONSES
    // These DO NOT call FastAPI / RAG / ChromaDB / Groq
    // =======================================================

    const frontendResponses = {
      // Greetings
      hi: "Hi! 👋 How can I help you?",
      hello: "Hello! 👋 How can I help you?",
      hey: "Hey!👋 How can I help you?",
      hii: "Hello! 👋 How can I help you?",
      hiii: "Hello! 👋 How can I help you?",
      helo: "Hello! 👋 How can I help you?",

      // Greetings with time
      "good morning":
        "Good morning! ☀️ How can I help you?",

      "good afternoon":
        "Good afternoon! 😊 How can I help you?",

      "good evening":
        "Good evening! 🌆 How can I help you?",

      "good night":
        "Good night! 🌙 Feel free to ask me about VJIT anytime.",

      // Thanks
      thanks:
        "You're welcome! 😊",

      "thank you":
        "You're welcome! 😊",

      "thanks a lot":
        "You're very welcome! 😊",

      "thank you so much":
        "You're very welcome! 😊",

      // Goodbye
      bye:
        "Goodbye! 👋 Have a great day!",

      goodbye:
        "Goodbye! 👋 Have a great day!",

      "see you":
        "See you! 👋 Have a great day!",

      "see you later":
        "See you later! 👋",

      // Simple conversation
      "who are you":
        "I'm VJIT College Bot 🤖. I can help you with college-related enquiries.",

      "what can you do":
        "I can answer questions about VJIT using the college information available to me.",

      help:
        "Sure! 😊 Ask me anything about VJIT, such as admissions, courses, departments, fees, facilities, placements, or other college information."
    };

    // =======================================================
    // CHECK FRONTEND RESPONSES
    // =======================================================

    if (frontendResponses[normalizedQuestion]) {
      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "bot",
          text: frontendResponses[normalizedQuestion]
        }
      ]);

      return;
    }

    // =======================================================
    // ACTUAL COLLEGE QUESTIONS
    // SEND TO:
    // React → FastAPI → RAG → ChromaDB → Groq
    // =======================================================

    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            query: question
          })
        }
      );

      if (!response.ok) {
        throw new Error(
          `Server error: ${response.status}`
        );
      }

      // =====================================================
      // READ STREAMING RESPONSE
      // =====================================================

      const reader = response.body.getReader();

      const decoder = new TextDecoder();

      let answer = "";

      // Add empty bot message
      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "bot",
          text: ""
        }
      ]);

      // Read response chunk by chunk
      while (true) {
        const { value, done } =
          await reader.read();

        if (done) {
          break;
        }

        const chunk = decoder.decode(value, {
          stream: true
        });

        answer += chunk;

        // Update last bot message while streaming
        setMessages((previousMessages) => {
          const updatedMessages = [
            ...previousMessages
          ];

          updatedMessages[
            updatedMessages.length - 1
          ] = {
            role: "bot",
            text: answer
          };

          return updatedMessages;
        });
      }

    } catch (error) {
      console.error(
        "Chatbot error:",
        error
      );

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "bot",
          text:
            "I'm unable to connect to the server right now. Please try again."
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // ENTER KEY
  // =========================================================

  const handleKeyDown = (event) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();

      sendMessage();
    }
  };

  // =========================================================
  // UI
  // =========================================================

  return (
    <>
      {/* =====================================================
          CHAT WINDOW
          ===================================================== */}

      {open && (
        <div className="chatbot-window">

          {/* HEADER */}
          <div className="chatbot-header">

            <div className="chatbot-brand">

              <div className="chatbot-logo">
                <img
                  src="/vjit-logo.png"
                  alt="VJIT Logo"
                />
              </div>

              <h3>VJIT College Bot</h3>

            </div>

            <button
              className="close-button"
              onClick={() =>
                setOpen(false)
              }
              aria-label="Close chatbot"
            >
              ×
            </button>

          </div>

          {/* =================================================
              MESSAGES
              ================================================= */}

          <div className="chatbot-messages">

            {messages.map(
              (message, index) => (

                <div
                  key={index}
                  className={
                    message.role === "user"
                      ? "message-wrapper user-message-wrapper"
                      : "message-wrapper bot-message-wrapper"
                  }
                >

                  {/* BOT AVATAR */}
                  {message.role === "bot" && (
                    <div className="message-avatar bot-avatar">
                      🤖
                    </div>
                  )}

                  {/* MESSAGE */}
                  <div
                    className={
                      message.role === "user"
                        ? "message user-message"
                        : "message bot-message"
                    }
                  >
                    <ReactMarkdown>{message.text}</ReactMarkdown>
                  </div>

                  {/* USER AVATAR */}
                  {message.role === "user" && (
                    <div className="message-avatar user-avatar">
                      👤
                    </div>
                  )}

                </div>
              )
            )}

            {/* =================================================
                LOADING INDICATOR
                ================================================= */}

            {loading && (
              <div className="message-wrapper bot-message-wrapper">

                <div className="message-avatar bot-avatar">
                  🤖
                </div>

                <div className="message bot-message typing-message">

                  <span></span>
                  <span></span>
                  <span></span>

                </div>

              </div>
            )}

          </div>

          {/* =================================================
              INPUT
              ================================================= */}

          <div className="chatbot-input-area">

            <textarea
              value={input}
              onChange={(event) =>
                setInput(event.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Ask about admissions, courses, fees..."
              disabled={loading}
              rows={1}
            />

            <button
              className="send-button"
              onClick={sendMessage}
              disabled={
                loading ||
                !input.trim()
              }
              aria-label="Send message"
            >
              ➤
            </button>

          </div>

        </div>
      )}

      {/* =====================================================
          FLOATING CHAT BUTTON
          ===================================================== */}

      <button
        className={`chatbot-launcher ${
          open ? "launcher-open" : ""
        }`}
        onClick={() =>
          setOpen(
            (previousState) =>
              !previousState
          )
        }
        aria-label="Open VJIT College Bot"
      >
        {open ? "×" : "💬"}
      </button>
    </>
  );
}

export default App;