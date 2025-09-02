'use client';
import React from 'react'
import { useRouter } from "next/navigation";
import useAuth from "@/hooks/useAuth";
import client from "@/api/client";

const styles: { [k: string]: React.CSSProperties } = {
  button: {
    backgroundColor: "#e10600",   // Ferrari red
    color: "white",
    fontSize: "1.2rem",
    fontWeight: "bold",
    border: "none",
    borderRadius: 8,
    padding: "12px 24px",
    cursor: "pointer",
    transition: "all 0.2s ease",
  },
};

const Login = () => {
  const router = useRouter();
  const { user, loading } = useAuth();

  // decide label
  let label = "Login";
  if (!loading && user) {
    label = "Logout";
  }

  const handleClick = () => {
    if (!loading && user) {
      client.auth.signOut({});
    } else {
      router.push("/login");
    }
  };

  return (
    <button style={styles.button} onClick={handleClick}>
      {label}
    </button>
  );
};

export default Login;