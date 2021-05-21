import numpy as np
import pandas as pd

import datetime as dt
from datetime import timedelta

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
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query dates and prcp from measurement
    #Calculate the date 1 year ago from the last data point in the database
    last_datapoint_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    A_year_before_last_datapoint_date = pd.to_datetime(last_datapoint_date[0]) - dt.timedelta(days = 365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= A_year_before_last_datapoint_date.strftime("%Y-%m-%d")).all()

    session.close()
    #Convert the query results to a dictionary using date as the key and prcp as the value
    temp_last_year ={}
    for date, temperature in results:
        temp_last_year[date] = temperature
    
    #Return the JSON representation of your dictionary
    return jsonify(temp_last_year)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query all stations
    results = session.query(Station.station).all()

    session.close()

    #Return a JSON list of stations from the dataset
    stations_list = list(np.ravel(results))

    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query the dates and temperature observations of the most active station for the last year of data
    last_datapoint_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    A_year_before_last_datapoint_date = pd.to_datetime(last_datapoint_date[0]) - dt.timedelta(days = 365)
    most_active_station = session.query(Station.station, func.count(Measurement.station)).filter(Station.station == Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == most_active_station[0]).filter(Measurement.date >= A_year_before_last_datapoint_date.strftime("%Y-%m-%d")).order_by(Measurement.date).all()

    session.close()

    #Return a JSON list of temperature observations (TOBS) for the previous year
    TOBS_list = []
    for date,tob in results:
        tob_dict ={}
        tob_dict['date'] = date
        tob_dict['tob'] = tob
        TOBS_list.append(tob_dict)
    
    return jsonify(TOBS_list)

@app.route("/api/v1.0/<start>")
def tobs_start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start
    #When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
    start_date = start

    last_datapoint_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    end_date = last_datapoint_date[0]
    
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    calc_tobs_list = []
    for tmin,tavg,tmax in result:
        calc_tob ={}
        calc_tob['TMIN'] = tmin
        calc_tob['TAVG'] = tavg
        calc_tob['TMAX'] = tmax
    
    return jsonify(calc_tobs_list)

    
@app.route("/api/v1.0/<start>/<end>")
def tobs_date_range(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range
    #When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive
    start_date = start
    end_date = end

    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    calc_tobs_list = []
    for tmin,tavg,tmax in result:
        calc_tob ={}
        calc_tob['TMIN'] = tmin
        calc_tob['TAVG'] = tavg
        calc_tob['TMAX'] = tmax
    
    return jsonify(calc_tobs_list)


if __name__ == "__main__":
    app.run(debug=True)