'use client';
import React from 'react'
import { useRouter } from "next/navigation";

const styles: { [k: string]: React.CSSProperties } = {
  button: {
    backgroundColor: "#e10600",   // Ferrari red
    color: "white",               // White text
    fontSize: "1.2rem",           // Bigger text
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
  return (
    <button 
      style={styles.button} 
      onClick={() => router.push("/login")}
    >
      Login
    </button>
  );
};

export default Login;