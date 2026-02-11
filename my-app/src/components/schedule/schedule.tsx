"use client";
import { useEffect, useState } from "react";
import "./f1schedule.css";
const API_BASE = process.env.NEXT_PUBLIC_OWN_API!;

type RoundRow = {
  id: number;
  RoundNumber: number;
  Country: string;
  Location: string;
  Date: string;
};

export default function Schedule() {
  const [rounds, setRounds] = useState<RoundRow[]>([]);
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${API_BASE}/f1data/getEventSchedule`, {
          cache: "no-store",
        });
        if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
        setRounds(await res.json());
      } catch (e: any) {
        setErr(e?.message ?? "fetch error");
      }
    })();
  }, []);

  return (
    <main style={{ padding: 24 }}>
      <h1>F1 Schedule</h1>
      {err && <p style={{ color: "red" }}>{err}</p>}
      {rounds.map((r) => (
        <div key={r.id}>
          Round {r.RoundNumber} — {r.Location}, {r.Country} — {r.Date}
        </div>
      ))}
    </main>
  );
}
