import { useState, useRef } from 'react'

const API_URL = 'http://localhost:8000'

export default function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const bottomRef = useRef(null)

  async function sendMessage() {
    const query = input.trim()
    if (!query || isStreaming) return

    setInput('')
    setMessages((prev) => [
      ...prev,
      { role: 'user', text: query },
      { role: 'assistant', text: '' },
    ])
    setIsStreaming(true)

    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    })

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const textChunk = decoder.decode(value, { stream: true })

      setMessages((prev) => {
        const updated = [...prev]
        const last = updated[updated.length - 1]
        updated[updated.length - 1] = { ...last, text: last.text + textChunk }
        return updated
      })

      bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    setIsStreaming(false)
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="chat-container">
      <h1>College Enquiry Chatbot</h1>

      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.role}`}>
            <span className="role-label">{m.role === 'user' ? 'You' : 'Bot'}</span>
            <p>{m.text || (isStreaming && i === messages.length - 1 ? '…' : '')}</p>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="input-row">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about admissions, courses, fees..."
          rows={2}
        />
        <button onClick={sendMessage} disabled={isStreaming}>
          {isStreaming ? 'Thinking...' : 'Send'}
        </button>
      </div>
    </div>
  )
}