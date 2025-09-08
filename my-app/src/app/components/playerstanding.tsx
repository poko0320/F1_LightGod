'use client';
import React from 'react'
import { useRouter } from "next/navigation";

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

const PlayerStanding = () => {
  const router = useRouter();
  return (
    <button 
      style={styles.button} 
      onClick={() => router.push("/playerStanding")}
    >
      Player Standing
    </button>
  )
}

export default PlayerStanding