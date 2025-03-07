import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const ProfilePage = () => {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const handleLogout = async () => {
    setIsLoggingOut(true);
    try {
      await logout();
      navigate("/login");
    } catch (error) {
      console.error("Logout failed:", error);
    } finally {
      setIsLoggingOut(false);
    }
  };

  if (!currentUser) {
    return <div>Loading profile...</div>;
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h2>Your Profile</h2>
      </div>

      <div className="profile-content">
        <div className="profile-avatar">
          <i className="bi bi-person-circle"></i>
        </div>

        <div className="profile-details">
          <div className="profile-name">
            {currentUser.firstName} {currentUser.lastName}
          </div>
          <div className="profile-email">{currentUser.email}</div>
        </div>

        <div className="profile-actions">
          <button className="action-button edit-profile">
            <i className="bi bi-pencil"></i> Edit Profile
          </button>
          <button
            className="action-button logout"
            onClick={handleLogout}
            disabled={isLoggingOut}
          >
            {isLoggingOut ? (
              <i className="bi bi-arrow-repeat spin"></i>
            ) : (
              <>
                <i className="bi bi-box-arrow-right"></i> Logout
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
