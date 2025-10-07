'use client';
import React, { useEffect, useMemo, useState } from "react";

interface SettingsResponse {
  remainRace: number;
  remainSprint: number;
}

interface CalcResponseOk {
  ok: true;
  winner: string;
  maxFinalPoints: number;
  norrisFinalPoints: number;
  oscarFinalPoints: number;
  breakdown: {
    max: Record<string, number>;
    norris: Record<string, number>;
    oscar: Record<string, number>;
  };
}

interface CalcResponseErr {
  ok: false;
  error: string;
  remainRace?: number;
  remainSprint?: number;
}

type CalcResponse = CalcResponseOk | CalcResponseErr;
type DriverKey = "max" | "norris" | "oscar";
const DRIVER_LABELS: Record<DriverKey, string> = {
  max: "Max Verstappen",
  norris: "Lando Norris",
  oscar: "Oscar Piastri",
};

// --- ✅ Safe API Base joiner
const RAW_BASE = process.env.NEXT_PUBLIC_OWN_API || "";
const API_BASE = RAW_BASE.replace(/\/+$/, "");
const join = (path: string) => `${API_BASE}${path.startsWith("/") ? path : `/${path}`}`;

export default function ChampionshipScenarioForm({
  settingsUrl = join("/setting/getRemain"),
  calculateUrl = join("/driver/calculateChampionshipScenario"),
}: {
  settingsUrl?: string;
  calculateUrl?: string;
}) {
  const [loadingSettings, setLoadingSettings] = useState(true);
  const [settingsError, setSettingsError] = useState<string | null>(null);
  const [remainRace, setRemainRace] = useState<number>(0);
  const [remainSprint, setRemainSprint] = useState<number>(0);

  const [racePositions, setRacePositions] = useState<Record<DriverKey, (number | "")[]>>({
    max: [], norris: [], oscar: [],
  });
  const [sprintPositions, setSprintPositions] = useState<Record<DriverKey, (number | "")[]>>({
    max: [], norris: [], oscar: [],
  });

  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [result, setResult] = useState<CalcResponseOk | null>(null);

  // ---- Load settings on mount
  useEffect(() => {
    let cancel = false;
    (async () => {
      try {
        setLoadingSettings(true);
        const res = await fetch(settingsUrl, { cache: "no-store" });
        if (!res.ok) throw new Error(`Settings load failed (${res.status})`);
        const data: SettingsResponse = await res.json();

        if (!cancel) {
          const race = Number(data.remainRace ?? 0);
          const sprint = Number(data.remainSprint ?? 0);
          setRemainRace(race);
          setRemainSprint(sprint);
          setRacePositions({
            max: Array(race).fill(""),
            norris: Array(race).fill(""),
            oscar: Array(race).fill(""),
          });
          setSprintPositions({
            max: Array(sprint).fill(""),
            norris: Array(sprint).fill(""),
            oscar: Array(sprint).fill(""),
          });
        }
      } catch (e: any) {
        if (!cancel) setSettingsError(e?.message || "Failed to load settings");
      } finally {
        if (!cancel) setLoadingSettings(false);
      }
    })();
    return () => { cancel = true; };
  }, [settingsUrl]);

  // ---- Update position cells
  const updatePosition = (type: "race" | "sprint", driver: DriverKey, idx: number, value: string) => {
    const val = value === "" ? "" : Math.max(0, Math.min(20, Number(value)));
    const setter = type === "race" ? setRacePositions : setSprintPositions;
    setter((prev) => {
      const copy = { ...prev };
      const arr = [...copy[driver]];
      arr[idx] = (val as number) ?? "";
      copy[driver] = arr;
      return copy;
    });
  };

  // ---- Validation
  const canSubmit = useMemo(() => {
    const filled = (arr: (number | "")[]) => arr.every((x) => x !== "");
    const raceOk =
      remainRace === 0 ||
      (filled(racePositions.max) && filled(racePositions.norris) && filled(racePositions.oscar));
    const sprintOk =
      remainSprint === 0 ||
      (filled(sprintPositions.max) && filled(sprintPositions.norris) && filled(sprintPositions.oscar));
    return raceOk && sprintOk && !submitting;
  }, [racePositions, sprintPositions, remainRace, remainSprint, submitting]);

  // ---- Submit handler
  const handleSubmit = async () => {
    setSubmitting(true);
    setSubmitError(null);
    setResult(null);
    const payload = {
      maxPositions: racePositions.max.map(Number),
      norrisPositions: racePositions.norris.map(Number),
      oscarPositions: racePositions.oscar.map(Number),
      maxSprintPositions: sprintPositions.max.map(Number),
      norrisSprintPositions: sprintPositions.norris.map(Number),
      oscarSprintPositions: sprintPositions.oscar.map(Number),
    };

    try {
      const res = await fetch(calculateUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const json: CalcResponse = await res.json();
      if (!res.ok || !json.ok) throw new Error(json.ok ? `HTTP ${res.status}` : json.error);
      setResult(json);
    } catch (e: any) {
      setSubmitError(e?.message || "Network error");
    } finally {
      setSubmitting(false);
    }
  };

  // ---- Table render helper
  const renderGrid = (title: string, count: number, type: "race" | "sprint",
    values: Record<DriverKey, (number | "")[]>) => {
    if (count <= 0) return null;
    return (
      <div className="mt-6">
        <h3 className="text-lg font-semibold mb-2">{title}</h3>
        <div className="overflow-x-auto rounded-2xl shadow border">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-3 py-2 text-left font-medium">Round</th>
                {Object.keys(DRIVER_LABELS).map((k) => (
                  <th key={k} className="px-3 py-2 text-left font-medium">{DRIVER_LABELS[k as DriverKey]}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {Array.from({ length: count }).map((_, rIdx) => (
                <tr key={rIdx} className={rIdx % 2 ? "bg-white" : "bg-gray-50/50"}>
                  <td className="px-3 py-2 font-medium">{rIdx + 1}</td>
                  {(Object.keys(DRIVER_LABELS) as DriverKey[]).map((driver) => (
                    <td key={driver} className="px-3 py-2">
                      <input
                        type="number"
                        min={0}
                        max={20}
                        placeholder="pos"
                        value={(values[driver][rIdx] ?? "") as any}
                        onChange={(e) => updatePosition(type, driver, rIdx, e.target.value)}
                        className="w-24 rounded-xl border px-3 py-1 focus:outline-none focus:ring"
                      />
                      <p className="text-[11px] text-gray-500 mt-1">0 = no points/DNF</p>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  // ---- Render
  return (
    <div className="max-w-5xl mx-auto p-4">
      <h2 className="text-2xl font-bold">Championship Scenario Calculator</h2>
      <p className="text-gray-600 mt-1">Fill finishing positions, then calculate the projected winner.</p>

      {loadingSettings && <div className="mt-6 text-gray-700">Loading settings…</div>}
      {settingsError && <div className="mt-6 text-red-600">{settingsError}</div>}

      {!loadingSettings && !settingsError && (
        <>
          <div className="mt-4 grid grid-cols-2 gap-4">
            <div className="rounded-2xl border p-4">
              <p className="text-sm text-gray-700">
                <span className="font-semibold">Remaining Races:</span> {remainRace}
              </p>
              <p className="text-sm text-gray-700">
                <span className="font-semibold">Remaining Sprints:</span> {remainSprint}
              </p>
            </div>
          </div>

          {renderGrid("Race Positions", remainRace, "race", racePositions)}
          {renderGrid("Sprint Positions", remainSprint, "sprint", sprintPositions)}

          <div className="mt-6 flex items-center gap-3">
            <button
              disabled={!canSubmit}
              onClick={handleSubmit}
              className="rounded-2xl px-5 py-2 border shadow disabled:opacity-50"
            >
              {submitting ? "Calculating…" : "Calculate Winner"}
            </button>
            {submitError && <span className="text-red-600 text-sm">{submitError}</span>}
          </div>

          {result && (
            <div className="mt-6 rounded-2xl border p-4 shadow">
              <h3 className="text-xl font-semibold">Winner: {result.winner}</h3>
              <div className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="rounded-xl border p-3">
                  <h4 className="font-medium">Max</h4>
                  <ul className="text-sm text-gray-700 mt-2 space-y-1">
                    <li>Final Points: {result.maxFinalPoints}</li>
                    <li>Race Points: {result.breakdown.max.projectedRacePoints}</li>
                    <li>Sprint Points: {result.breakdown.max.projectedSprintPoints}</li>
                  </ul>
                </div>
                <div className="rounded-xl border p-3">
                  <h4 className="font-medium">Norris</h4>
                  <ul className="text-sm text-gray-700 mt-2 space-y-1">
                    <li>Final Points: {result.norrisFinalPoints}</li>
                    <li>Race Points: {result.breakdown.norris.projectedRacePoints}</li>
                    <li>Sprint Points: {result.breakdown.norris.projectedSprintPoints}</li>
                  </ul>
                </div>
                <div className="rounded-xl border p-3">
                  <h4 className="font-medium">Oscar</h4>
                  <ul className="text-sm text-gray-700 mt-2 space-y-1">
                    <li>Final Points: {result.oscarFinalPoints}</li>
                    <li>Race Points: {result.breakdown.oscar.projectedRacePoints}</li>
                    <li>Sprint Points: {result.breakdown.oscar.projectedSprintPoints}</li>
                  </ul>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}