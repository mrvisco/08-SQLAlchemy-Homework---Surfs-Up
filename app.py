# Import Dependencies
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Setting up the Database

# Create engine using the 'hawaii.sqlite' database file created in database engineering
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup

# Create an instance of Flask app
app = Flask(__name__)

def convert_to_dict(query_result, label):
    data = []
    for record in query_result:
        data.append({'date': record[0], label: record[1]})
    return data

def get_most_recent_date():
    recent_date = session.query(Measurement).\
        order_by(Measurement.date.desc()).limit(1)

    for date in recent_date:
        most_recent_date = date.date

    return dt.datetime.strptime(most_recent_date, "%Y-%m-%d")

# #Flask Routes

# Create home route
@app.route("/")
def home(): 
    return (
        f"Welcome to the Hawaii Climate Analysis API<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Enter start and end date in the specified format for below:<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
    )
# Create the route to show precipitation
@app.route("/api/v1.0/precipitation")
def precip():
    """Return a list of the prior year rain fall""" 
    # Determine the last Date in the file
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    beg_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    rain = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= beg_date).\
        order_by(Measurement.date).all()
    precip={date:prcp for date,prcp in rain}
    # Return template and data
    return jsonify(precip)
    
# Create the route to show individual station numbers
@app.route("/api/v1.0/stations")
def statn():
    station_list = session.query(Measurement.station).distinct()
    return jsonify([station[0] for station in station_list])

@app.route("/api/v1.0/tobs")
def return_tobs():     
    most_recent_date = get_most_recent_date()
    one_year_ago = most_recent_date - dt.timedelta(days=365)
    recent_tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()
    return jsonify(convert_to_dict(recent_tobs_data, label='tobs'))

@app.route('/api/v1.0/<start_date>/<end_date>/')
def query_dates(start_date, end_date):
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    data_list = []
    for result in results:
        row = {}
        row["Start Date"] = start_date
        row["End Date"] = end_date
        row["Average Temperature"] = result[0]
        row["Highest Temperature"] = result[1]
        row["Lowest Temperature"] = result[2]
        data_list.append(row)
    return jsonify(data_list)

if __name__ == "__main__": 
    app.run(debug= True)   