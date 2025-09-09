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

ALLOWED_ORIGINS = [
    "https://f1lightgod.com",
    "https://www.f1lightgod.com",
    # dev / preview origins (optional but handy)
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # "https://*.vercel.app",   # flask-cors doesn't support wildcards in list
]

CORS(
    app,
    resources={
        r"/player/*": {"origins": ALLOWED_ORIGINS},
        r"/f1data/*": {"origins": ALLOWED_ORIGINS},
        r"/driver/*": {"origins": ALLOWED_ORIGINS},
        r"/setting/*": {"origins": ALLOWED_ORIGINS},
    },
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Length"],
    supports_credentials=True,
)

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
#run_surver
if __name__ == "__main__":
    app.run(debug=True)
