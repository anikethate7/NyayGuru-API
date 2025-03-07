export const ChatInput = ({
  onSendMessage,
  languages,
  currentLanguage,
  onLanguageChange,
  disabled,
}) => {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || disabled) return;

    onSendMessage(input);
    setInput("");
  };

  return (
    <div className="chat-input">
      <form onSubmit={handleSubmit}>
        <div className="row g-3 align-items-center">
          <div className="col-md-4">
            <label htmlFor="language" className="form-label">
              Language
            </label>
            <select
              className="form-select"
              id="language"
              value={currentLanguage}
              onChange={(e) => onLanguageChange(e.target.value)}
            >
              {Object.keys(languages).map((lang) => (
                <option key={lang} value={lang}>
                  {lang}
                </option>
              ))}
            </select>
          </div>
          <div className="col-md-8">
            <label htmlFor="user-input" className="form-label visually-hidden">
              Your Question
            </label>
            <div className="input-group">
              <input
                type="text"
                className="form-control"
                id="user-input"
                placeholder={
                  disabled && !currentLanguage
                    ? "Please select a category first..."
                    : "Type your legal question here..."
                }
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={disabled}
                required
              />
              <button
                className="btn btn-primary"
                type="submit"
                disabled={disabled}
              >
                <i className="bi bi-send"></i> Send
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
};
