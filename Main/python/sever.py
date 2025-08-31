from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flasgger import Swagger #make a api doc

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
swagger = Swagger(app)

#table Driver and Team 
@app.route("/addDriver", methods=["POST"])
def addDriver():
    ## api doc
    """
    Create a driver using JSON body.   
    ---
    tags: [Driver & Team]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [name, driver_Num, team]
          properties:
            name:       {type: string,  example: Yuki}
            driver_Num: {type: integer, example: 22}
            team:       {type: string,  example: "RedBull Racing"}
    responses:
      201: {description: Created}
      400: {description: Bad request}
    """
    data = request.get_json(force=True)
    name = data.get("name")
    driver_num = data.get("driver_Num")
    team = data.get("team")
    if not all([name, driver_num, team]):
        return jsonify({"ok": False, "error": "name, driver_Num, team are required"}), 400
    try:
        resp = supabase.table("Driver").insert({
            "name": name,
            "driver_Num": driver_num,
            "team": team
        }).execute()
        
        return jsonify(resp.data), 201
    except Exception as e:
        return jsonify(), 405

@app.route("/addTeam", methods=["POST"])
def addTeam():
    """
    Create a Team using JSON body.  
    ---
    tags: [Driver & Team]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [name]
          properties:
            name:       {type: string,  example: RedBull Racing}
    responses:
      201: {description: Created}
      400: {description: Bad request}
      405: {description: Error}
    """
    #get name from json 
    data = request.get_json(force=True)
    name = data.get("name")
    if not all([name]):
        return jsonify({"ok": False, "error": "team name are required"}), 400
    try:
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
        return jsonify(resp.data), 201
    except Exception as e:
        return jsonify(), 405

@app.route("/editPoint", methods=["PATCH"])
def editPoint():
    """
    add the driver points, auto update the team points.  
    ---
    tags: [Driver & Team]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [driverName, pointsEdit, add]
          properties:
            driverName:         {type: string,  example: Yuki}
            pointsEdit:         {type: int,  example: 10}
            add:                {type: boolean, example: true, description: true=add, false=subtract}

    responses:
      200: {description: Edited}
      400: {description: Bad request}
      405: {description: Error}
    """
    #get name from json 
    data = request.get_json(force=True)
    driverName = data.get("driverName")
    pointsEdit = data.get("pointsEdit")
    add = data.get("add")
    if driverName is None or pointsEdit is None or add is None:
        return jsonify({"ok": False, "error": "driverName, pointsEdit, add are required"}), 400
    try:
        #edit driver table
        res = supabase.table("Driver").select("name, points, team").eq("name", driverName).limit(1).execute()

        row = res.data[0]
        if(add):
            new_points = (row.get("points") or 0) + pointsEdit
        else:
            new_points = (row.get("points") or 0) - pointsEdit
        upd = supabase.table("Driver").update({"points": new_points}).eq("name", row["name"]).execute()

        #edit team table
        team = row.get("team")
        res2 = supabase.table("Team").select("points").eq("name", team).limit(1).execute()
        row = res2.data[0]
        if(add):
            new_points = (row.get("points") or 0) + pointsEdit
        else:
            new_points = (row.get("points") or 0) - pointsEdit
        upd2 = supabase.table("Team").update({"points": new_points}).eq("name", team).execute()
        
        return jsonify(), 200
    except Exception as e:
        return jsonify(), 405

#table PlayerResult
@app.route("/addPlayerPredict", methods=["POST"])
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
      405: {description: Error}
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
            return jsonify(resp.data), 201
        else:
            return jsonify(),500
    except Exception as e:
        return jsonify(), 405

@app.route("/editPlayerPredict", methods=["PATCH"])
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

#-------------------login----------------------
@app.post("/auth/signup")
def signup():
    """
    Sign up with email & password.
    ---
    tags: [Auth]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [email, password, display_name]
          properties:
            email:    {type: string, example: user@example.com}
            password: {type: string, example: StrongPassw0rd!}
            display_name: {type: string, example: Josh}
    responses:
      200: {description: Signed up (need email confirm)}
      400: {description: Error}
    """
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")
    display_name = data.get("display_name")
    if not email or not password:
        return {"ok": False, "error": "email and password required"}, 400
    try:
        resp = supabase.auth.sign_up({"email": email, "password": password, "options": {
                "data": {          
                    "Display name": display_name
                }
            }})
        
        resp2 = supabase.table("User_points").insert({"player_name": display_name}).execute()
        return {}, 200
    except Exception as e:
        return {"ok": False, "error": str(e)}, 400


@app.post("/auth/login")
def login():
    """
    Log in with email & password.
    ---
    tags: [Auth]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [email, password]
          properties:
            email:    {type: string, example: user@example.com}
            password: {type: string, example: StrongPassw0rd!}
    responses:
      200: {description: Logged in}
      400: {description: Error}
    """
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return {"ok": False, "error": "email and password required"}, 400
    try:
        session = supabase.auth.sign_in_with_password({"email": email, "password": password})
    
        access_token = session.session.access_token
        refresh_token = session.session.refresh_token

        return {"ok": True, "access_token": access_token, "refresh_token": refresh_token}, 200

    except Exception as e:
        return {"ok": False, "error": str(e)}, 400

#-----------f1 data get and update player points-------------------
@app.post("/qualify/updateResult")
def addQualifyResult():
  """
    Create a driver using JSON body.   
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

#run_surver
if __name__ == "__main__":
    app.run(debug=True)