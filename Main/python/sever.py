from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

#Flask
app = Flask(__name__)

#table Driver and Team 
@app.route("/addDriver/<name>/<int:driver_Num>/<team>")
def addDriver(name: str, driver_Num: int, team: str):
    data = request.get_json(force=True)
    name = data.get("name")
    driver_num = data.get("driver_Num")
    team = data.get("team")
    if not all([name, driver_num, team]):
        return jsonify({"ok": False, "error": "name, driver_Num, team are required"}), 400
    try:
        resp = supabase.table("Driver").insert({
            "name": name,
            "driver_Num": driver_Num,
            "team": team
        }).execute()
        
        return jsonify(resp.data), 200
    except Exception as e:
        return jsonify(), 405

@app.route("/addTeam/<name>")
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


#run_surver
if __name__ == "__main__":
    app.run(debug=True)