import { useEffect, useRef } from "react";

const ChatMessages = ({ messages, messagesEndRef }) => {
  const chatContainerRef = useRef(null);

  // Auto-scroll function
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  function formatMessageText(text) {
    // This will handle basic formatting like new lines
    return text.split("\n").map((line, index) => (
      <span key={index}>
        {line}
        {index < text.split("\n").length - 1 && <br />}
      </span>
    ));
  }

  return (
    <div className="chat-messages-container" ref={chatContainerRef}>
      <div className="messages-list">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message-wrapper ${message.sender}-wrapper`}
          >
            <div
              className={`message ${message.sender}-message ${
                message.isError ? "error-message" : ""
              }`}
            >
              {message.sender === "bot" && !message.isLoading && (
                <div className="message-avatar bot-avatar">
                  <i className="bi bi-robot"></i>
                </div>
              )}

              {message.sender === "user" && (
                <div className="message-avatar user-avatar">
                  <i className="bi bi-person-circle"></i>
                </div>
              )}

              <div className="message-content">
                {message.isLoading ? (
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                ) : (
                  <>
                    <div className="message-text">
                      {formatMessageText(message.text)}
                    </div>

                    {message.sources && message.sources.length > 0 && (
                      <div className="message-sources">
                        <div className="sources-title">
                          <i className="bi bi-link-45deg"></i> Sources
                        </div>
                        <ul className="sources-list">
                          {message.sources.map((source, index) => (
                            <li key={index}>{source}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </>
                )}
              </div>

              <div className="message-time">
                {!message.isLoading &&
                  new Date().toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
              </div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ChatMessages;
