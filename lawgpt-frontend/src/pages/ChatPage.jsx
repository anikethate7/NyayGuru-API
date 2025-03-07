import { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useSession } from "../context/SessionContext";
import api from "../services/api";
import CategoryTabs from "./CategoryTabs";
import ChatMessages from "./ChatMessages";
import ChatInput from "./ChatInput";
import LoadingSpinner from "./LoadingSpinner";

const ChatPage = () => {
  const { category: urlCategory } = useParams();
  const navigate = useNavigate();
  const { sessionId, categories, languages, loading, error } = useSession();

  const [messages, setMessages] = useState([
    {
      id: "welcome",
      text: "Hello! I'm LawGPT, your legal assistant. Select a legal category and ask me a question.",
      sender: "bot",
      sources: [],
    },
  ]);
  const [currentCategory, setCurrentCategory] = useState(null);
  const [currentLanguage, setCurrentLanguage] = useState("English");
  const [isProcessing, setIsProcessing] = useState(false);
  const [sidebarExpanded, setSidebarExpanded] = useState(false); // New state

  const messagesEndRef = useRef(null);

  const toggleSidebar = () => {
    setSidebarExpanded(!sidebarExpanded);
  };

  // Handle URL category parameter
  useEffect(() => {
    if (categories.length > 0 && urlCategory) {
      // Find the category that matches the URL parameter (case insensitive)
      const matchedCategory = categories.find(
        (cat) => cat.toLowerCase() === urlCategory.toLowerCase()
      );

      if (matchedCategory) {
        setCurrentCategory(matchedCategory);
      } else {
        // If category in URL doesn't exist, navigate to base path
        navigate("/");
      }
    }
  }, [urlCategory, categories, navigate]);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleCategoryChange = (category) => {
    setCurrentCategory(category);
    navigate(`/category/${category.toLowerCase().replace(/\s+/g, "-")}`);

    // Add category selection message
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now().toString(),
        text: `You are now in the "${category}" category. Please ask a relevant question.`,
        sender: "bot",
        sources: [],
      },
    ]);
  };

  const handleLanguageChange = (language) => {
    setCurrentLanguage(language);
  };

  const handleSendMessage = async (text) => {
    if (!text.trim() || !sessionId || !currentCategory) return;

    // Add user message to chat
    const userMessageId = Date.now().toString();
    setMessages((prev) => [
      ...prev,
      {
        id: userMessageId,
        text,
        sender: "user",
      },
    ]);

    // Add loading message
    const loadingId = `loading-${Date.now()}`;
    setMessages((prev) => [
      ...prev,
      {
        id: loadingId,
        text: "Generating response...",
        sender: "bot",
        isLoading: true,
      },
    ]);

    setIsProcessing(true);

    try {
      const response = await api.sendMessage(
        text,
        currentCategory,
        currentLanguage,
        sessionId
      );

      // Remove loading message and add actual response
      setMessages((prev) =>
        prev
          .filter((msg) => msg.id !== loadingId)
          .concat({
            id: Date.now().toString(),
            text: response.answer,
            sender: "bot",
            sources: response.sources || [],
          })
      );
    } catch (error) {
      console.error("Message sending failed:", error);

      // Remove loading message and add error message
      setMessages((prev) =>
        prev
          .filter((msg) => msg.id !== loadingId)
          .concat({
            id: Date.now().toString(),
            text: `Error: Failed to send your message. Please try again.`,
            sender: "bot",
            isError: true,
          })
      );
    } finally {
      setIsProcessing(false);
    }
  };

  if (loading) {
    return <LoadingSpinner message="Initializing LawGPT..." />;
  }

  if (error) {
    return <div className="error-container">{error}</div>;
  }

  return (
    <div className="app-container">
      <div className={`sidebar ${sidebarExpanded ? "expanded" : ""}`}>
        <div className="sidebar-header" onClick={toggleSidebar}>
          <h3>Categories</h3>
        </div>
        <div className="sidebar-content">
          <ul className="category-list">
            {categories.map((category) => (
              <li
                key={category}
                className={currentCategory === category ? "active" : ""}
                onClick={() => handleCategoryChange(category)}
              >
                <i className="bi bi-bookmark-fill"></i>
                <span>{category}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="sidebar-footer">
          <div className="language-selector">
            <label htmlFor="language-select">Language</label>
            <select
              id="language-select"
              value={currentLanguage}
              onChange={(e) => handleLanguageChange(e.target.value)}
            >
              {Object.keys(languages).map((lang) => (
                <option key={lang} value={lang}>
                  {lang}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      <div className="chat-panel">
        <div className="chat-header">
          <h2>
            <i className="bi bi-chat-square-text-fill"></i>
            {currentCategory
              ? `LawGPT - ${currentCategory}`
              : "LawGPT Assistant"}
          </h2>
          {currentCategory && (
            <span className="category-badge">{currentCategory}</span>
          )}
        </div>

        <ChatMessages messages={messages} messagesEndRef={messagesEndRef} />

        <ChatInput
          onSendMessage={handleSendMessage}
          disabled={!currentCategory || isProcessing}
          isProcessing={isProcessing}
        />
      </div>
    </div>
  );
};

export default ChatPage;
