"use client";

import React, { useEffect, useMemo, useState } from "react";
import "./f1schedule.css";

const API_BASE = process.env.NEXT_PUBLIC_OWN_API!;

type RoundRow = {
  RoundNumber: number;
  Country: string;
  Location: string;
  Date: string | null;
};

function formatDateSydney(iso: string | null) {
  if (!iso) return "TBA";
  const d = new Date(iso);
  return new Intl.DateTimeFormat("en-AU", {
    timeZone: "Australia/Sydney",
    year: "numeric",
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(d);
}

function FlipCard({ r }: { r: RoundRow }) {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <div
      className="flip-card-container"
      onClick={() => setIsFlipped((v) => !v)}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") setIsFlipped((v) => !v);
      }}
    >
      <div className={`flip-card-inner ${isFlipped ? "is-flipped" : ""}`}>
        {/* FRONT */}
        <div className="flip-card-front">
          <div className="round-badge">Round {r.RoundNumber}</div>
          <h3 className="round-title">{r.Location}</h3>
          <p className="round-subtitle">{r.Country}</p>
          <p className="hint">Click to view date</p>
        </div>

        {/* BACK */}
        <div className="flip-card-back">
          <h3 className="back-title">Race Date</h3>
          <div className="detail-row">
            <span className="label">Start (Sydney)</span>
            <span className="value">{formatDateSydney(r.Date)}</span>
          </div>

          <p className="hint">Click to flip back</p>
        </div>
      </div>
    </div>
  );
}

export default function Schedule() {
  const [roundsRaw, setRoundsRaw] = useState<RoundRow[]>([]);
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        setErr("");

        const res = await fetch(`${API_BASE}/f1data/getEventSchedule`, {
          cache: "no-store",
        });

        if (!res.ok) {
          const body = await res.text().catch(() => "");
          throw new Error(
            `${res.status} ${res.statusText}${body ? ` — ${body}` : ""}`
          );
        }

        const data = await res.json();
        setRoundsRaw(Array.isArray(data) ? data : []);
      } catch (e: any) {
        setErr(e?.message ?? "fetch error");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const rounds = useMemo(() => {
    const map = new Map<number, RoundRow>();

    for (const r of roundsRaw) {
      if (!r || typeof r.RoundNumber !== "number") continue;
      if (r.RoundNumber <= 0) continue;
      if (!map.has(r.RoundNumber)) {
        map.set(r.RoundNumber, r);
      }
    }

    return Array.from(map.values()).sort(
      (a, b) => a.RoundNumber - b.RoundNumber
    );
  }, [roundsRaw]);

  return (
    <main className="page">
      <header className="header">
        <h1 className="page-title">F1 Schedule</h1>
        <p className="page-subtitle">Click a card to flip</p>
      </header>

      {err && <p className="error">{err}</p>}
      {loading && <p className="status">Loading…</p>}
      {!loading && !err && rounds.length === 0 && (
        <p className="status">No rounds found.</p>
      )}

      <section className="cards-grid">
        {rounds.map((r) => (
          <FlipCard key={r.RoundNumber} r={r} />
        ))}
      </section>
    </main>
  );
}
