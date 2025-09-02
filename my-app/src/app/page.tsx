import type { CSSProperties } from "react";
import Header from "./components/Header";

const container: CSSProperties = {
  textAlign: "center",
  marginTop: 50,          // use number instead of "50px" (string or number is ok, but number is cleaner)
};

const title: CSSProperties = {
  fontSize: "2rem",
  color: "#e10600",
};

const text: CSSProperties = {
  fontSize: "1.2rem",
  color: "#333",
};

const link: CSSProperties = {
  display: "inline-block",
  marginTop: 20,
  color: "#0070f3",
  textDecoration: "underline",
};

export default function Home() {
  return (
    <>
      <div style={container}>
        <h1 style={title}>🏎️ Welcome to F1 LightGod</h1>
        <p style={text}>
          F1 predict game term break side project for fun only
        </p>
        <a href="https://github.com/poko0320/F1_LightGod" style={link}>GitHub</a>
      </div>
    </>
  );
}