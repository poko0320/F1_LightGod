import { useContext } from "react";
import { AuthContext } from "../components/ui/context/AuthProvider";

const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context; // should include { user, loading, ... }
};

export default useAuth;