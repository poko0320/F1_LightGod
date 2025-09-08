"use client";
import React from "react";
import { useRouter } from "next/navigation";
import useAuth from "@/hooks/useAuth";

const API_BASE = process.env.NEXT_PUBLIC_OWN_API!;

const styles: { [k: string]: React.CSSProperties } = {
  container: {
    display: "flex",
    justifyContent: "center",  // horizontal center
    alignItems: "center",      // vertical center
    height: "100vh",           // full viewport height
  },
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

export default function Page() {
  const router = useRouter();
  const { user } = useAuth();   

  const addUserPoint = async () => {
    const display_name = user?.user_metadata?.display_name || "";

    try {
      const res = await fetch(`${API_BASE}/player/addPlayerToPlayerStanding`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ playerName: display_name }),
      });

      if (!res.ok) {
        console.error("Failed to add player:", await res.text());
        return;
      }

      console.log("Player added successfully");
      router.push("/dashboard");   
    } catch (err) {
      console.error("Error adding player:", err);
    }
  };

  return (
    <div style={styles.container}>
      <button style={styles.button} onClick={addUserPoint}>
        Confirm
      </button>
    </div>
  );
}