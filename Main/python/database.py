from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

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
    
# Run
addPoint("Yuki", 20)


