# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 20:05:29 2020

@author: sarah
"""

import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    """Return the precipitation data as json"""
    all_prcp = []
    for date, prcpdata in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcpdata
        all_prcp.append(prcp_dict)
        
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name).all()    
    session.close()
    """Return the station data as json"""
    all_stations = []
    for statid, name in results:
        station_dict = {}
        station_dict["stationid"] = statid
        station_dict["stationname"] = name
        all_stations.append(station_dict)
        
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()
    session.close()
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    all_tobs = []
    for date, temp in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temp"] = temp
        all_tobs.append(temp_dict)
    return jsonify(all_tobs)



@app.route("/api/v1.0/<start>")
def startdate(start):
    session = Session(engine)
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
 # go back one year from start date and go to end of data for Min/Avg/Max temp   
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    start_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close()
    trip = list(np.ravel(start_data))
    return jsonify(trip)


@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    session = Session(engine)
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
 # go back one year from start date and go to end of data for Min/Avg/Max temp   
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end, '%Y-%m-%d')
    startend_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    trip2 = list(np.ravel(startend_data))
    return jsonify(trip2)


@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/></n>"
        f"<br/></n>"
        f"/api/v1.0/precipitation<br/></n>"
        f"Return the precipitation data as json"
        f"<br/></n>"        
        f"/api/v1.0/stations<br/></n>"
        f"Return the station data as json"
        f"<br/></n>"
        f"/api/v1.0/tobs<br/></n>"
        f"Return a JSON list of Temperature Observations (tobs) for the previous year."
        f"<br/></n>"        
        f"/api/v1.0/start<br/>"
        f"When given the start date (YYYY-MM-DD), calculates the MIN/AVG/MAX temperature for all dates after start date<br/>"           
        f"/api/v1.0/start/end<br/>"
        f"Given a start and an end date (YYYY-MM-DD), calculates the MIN/AVG/MAX temperature for dates between two dates<br/>"
    )


if __name__ == "__main__":
    app.run(debug=True)
