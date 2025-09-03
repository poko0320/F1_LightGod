'use client';
import Image from "next/image";
import LoginButton from "./loginButton";
import PredictButton from "./predictButton";
import StandingButton from "./standingButton";
import Link from "next/link";
import DashboardButton from "./dashboardButton";
import PlayerStandingButton from "./playerstandingButton";


export default function Header() {
  return (
    <header style={styles.header}>
      {/* Left: Logo */}
      <div style={styles.logoContainer}>
        <Link href="/">
          <Image
            src="/RBCar.png"
            alt="RB car"
            width={100}
            height={40}
            style={{ cursor: "pointer" }}
          />
        </Link>
      </div>

      {/* Right: Buttons together */}
      <div style={styles.buttonGroup}>
        <PlayerStandingButton/>
        <DashboardButton/>
        <StandingButton/>
        <PredictButton />
        <LoginButton />
      </div>
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
    justifyContent: "space-between", // logo left, buttons right
    padding: "0 20px",
    boxShadow: "0 2px 6px rgba(0,0,0,0.2)",
  },
  logoContainer: {
    display: "flex",
    alignItems: "center",
  },
  buttonGroup: {
    display: "flex",
    alignItems: "center",
    gap: "12px", // space between buttons
  },
};