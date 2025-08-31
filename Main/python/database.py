from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client, Client

#import f1 data
import fastf1
from fastf1.core import Laps
import pandas as pd

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

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
                
            

# Run
test("2025 Netherlands Grand Prix")


