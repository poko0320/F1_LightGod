import React from "react";

const API_BASE = process.env.NEXT_PUBLIC_OWN_API!;

export default async function PlayerStanding() {
  const res = await fetch(`${API_BASE}/player/getTOP10`, { cache: "no-store" });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);

  const data = await res.json(); // { player: [...] }
  const rows: Array<{ player_name: string; points: number }> = Array.isArray(data?.player)
    ? data.player
    : [];

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={{ ...styles.row, ...styles.header }}>
        <div style={{ ...styles.cell, ...styles.withBorder }}>#</div>
        <div style={{ ...styles.cell, ...styles.withBorder }}>Name</div>
        <div style={styles.cell}>Points</div>
      </div>

      {/* Rows */}
      {rows.length > 0 ? (
        rows.slice(0, 10).map((d, idx) => (
          <div key={`${d.player_name}-${idx}`} style={styles.row}>
            <div style={{ ...styles.cell, ...styles.withBorder }}>{idx + 1}</div>
            <div style={{ ...styles.cell, ...styles.withBorder }}>{d.player_name}</div>
            <div style={styles.cell}>{d.points ?? 0}</div>
          </div>
        ))
      ) : (
        <div style={styles.row}>
          <div style={{ ...styles.cell, ...styles.withBorder }}>–</div>
          <div style={{ ...styles.cell, ...styles.withBorder }}>No results</div>
          <div style={styles.cell}>–</div>
        </div>
      )}
    </div>
  );
}

const styles: { [k: string]: React.CSSProperties } = {
  container: {
    display: "grid",
    gridTemplateColumns: "1fr",
    maxWidth: 640,
    margin: "20px auto",
    fontFamily: "sans-serif",
    border: "1px solid #ccc",
    borderRadius: "6px",
    overflow: "hidden",
  },
  row: {
    display: "grid",
    gridTemplateColumns: "60px 1fr 100px", // # | Name | Points
    borderBottom: "1px solid #eee",
    alignItems: "center",
  },
  cell: { padding: "10px" },
  withBorder: { borderRight: "1px solid #eee" },
  header: { fontWeight: "bold", backgroundColor: "#f5f5f5" },
};
