'use client';
import Image from "next/image";
import LoginButton from "./login";

export default function Header() {
  return (
    <header style={styles.header}>
      {/* Left: Logo */}
      <div style={styles.logoContainer}>
        <Image
          src="/RBCar.png"   // Put your logo in the `public/` folder (e.g., public/logo.svg)
          alt="RB car"
          width={100}       // adjust size
          height={40}
        />
      </div>

      {/* Right: Login Button */}
      <LoginButton />
    </header>
  );
}

const styles: { [k: string]: React.CSSProperties } = {
  header: {
    width: "100%",
    height: 60,
    backgroundColor: "#e10600", // Ferrari red
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between", // logo left, button right
    padding: "0 20px",
    boxShadow: "0 2px 6px rgba(0,0,0,0.2)",
  },
  logoContainer: {
    display: "flex",
    alignItems: "center",
  },
};