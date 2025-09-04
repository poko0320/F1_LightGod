'use client';
import React from 'react'
import { useRouter } from "next/navigation";

const Dashboard = () => {
  const router = useRouter();
  return (
    <button 
      style={styles.button} 
      onClick={() => router.push("/dashboard")}
    >
      Dashboard
    </button>
  )
}

export default Dashboard

import { CSSProperties } from "react";

export const styles: { [k: string]: CSSProperties } = {
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
  card: {
    maxWidth: "700px",
    margin: "20px auto",
    padding: "20px",
    borderRadius: "12px",
    border: "1px solid #ccc",
    background: "rgba(255,255,255,0.7)",
    boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
  },
  header: {
    display: "flex",
    alignItems: "center",
    gap: "16px",
    marginBottom: "20px",
  },
  avatar: {
    borderRadius: "50%",
    border: "2px solid #ddd",
    objectFit: "cover",
  },
  title: {
    fontSize: "1.25rem",
    fontWeight: 600,
    margin: 0,
  },
  subtitle: {
    fontSize: "0.9rem",
    color: "#555",
    margin: 0,
  },
  infoGrid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "12px",
    marginBottom: "24px",
  },
  field: {
    display: "flex",
    flexDirection: "column",
    padding: "8px",
    border: "1px solid #eee",
    borderRadius: "8px",
    fontSize: "0.9rem",
  },
  predictions: {
    marginTop: "20px",
  },
  predList: {
    listStyle: "none",
    padding: 0,
    marginTop: "8px",
  },
  predItem: {
    borderBottom: "1px solid #eee",
    padding: "6px 0",
    fontSize: "0.9rem",
  },
};
