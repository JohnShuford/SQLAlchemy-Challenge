import numpy as np

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #create a session link
    session = Session(engine)

    #query for the date and precipitation
    weather = session.query(Measurement.date, Measurement.prcp).all()

    #close out the session
    session.close

    #create the dictionary from the queried data
    weather_all = []
    for date, prcp in weather:
        weather_dict = {}
        weather_dict['date'] = date
        weather_dict['prcp'] = prcp
        weather_all.append(weather_dict)

    #return a jsonified object
    return jsonify(weather_all)

@app.route('/api/v1.0/stations')
def stations():
    #create a session link
    session = Session(engine)

    #query for the date and precipitation
    station = session.query(Station.name).all()

    #close out the session
    session.close

    #convert the list of tuples to normal lists
    station_names = list(np.ravel(station))

    #return the list jsonified
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    #create a session link
    session = Session(engine)

    #query for the date and precipitation
    tobs = session.query(Measurement.tobs).filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.station == 'USC00519281').all()

    #close out the session
    session.close

    #create a lits from the query
    tobs_all = list(np.ravel(tobs))

    #return the list jsonified
    return jsonify(tobs_all)

# @app.route("/api/v1.0/<start>")
# @app.route("/api/v1.0/<start>/<end>")
# def name(start = None, end=None):
    

if __name__ == '__main__':
    app.run(debug=True)