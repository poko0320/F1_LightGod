"use client";

import useAuth from "@/hooks/useAuth";
import { useEffect, useState } from "react";
import { styles } from "../../components/dashboard";
import Image from "next/image";

type PredictRow = {
  player_name: string;
  P1: number; P2: number; P3: number; P4: number; P5: number;
  special: number;
  RaceCode: string;
};

type ApiPayload = {
  points?: Array<{ points: number; player_name?: string }>;
  predicts?: PredictRow[];
};

const API_BASE = process.env.NEXT_PUBLIC_OWN_API!; 

export default function Dashboard() {
  const { user, loading } = useAuth();
  const [points, setPoints] = useState<string>("-");
  const [predictions, setPredictions] = useState<PredictRow[]>([]);
  const [err, setErr] = useState<string | null>(null);

  const displayName =
    user?.user_metadata?.display_name ??
    user?.user_metadata?.full_name ??
    user?.email?.split("@")[0] ??
    "User";
  
  const avatar =
    user?.user_metadata?.avatar_url || "/user.png";

  useEffect(() => {
    if (loading || !user) return;
    if (!API_BASE) {
      setErr("NEXT_PUBLIC_OWN_API is not defined.");
      return;
    }

    const pname =
      user?.user_metadata?.display_name ?? user.email?.split("@")[0] ?? "user";

    (async () => {
      try {
        setErr(null);

        const url = `${API_BASE}/player/getDashboardData/${encodeURIComponent(pname)}`;
        const res = await fetch(url, { cache: "no-store" });
        if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);

        const data: ApiPayload = await res.json();
        console.log("dashboard payload:", data);

        // Points: first row’s points or 0
        const p =
          Array.isArray(data.points) && data.points.length
            ? data.points[0]?.points ?? 0
            : 0;
        setPoints(String(p));

        // Predictions: must be data.predicts
        const list = Array.isArray(data.predicts) ? data.predicts : [];
        setPredictions(list);
      } catch (e) {
        if (e instanceof Error) {
          setErr(e.message);
        } else {
          setErr(String(e));
        }
      }
    })();
  }, [loading, user]);

  if (loading) return <div>Loading…</div>;
  if (!user) return <div>Please sign in</div>;

  const fmt = (r: PredictRow) =>
    `${r.P1} > ${r.P2} > ${r.P3} > ${r.P4} > ${r.P5} | S:${r.special}`;

  return (
    <div style={styles.card}>
      {/* Header */}
      <div style={styles.header}>
        <Image
          src={avatar}
          alt="Avatar"
          width={64}
          height={64}
          style={styles.avatar}
        />
        <div>
          <h1 style={styles.title}>{displayName}</h1>
          <p style={styles.subtitle}>Profile Dashboard</p>
        </div>
      </div>

      {/* Info */}
      <div style={styles.infoGrid}>
        <div style={styles.field}><span>User ID</span><span>{user.id}</span></div>
        <div style={styles.field}><span>Email</span><span>{user.email}</span></div>
        <div style={styles.field}><span>Points</span><span>{points}</span></div>
      </div>

      {err && (
        <div style={{ color: "#842029", background: "#f8d7da", border: "1px solid #f5c2c7", padding: 8, borderRadius: 8 }}>
          {err}
        </div>
      )}

      {/* Predictions */}
      <div style={styles.predictions}>
        <h2>Your Predictions</h2>
        {predictions.length === 0 ? (
          <p>No predictions yet.</p>
        ) : (
          <ul style={styles.predList}>
            {predictions.map((p, i) => (
              <li key={`${p.RaceCode}-${i}`} style={styles.predItem}>
                <strong>{p.RaceCode}</strong> — {fmt(p)}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
