from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flasgger import Swagger #make a api doc
from flask_cors import CORS

load_dotenv()

import os
from supabase import create_client, Client

import fastf1
from fastf1.core import Laps
import pandas as pd

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

#Flask
app = Flask(__name__)

CORS(app, resources={r"/player/*": {"origins": ["http://localhost:3000"]}})
CORS(app, resources={r"/f1data/*": {"origins": ["http://localhost:3000"]}})
CORS(app, resources={r"/driver/*": {"origins": ["http://localhost:3000"]}})
CORS(app, resources={r"/setting/*": {"origins": ["http://localhost:3000"]}})
# CORS(app, resources={r"/player/*": {"origins": ["http://f1lightgod"]}})
# CORS(app, resources={r"/f1data/*": {"origins": ["http://f1lightgod"]}})
# CORS(app, resources={r"/driver/*": {"origins": ["http://f1lightgod"]}})
# CORS(app, resources={r"/setting/*": {"origins": ["http://f1lightgod"]}})

swagger = Swagger(app)

@app.route("/player/addPlayerToPlayerStanding", methods=["POST"])
def addPlayerToPlayerStanding():
    """
    add Player PlayerStanding.  
    ---
    tags: [Player]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [playerName]
          properties:
            playerName:
              type: string
              example: Josh
    responses:
      201:
        description: Created
      400:
        description: Bad request
      409:
        description: Error already have
      500:
        description: Server error
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"ok": False, "error": "Invalid or missing JSON body"}), 400

    playerName = (data.get("playerName") or "").strip()
    if not playerName:
        return jsonify({"ok": False, "error": "playerName is required"}), 400

    try:
        existing = (
            supabase.table("User_points")
            .select("player_name")
            .eq("player_name", playerName)
            .execute()
        )
        if existing.data and len(existing.data) > 0:
            return jsonify({"ok": False, "error": "Player already exists"}), 409

        resp = (
            supabase.table("User_points")
            .insert({"player_name": playerName})
            .execute()
        )
        return jsonify({"ok": True, "data": resp.data}), 201

    except Exception as e:
        msg = str(e)
        if "duplicate" in msg.lower() or "unique" in msg.lower():
            return jsonify({"ok": False, "error": "Player already exists"}), 409
        return jsonify({"ok": False, "error": msg}), 500
  
  

#table PlayerResult
@app.route("/player/addPlayerPredict", methods=["POST"])
def addPlayerPredict():
    """
    add Player Predict.  
    ---
    tags: [Player]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [playerName, raceCode, p1, p2, p3, p4, p5, spec]
          properties:
            playerName:       {type: string,  example: Josh}
            raceCode:         {type: string,  example: 2025 Monza}
            p1:               {type: int,  example: 1}
            p2:               {type: int,  example: 2}
            p3:               {type: int,  example: 3}
            p4:               {type: int,  example: 4}
            p5:               {type: int,  example: 5}
            spec:             {type: int,  example: 6}
    responses:
      201: {description: Created}
      400: {description: Bad request}
      409: {description: Error}
      500: {might already appear}
    """
    data = request.get_json(force=True)
    playerName = data.get("playerName")
    raceCode = data.get("raceCode")
    p1 = data.get("p1")
    p2 = data.get("p2")
    p3 = data.get("p3")
    p4 = data.get("p4")
    p5 = data.get("p5")
    spec = data.get("spec")
    if not all([playerName, raceCode, p1, p2, p3, p4, p5, spec]):
        print(playerName, raceCode, p1, p2, p3, p4, p5, spec)
        return jsonify({"ok": False, "error": "json error"}), 400
    try:
        check = supabase.table("Player_predict").select("player_name").eq("player_name", playerName).eq("RaceCode", raceCode).execute()
        lenCheck = len(check.data)
        if(lenCheck <1):
            resp = supabase.table("Player_predict").insert({"player_name": playerName, "RaceCode": raceCode,
                                                            "P1": p1,
                                                            "P2": p2,
                                                            "P3": p3,
                                                            "P4": p4,
                                                            "P5": p5,
                                                            "special": spec
                                                            }).execute()
            return jsonify({"ok": True, "data": resp.data}), 201
        else:
          check = supabase.table("Player_predict").update({"P1": p1,
                                                            "P2": p2,
                                                            "P3": p3,
                                                            "P4": p4,
                                                            "P5": p5,
                                                            "special": spec}).eq("player_name", playerName).eq("RaceCode", raceCode).execute()
          return jsonify({"ok": True, "data": check.data}), 201
    except Exception as e:
        print(str(e))
        return jsonify({"ok": False, "error": str(e)}),  500

@app.route("/player/editPlayerPredict", methods=["PATCH"])
def editPlayerPredict():
    """
    edit Player Predict.  
    ---
    tags: [Player]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [playerName, raceCode, column, value]
          properties:
            playerName:       {type: string,  example: Josh}
            raceCode:         {type: string,  example: 2025 Monza}
            column:           {type: string,  example: P1}
            value:            {type: int,  example: 10}
    responses:
      200: {description: Done}
      400: {description: Bad request}
      405: {description: Error}
    """
    data = request.get_json(force=True)
    playerName = data.get("playerName")
    raceCode = data.get("raceCode")
    column = data.get("column")
    value = data.get("value")
    if not all([playerName, raceCode, column, value]):
        return jsonify({"ok": False, "error": "json error"}), 400
    try:
        check = supabase.table("Player_predict").update({column: value}).eq("player_name", playerName).eq("RaceCode", raceCode).execute()
        print("eddit:", column, value)
        return jsonify(), 200
    except Exception as e:
        return jsonify(), 405

@app.route("/player/updatePoint", methods=["PUT"])
def updatePoint():
  """
    update Player Point.  
    ---
    tags: [Player]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [raceCode]
          properties:
            raceCode:         {type: string,  example: 2025 Spanish Grand Prix}
    responses:
      200: {description: Done}
      400: {description: Bad request}
      405: {description: Error}
  """
  data = request.get_json(force=True)
  raceCode = data.get("raceCode")
  if not all([raceCode]):
        return jsonify({"ok": False, "error": "json error"}), 400

  try:
    resp = supabase.table("User_points").select("player_name").execute()
    display_names = [row["player_name"] for row in resp.data]
    res_result = supabase.table("Qualify_result").select("driver_num").eq("race_name", raceCode).execute()
    res_result_data = res_result.data[0]["driver_num"][:5]

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
    return jsonify(), 200
  except Exception as e:
        return jsonify({"error": e}), 405

#-----------f1 data get and update player points-------------------
@app.post("/f1data/qualify/updateResult")
def addQualifyResult():
  """
    Create a QualifyResult using JSON body.   
    ---
    tags: [F1Data]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [race_name, driver_num]
          properties:
            race_year: {type: integer, example: 2021}
            race_name:       {type: str, example: Spanish Grand Prix}
    responses:
      201: {description: Created}
      400: {description: Bad request}
  """
  data = request.get_json(silent=True) or {}
  race_year = data.get("race_year")
  race_name = data.get("race_name")

  if not race_name or not race_year:
        return {"ok": False, "error": "race_name, driver_num required"}, 400

  try:
    session = fastf1.get_session(race_year, race_name, 'Q')
    session.load()

    DriverNumber = pd.unique(session.results.DriverNumber).tolist()
    resp = supabase.table("Qualify_result").insert({
      "race_name": f"{race_year} {race_name}",
      "driver_num": DriverNumber
    }).execute()
    return {}, 201
  except Exception as e:
        return {"ok": False, "error": str(e)}, 400

@app.get("/driver/get")
def getDriverStand():
  """
    
    ---
    tags: [F1Data]
    parameters:
      - in: 
    responses:
      200: {description: Created}
      500: {description: error}
  """
  try:
    resp = supabase.table("Driver").select("*").order("standing", desc=False).execute()
    print(resp.data)
    return {"drivers": resp.data}, 200
  except Exception as e:
        return jsonify({"error": e}), 500

@app.get("/player/getTOP10")
def getPlayerStand():
  """
    
    ---
    tags: [Player]
    parameters:
      - in: 
    responses:
      200: {description: Created}
      500: {description: error}
  """

  try:
    resp = supabase.table("User_points").select("*").order("points", desc=True, nullsfirst=False).limit(10).execute()
    print(resp.data)
    return {"player": resp.data}, 200
  except Exception as e:
        return jsonify({"error": e}), 500

@app.get("/player/getPoint/<string:player_name>")
def getPlayerPoint(player_name: str):
  """
    
    ---
    tags: [Player]
    parameters:
      - in: 
    responses:
      200: {description: Created}
      500: {description: error}
  """
  try:
    resp = supabase.table("User_points").select("points").eq("player_name", player_name).execute()
    print(resp.data)
    return {"points": resp.data}
  except Exception as e:
        return jsonify({"error": e}), 500
  
@app.get("/player/getCurrentPredict/<string:player_name>")
def getCurrentPredict(player_name: str):
  """
    
    ---
    tags: [Player]
    parameters:
      - in: 
    responses:
      200: {description: Created}
      500: {description: error}
  """
  try:
    resp = supabase.table("Player_predict").select("*").eq("player_name", player_name).execute()
    print(resp.data)
    return {"predicts": resp.data}
  except Exception as e:
        return jsonify({"error": e}), 500
  
@app.get("/player/getDashboardData/<string:player_name>")
def getDashboardData(player_name: str):
  """
    
    ---
    tags: [Player]
    parameters:
      - in: 
    responses:
      200: {description: Created}
      500: {description: error}
  """
  try:
    resp = supabase.table("User_points").select("points").eq("player_name", player_name).execute()
    resp2 = supabase.table("Player_predict").select("*").eq("player_name", player_name).execute()
    print(resp.data + resp2.data)
    return {"points": resp.data, "predicts": resp2.data}
  except Exception as e:
        return jsonify({"error": e}), 500
  
@app.get("/setting/racecode")
def getRaceCode():
  """
    ---
    tags: [Setting]
    parameters:
      - in: 
    responses:
      200: {description: Created}
      500: {description: error}
  """
  try:
    res = (
            supabase
            .table("setting")             
            .select("raceCode")           
            .eq("version", "1.1")         
            .limit(1)
            .execute()
        )
    return {"raceCode":  res.data[0].get("raceCode")}
  except Exception as e:
        return jsonify({"error": e}), 500

    
@app.route("/driver/calculateChampionshipScenario", methods=["POST"])
def calculateChampionshipScenario():
    """
      Calculate championship scenario for Max, Norris, and Oscar
      ---
      tags: [Driver]
      parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            required: [remainRace, maxPositions, norrisPositions, oscarPositions]
            properties:
              maxPositions:
                type: array
                items:
                  type: integer
                example: [1, 1, 2, 1, 3, 1]
              norrisPositions:
                type: array
                items:
                  type: integer
                example: [2, 3, 1, 2, 2, 2]
              oscarPositions:
                type: array
                items:
                  type: integer
                example: [3, 2, 3, 3, 1, 3]
              maxSprintPositions:
                type: array
                items:
                  type: integer
                example: [1, 2]
              norrisSprintPositions:
                type: array
                items:
                  type: integer
                example: [2, 1]
              oscarSprintPositions:
                type: array
                items:
                  type: integer
                example: [3, 3]
      responses:
        200: {description: Success}
        400: {description: Bad request}
        500: {description: Server error}
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"ok": False, "error": "Invalid JSON"}), 400

    max_positions = data.get("maxPositions", []) or []
    norris_positions = data.get("norrisPositions", []) or []
    oscar_positions = data.get("oscarPositions", []) or []
    max_sprint_positions = data.get("maxSprintPositions", []) or []
    norris_sprint_positions = data.get("norrisSprintPositions", []) or []
    oscar_sprint_positions = data.get("oscarSprintPositions", []) or []

    # ---- fetch settings (remain counts + current wins) ----
    settings_resp = supabase.table("setting").select(
        "remainRace, remainSprint, maxWin, norisWin, oscarWin"
    ).single().execute()

    if not settings_resp.data:
        return jsonify({"ok": False, "error": "No settings row found"}), 500

    remain_race = int(settings_resp.data.get("remainRace", 0))
    remain_sprint = int(settings_resp.data.get("remainSprint", 0))
    current_max_wins = int(settings_resp.data.get("maxWin", 0))
    current_norris_wins = int(settings_resp.data.get("norisWin", 0))  # column name as given
    current_oscar_wins = int(settings_resp.data.get("oscarWin", 0))

    # ---- validate lengths ----
    if any(len(lst) != remain_race for lst in [max_positions, norris_positions, oscar_positions]):
        return jsonify(
            ok=False,
            error="Position arrays must match remainRace length",
            remainRace=remain_race
        ), 400

    if remain_sprint > 0 and any(
        len(lst) != remain_sprint
        for lst in [max_sprint_positions, norris_sprint_positions, oscar_sprint_positions]
    ):
        return jsonify(ok=False, error="Sprint position arrays must match remainSprint length",
                       remainSprint=remain_sprint), 400

    # ---- points tables ----
    position_points = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
    sprint_points   = {1:  8, 2:  7, 3:  6, 4:  5, 5:  4, 6: 3, 7: 2, 8: 1}

    try:
        # ---- current driver points ----
        drivers_resp = supabase.table("Driver").select("driver_Num, name, points").execute()
        drivers_data = {d["driver_Num"]: d for d in (drivers_resp.data or [])}

        max_driver    = next((d for d in drivers_resp.data if "Verstappen" in d.get("name","")), None)
        norris_driver = next((d for d in drivers_resp.data if "Norris"     in d.get("name","")), None)
        oscar_driver  = next((d for d in drivers_resp.data if "Piastri"    in d.get("name","")), None)

        if not all([max_driver, norris_driver, oscar_driver]):
            return jsonify({"ok": False, "error": "Could not find all drivers"}), 400

        # ---- projected points ----
        max_race_projected    = sum(position_points.get(p, 0) for p in max_positions)
        norris_race_projected = sum(position_points.get(p, 0) for p in norris_positions)
        oscar_race_projected  = sum(position_points.get(p, 0) for p in oscar_positions)

        max_sprint_projected    = sum(sprint_points.get(p, 0) for p in max_sprint_positions)
        norris_sprint_projected = sum(sprint_points.get(p, 0) for p in norris_sprint_positions)
        oscar_sprint_projected  = sum(sprint_points.get(p, 0) for p in oscar_sprint_positions)

        max_projected    = max_race_projected    + max_sprint_projected
        norris_projected = norris_race_projected + norris_sprint_projected
        oscar_projected  = oscar_race_projected  + oscar_sprint_projected

        max_current_pts    = int(max_driver.get("points", 0))
        norris_current_pts = int(norris_driver.get("points", 0))
        oscar_current_pts  = int(oscar_driver.get("points", 0))

        max_final    = max_current_pts    + max_projected
        norris_final = norris_current_pts + norris_projected
        oscar_final  = oscar_current_pts  + oscar_projected

        # ---- tie-break wins (current + projected) ----
        max_race_wins    = sum(1 for p in max_positions if p == 1)
        norris_race_wins = sum(1 for p in norris_positions if p == 1)
        oscar_race_wins  = sum(1 for p in oscar_positions if p == 1)

        max_sprint_wins    = sum(1 for p in max_sprint_positions if p == 1)
        norris_sprint_wins = sum(1 for p in norris_sprint_positions if p == 1)
        oscar_sprint_wins  = sum(1 for p in oscar_sprint_positions if p == 1)

        max_total_wins    = current_max_wins    + max_race_wins    + max_sprint_wins
        norris_total_wins = current_norris_wins + norris_race_wins + norris_sprint_wins
        oscar_total_wins  = current_oscar_wins  + oscar_race_wins  + oscar_sprint_wins

        contenders = [
            {"key": "max",    "name": "Max",    "points": max_final,    "wins": max_total_wins},
            {"key": "norris", "name": "Norris", "points": norris_final, "wins": norris_total_wins},
            {"key": "oscar",  "name": "Oscar",  "points": oscar_final,  "wins": oscar_total_wins},
        ]

        top_points = max(c["points"] for c in contenders)
        top_contenders = [c for c in contenders if c["points"] == top_points]

        if len(top_contenders) == 1:
            winner = top_contenders[0]
            winner_reason = "points"
        else:
            top_wins = max(c["wins"] for c in top_contenders)
            winners_by_wins = [c for c in top_contenders if c["wins"] == top_wins]
            if len(winners_by_wins) == 1:
                winner = winners_by_wins[0]
                winner_reason = "wins"
            else:
                # still tied -> stable order fallback
                order = {"max": 0, "norris": 1, "oscar": 2}
                winner = sorted(winners_by_wins, key=lambda c: order[c["key"]])[0]
                winner_reason = "stable-order"

        return jsonify({
            "ok": True,
            "winner": winner["name"],
            "winnerReason": winner_reason,
            "maxFinalPoints": max_final,
            "norrisFinalPoints": norris_final,
            "oscarFinalPoints": oscar_final,
            "breakdown": {
                "max": {
                    "currentPoints": max_current_pts,
                    "projectedRacePoints": max_race_projected,
                    "projectedSprintPoints": max_sprint_projected,
                    "projectedTotalPoints": max_projected,
                    "finalPoints": max_final,
                    "currentWins": current_max_wins,
                    "projectedRaceWins": max_race_wins,
                    "projectedSprintWins": max_sprint_wins,
                    "totalWinsForTieBreak": max_total_wins
                },
                "norris": {
                    "currentPoints": norris_current_pts,
                    "projectedRacePoints": norris_race_projected,
                    "projectedSprintPoints": norris_sprint_projected,
                    "projectedTotalPoints": norris_projected,
                    "finalPoints": norris_final,
                    "currentWins": current_norris_wins,
                    "projectedRaceWins": norris_race_wins,
                    "projectedSprintWins": norris_sprint_wins,
                    "totalWinsForTieBreak": norris_total_wins
                },
                "oscar": {
                    "currentPoints": oscar_current_pts,
                    "projectedRacePoints": oscar_race_projected,
                    "projectedSprintPoints": oscar_sprint_projected,
                    "projectedTotalPoints": oscar_projected,
                    "finalPoints": oscar_final,
                    "currentWins": current_oscar_wins,
                    "projectedRaceWins": oscar_race_wins,
                    "projectedSprintWins": oscar_sprint_wins,
                    "totalWinsForTieBreak": oscar_total_wins
                }
            }
        }), 200

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/setting/getRemain", methods=["GET"])
def getRemain():
  """
    
    ---
    tags: [Setting]
    parameters:
      - in: 
    responses:
      200: {description: Created}
      500: {description: error}
  """
  resp = supabase.table("setting").select("remainRace, remainSprint").single().execute()
  if resp.data:
    return jsonify(resp.data), 200
  else:
      return jsonify({"ok": False, "error": "No setting found"}), 404

@app.route("/f1data/getEventSchedule", methods=["GET"])
def get_event_schedule():
  """
    
    ---
    tags: [F1Data]
    parameters:
      - in: 
    responses:
      200: {description: Created}
      404: {description: error}
  """
  resp = supabase.table("schedule").select("RoundNumber, Country, Location, Date").execute()
  if resp.data:
    return jsonify(resp.data), 200
  else:
      return jsonify({"ok": False, "error": "No setting found"}), 404
#run_surver
if __name__ == "__main__":
    app.run(debug=True)
