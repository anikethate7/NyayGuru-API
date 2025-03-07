import { createContext, useState, useEffect, useContext } from "react";
import api from "../services/api";

const SessionContext = createContext();

export const SessionProvider = ({ children }) => {
  const [sessionId, setSessionId] = useState(null);
  const [categories, setCategories] = useState([]);
  const [languages, setLanguages] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const initializeSession = async () => {
      try {
        setLoading(true);
        // Create a new session
        const sessionResponse = await api.createSession();
        setSessionId(sessionResponse.session_id);

        // Fetch categories
        const categoriesResponse = await api.fetchCategories();
        setCategories(categoriesResponse.categories);

        // Fetch languages
        const languagesResponse = await api.fetchLanguages();
        setLanguages(languagesResponse.languages);

        setLoading(false);
      } catch (error) {
        console.error("Initialization error:", error);
        setError("Failed to initialize application. Please refresh the page.");
        setLoading(false);
      }
    };

    initializeSession();
  }, []);

  return (
    <SessionContext.Provider
      value={{
        sessionId,
        categories,
        languages,
        loading,
        error,
      }}
    >
      {children}
    </SessionContext.Provider>
  );
};

export const useSession = () => useContext(SessionContext);

export default SessionContext;
