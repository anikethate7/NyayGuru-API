import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Header = () => {
  const { currentUser } = useAuth();

  return (
    <header className="app-header">
      <div className="header-content">
        <div className="logo">
          <i className="bi bi-scale"></i>
          <h1>LawGPT</h1>
        </div>
        <p className="tagline">
          Your AI-powered legal assistant, ready to help!
        </p>

        {currentUser && (
          <Link to="/profile" className="user-profile">
            <div className="user-avatar">
              <i className="bi bi-person"></i>
            </div>
            <span>{currentUser.firstName}</span>
          </Link>
        )}
      </div>
    </header>
  );
};

export default Header;
