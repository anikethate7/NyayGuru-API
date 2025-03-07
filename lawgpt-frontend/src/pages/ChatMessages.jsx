export const ChatMessages = ({ messages, messagesEndRef }) => {
  return (
    <div className="chat-messages" id="chat-messages">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`message ${message.sender}-message ${
            message.isError ? "error-message" : ""
          }`}
        >
          {message.isLoading ? (
            <>
              <div className="loader"></div>
              <p className="loading-message">{message.text}</p>
            </>
          ) : (
            <>
              <p>{message.text}</p>
              {message.sources && message.sources.length > 0 && (
                <div className="sources">
                  Sources: {message.sources.join(", ")}
                </div>
              )}
            </>
          )}
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatMessages;
