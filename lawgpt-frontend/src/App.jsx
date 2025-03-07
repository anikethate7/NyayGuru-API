import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./styles/App.css";
import Header from "./components/Header";
import ChatPage from "./pages/ChatPage";
import NotFound from "./pages/NotFound";
import { SessionProvider } from "./context/SessionContext";

function App() {
  return (
    <Router>
      <SessionProvider>
        <div className="App">
          <Header />
          <Routes>
            <Route path="/" element={<ChatPage />} />
            <Route path="/category/:category" element={<ChatPage />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </SessionProvider>
    </Router>
  );
}

export default App;
