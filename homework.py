import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Dictionary 
#queryresults = [
 #   {key:prcp}

Base = automap_base()
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine) 

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/date/<start><br/>"
        f"/api/v1.0/date/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
     print("Server received request for 'Precipitation' page...")
     lastyear = dt.date(2017,8,23)-dt.timedelta(days=365)
     queryresults = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=lastyear).all()
     return jsonify(queryresults)


@app.route("/api/v1.0/stations")
def station():
    print("Server received request for 'Station' Page")
    queryresults = session.query(Station.station).all()
    return jsonify(queryresults)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Tobs' Page")
    lastyear = dt.date(2017,8,23)-dt.timedelta(days=365)
    queryresults = session.query(Measurement.tobs).filter(Measurement.date>=lastyear).\
    filter(Measurement.station == "USC00519281").all()
    return jsonify(queryresults)

@app.route("/api/v1.0/date/<start>")
def startdate(start):
    print("Server received request for 'Start' Page")
    print(start)
    session = Session(engine)
    queryresults = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), 
              func.avg(Measurement.tobs).filter(Measurement.date>=start)).all()
    for min, max, avg in queryresults:
        querydates = {}
        querydates["min"]=min 
        querydates["max"]=max 
        querydates["avg"]=avg
    return jsonify(querydates)

@app.route("/api/v1.0/date/<start>/<end>")
def enddate(start, end):
    print("Server received request for 'End' Page")
    session = Session(engine)
    queryresults = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), 
              func.avg(Measurement.tobs).filter(Measurement.date>=start).filter(Measurement.date>=end)).all()
    for min, max, avg in queryresults:
        querydates = {}
        querydates["min"]=min 
        querydates["max"]=max 
        querydates["avg"]=avg 
    return jsonify(querydates)


if __name__ == "__main__":
    app.run(debug=True)