import { useContext } from "react";
import { AuthContext } from "../components/ui/context/AuthProvider";

/**
 * @typedef {Object} AuthUser
 * @property {string} id - User ID
 * @property {string} [email] - User email
 * @property {Object} [user_metadata] - User metadata
 * @property {string} [user_metadata.display_name] - Display name
 * @property {string} [user_metadata.full_name] - Full name
 * @property {string} [user_metadata.avatar_url] - Avatar URL
 */

/**
 * @typedef {Object} AuthContextType
 * @property {AuthUser|null} user - Current user or null
 * @property {boolean} loading - Loading state
 */

/**
 * Hook to access authentication context
 * @returns {AuthContextType} The auth context containing user and loading state
 */
const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context; // returns { user, loading }
};

export default useAuth;