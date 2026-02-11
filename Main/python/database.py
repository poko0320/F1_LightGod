from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client, Client

#import f1 data
import fastf1
from fastf1.core import Laps
import pandas as pd

import requests

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
standingUrl = os.environ.get("STANDING_URL")
standingHeaders = {
    "x-rapidapi-key": os.environ.get("RAPIDAPI_KEY"),
    "x-rapidapi-host": os.environ.get("RAPIDAPI_HOST"),
}

supabase: Client = create_client(url, key)

#table Driver and Team 
def addDriver(name: str, driver_Num: int, team: str):
    resp = supabase.table("Driver").insert({
        "name": name,
        "driver_Num": driver_Num,
        "team": team
    }).execute()
    print("addDriver:", resp.data)

def addTeam(name: str):
    # fetch drivers (name + points) for this team
    resp = supabase.table("Driver").select("name, points").eq("team", name).execute()
    print("select drivers:", resp.data)

    driver_names = [row["name"] for row in resp.data]
    total_points = sum((row.get("points") or 0) for row in resp.data)

    # insert team row
    resp2 = supabase.table("Team").insert({
        "name": name,
        "drivers": driver_names,   
        "points": total_points
    }).execute()
    print("addTeam:", resp2.data)

def addPoint(driverName: str, pointsAdd: int):
    res = supabase.table("Driver").select("name, points").eq("name", driverName).limit(1).execute()

    row = res.data[0]
    new_points = (row.get("points") or 0) + pointsAdd
    upd = supabase.table("Driver").update({"points": new_points}).eq("name", row["name"]).execute()

def subPoint(driverName: str, pointsAdd: int):
    res = supabase.table("Driver").select("name, points").eq("name", driverName).limit(1).execute()

    row = res.data[0]
    new_points = (row.get("points") or 0) - pointsAdd
    upd = supabase.table("Driver").update({"points": new_points}).eq("name", row["name"]).execute()

#table PlayerResult
def addPlayerPredict(playerName: str, raceCode: str, p1: int, p2: int, p3: int, p4: int, p5: int, p6: int, p7: int, p8: int, p9: int, p10: int, spec: int):
    check = supabase.table("Player_predict").select("player_name").eq("player_name", playerName).eq("RaceCode", raceCode).execute()
    lenCheck = len(check.data)
    if(lenCheck <1):
        resp = supabase.table("Player_predict").insert({"player_name": playerName, "RaceCode": raceCode,
                                                        "P1": p1,
                                                        "P2": p2,
                                                        "P3": p3,
                                                        "P4": p4,
                                                        "P5": p5,
                                                        "P6": p6,
                                                        "P7": p7,
                                                        "P8": p8,
                                                        "P9": p9,
                                                        "P10": p10,
                                                        "special": spec
                                                        }).execute()
        print("Player predict:", resp.data)
    else:
        print("error")
    
def editPlayerPredict(playerName: str, raceCode: str, column: str, value: int):
    check = supabase.table("Player_predict").update({column: value}).eq("player_name", playerName).eq("RaceCode", raceCode).execute()
    print("eddit:", column, value)

def testF1Data():
    session = fastf1.get_session(2021, 'Spanish Grand Prix', 'Q')
    session.load()

    DriverNumber = pd.unique(session.results.DriverNumber).tolist()
    resp = supabase.table("Qualify_result").insert({
        "race_name": f"{2021} Spanish Grand Prix",
        "driver_num": DriverNumber
    }).execute()

def updatePlayerQualifyPoint(raceCode: str):
    resp = supabase.table("User_points").select("player_name").execute()
    display_names = [row["player_name"] for row in resp.data]
    res_result = supabase.table("Qualify_result").select("driver_num").eq("race_name", raceCode).execute()
    res_result_data = res_result.data[0]
    res_result_data = res_result_data["driver_num"][:5]

    points = [25, 18, 15, 12, 10]
    for name in display_names:
        res_predict = supabase.table("Player_predict") \
            .select("P1, P2, P3, P4, P5") \
            .eq("RaceCode", raceCode) \
            .eq("player_name", name) \
            .execute()

        if not res_predict.data:
            continue  
        
        predictData = res_predict.data[0]
        predicted_top5 = [predictData[f"P{i}"] for i in range(1, 6)]

        for i in range(5):
            if(predicted_top5[i] == res_result_data[i]):
                resp2 = supabase.table("User_points").select("points").eq("player_name", name).execute()
                value = resp2.data[0]["points"] + points[i]
                supabase.table("User_points").update({"points": value}).eq("player_name", name).execute()
                

