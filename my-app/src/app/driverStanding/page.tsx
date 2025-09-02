import React from "react";

const API_BASE = process.env.OWN_API!;

const DriverStanding = async () => {
  const res = await fetch(`${API_BASE}/driver/get`, {
    cache: "no-store", // disable caching
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  const data = await res.json();

  return (
    <div style={styles.container}>
      {/* Header Row */}
      <div style={{ ...styles.row, ...styles.header }}>
        <div style={styles.cell}>#</div>
        <div style={styles.cell}>Name</div>
        <div style={styles.cell}>No.</div>
        <div style={styles.cell}>Team</div>
        <div style={styles.cell}>Points</div>
      </div>

      {/* Data Rows */}
      {data.drivers.map((d: any, idx: number) => (
        <div key={d.name} style={styles.row}>
          <div style={{ ...styles.cell, ...styles.withBorder }}>{d.standing ?? idx + 1}</div>
          <div style={{ ...styles.cell, ...styles.withBorder }}>{d.name}</div>
          <div style={{ ...styles.cell, ...styles.withBorder }}>{d.driver_Num}</div>
          <div style={{ ...styles.cell, ...styles.withBorder }}>{d.team}</div>
          <div style={styles.cell}>{d.points}</div> {/* no border-right on last col */}
        </div>
      ))}
    </div>
  );
};

export default DriverStanding;

// Inline CSS styles
const styles: { [k: string]: React.CSSProperties } = {
  container: {
    display: "grid",
    gridTemplateColumns: "1fr", // rows stack
    maxWidth: 800,
    margin: "20px auto",
    fontFamily: "sans-serif",
    border: "1px solid #ccc", // outer border
    borderRadius: "6px",
    overflow: "hidden",
  },
  row: {
    display: "grid",
    gridTemplateColumns: "50px 1fr 60px 1fr 80px", // 5 columns
    borderBottom: "1px solid #ccc",
    alignItems: "center",
  },
  cell: {
    padding: "10px",
  },
  withBorder: {
    borderRight: "1px solid #ccc",
  },
  header: {
    fontWeight: "bold",
    backgroundColor: "#f5f5f5",
  },
};