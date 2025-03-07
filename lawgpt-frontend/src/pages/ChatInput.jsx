import { useState } from "react";

const ChatInput = ({ onSendMessage, disabled, isProcessing }) => {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || disabled) return;

    onSendMessage(input);
    setInput("");
  };

  return (
    <div className="chat-input-container">
      <form onSubmit={handleSubmit}>
        <div className="input-wrapper">
          <input
            type="text"
            className="message-input"
            placeholder={
              disabled
                ? "Please select a category first..."
                : "Type your legal question here..."
            }
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={disabled}
            required
          />
          <button
            className={`send-button ${disabled ? "disabled" : ""} ${
              isProcessing ? "processing" : ""
            }`}
            type="submit"
            disabled={disabled}
          >
            {isProcessing ? (
              <i className="bi bi-arrow-repeat spin"></i>
            ) : (
              <i className="bi bi-send-fill"></i>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInput;