def get_and_store_driver_standings():
    r = requests.get((standingUrl +"/driverStandings"), headers=standingHeaders)
    if r.status_code != 200:
        print("Fetch error:", r.status_code, r.text)
        return

    data = r.json()
    drivers = data.get("drivers", [])
    if not drivers:
        print("No drivers in response")
        return

    rows = []
    for d in drivers:
        rows.append({
            "name": d.get("name"),
            "points": d.get("points", 0),
            "team": d.get("team"),
            # NEW:
            "standing": d.get("position"),  # the queue position / current standing
        })

    # remove empty names just in case
    rows = [row for row in rows if row["name"]]

    # Upsert (update on name conflict)
    resp = supabase.table("Driver").upsert(rows, on_conflict="name").execute()
    print("Upserted/updated:", len(resp.data))

def update_driver_standings():
    r = requests.get((standingUrl +"/driverStandings"), headers=standingHeaders)
    if r.status_code != 200:
        print("Fetch error:", r.status_code, r.text)
        return

    data = r.json()
    drivers = data.get("drivers", [])
    if not drivers:
        print("No drivers in response")
        return

    for d in drivers:
        name = d.get("name")
        standing = d.get("position")
        points = d.get("points", 0)

        if not name:
            continue  # skip invalid rows

        # Update only points & standing
        resp = (
            supabase.table("Driver")
            .update({"points": points, "standing": standing})
            .eq("name", name)   # match by driver name
            .execute()
        )

        if resp.data:
            print(f"Updated {name}: standing={standing}, points={points}")
        else:
            print(f"Skipped {name} (not found in table)")

def _fetch_team_standings():
    url = f"{standingUrl}/teamStandings"
    r = requests.get(url, headers=standingHeaders, timeout=20)
    r.raise_for_status()
    data = r.json()
    teams = data.get("teams", [])
    return teams

def seed_or_upsert_team_standings():
    try:
        teams = _fetch_team_standings()
        if not teams:
            print("No teams returned from API.")
            return

        rows = []
        for t in teams:
            name = t.get("name")
            if not name:
                continue
            rows.append({
                "name": name,
                "points": t.get("points", 0),
                "position": t.get("position"),
            })

        if not rows:
            print("No valid team rows to upsert.")
            return

        resp = supabase.table("Team").upsert(rows, on_conflict="name").execute()
        print(f"[Team] Upserted/updated rows: {len(resp.data)}")

    except requests.HTTPError as e:
        print("HTTP error while fetching team standings:", e, getattr(e, "response", None).text if hasattr(e, "response") else "")
    except Exception as e:
        print("Unexpected error in seed_or_upsert_team_standings:", e)

def update_team_standings():
    try:
        teams = _fetch_team_standings()
        if not teams:
            print("No teams returned from API.")
            return

        updated = 0
        skipped = 0
        for t in teams:
            name = t.get("name")
            if not name:
                continue

            points = t.get("points", 0)
            position = t.get("position")

            resp = (
                supabase.table("Team")
                .update({"points": points, "position": position})
                .eq("name", name)
                .execute()
            )
            if resp.data:
                updated += 1
            else:
                skipped += 1  # not found by name

        print(f"[Team] Updated: {updated}, Skipped (not found): {skipped}")

    except requests.HTTPError as e:
        print("HTTP error while fetching team standings:", e, getattr(e, "response", None).text if hasattr(e, "response") else "")
    except Exception as e:
        print("Unexpected error in update_team_standings:", e)
def update_year_schedule():
    data = fastf1.get_event_schedule(2026, include_testing=True, backend=None, force_ergast=False)
    data = data[['RoundNumber', 'Country', 'Location', 'Session5Date']].copy()

    # Convert pandas timestamps to ISO strings
    data['Session5Date'] = data['Session5Date'].apply(
        lambda x: x.isoformat() if pd.notna(x) else None
    )

    rows = []
    for row in data.itertuples(index=False):
        rows.append({
            "RoundNumber": int(row.RoundNumber) if pd.notna(row.RoundNumber) else None,
            "Country": row.Country,
            "Location": row.Location,
            "Date": row.Session5Date,
        })

    res = supabase.table("schedule").insert(rows).execute()
    print(res)

def test():
    resp = supabase.table("setting").select("RoundNumber, Country, Location, Date").single().execute()
    print(resp.data)

# Run
test()


