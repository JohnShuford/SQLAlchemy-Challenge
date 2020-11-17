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
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


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
        f"/api/v1.0/start/2017-08-15<br/>"
        f"/api/v1.0/start/2017-08-20/2017-08-23<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #create a session link
    # session = Session(engine)

    #query for the date and precipitation
    weather = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2017-08-20').all()

    #close out the session
    # session.close

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
    # session = Session(engine)

    #query for the date and precipitation
    station = session.query(Station.name).all()

    #close out the session
    # session.close

    #convert the list of tuples to normal lists
    station_names = list(np.ravel(station))

    #return the list jsonified
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    #create a session link
    # session = Session(engine)

    #query for the date and precipitation
    tobs = session.query(Measurement.tobs).filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.station == 'USC00519281').all()

    #close out the session
    # session.close

    #create a lits from the query
    tobs_all = list(np.ravel(tobs))

    #return the list jsonified
    return jsonify(tobs_all)

# @app.route("/api/v1.0/start/<start>")
# @app.route("/api/v1.0/start/<start>")
# def route(start = None):
#     #create the search variables
#     start_date = start
    
#     #create a session link
#     session = Session(engine)

#     maxTemp = session.query(func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start_date).scalar()
#     minTemp = session.query(func.min(Measurement.tobs)).\
#         filter(Measurement.date >= start_date).scalar()
#     avgTemp = session.query(func.avg(Measurement.tobs)).\
#         filter(Measurement.date >= start_date).scalar()

#     #close out the session
#     session.close

#     #create a dictionary
#     weather_date = []
#     weather_dict = {}
#     weather_dict["Start_Date"] = start_date
#     weather_dict["Avg_Temp"] = round(avgTemp,2)
#     weather_dict["Max_Temp"] = maxTemp
#     weather_dict["Min_Temp"] = minTemp
#     weather_date.append(weather_dict)

#     return jsonify(weather_date)
@app.route("/api/v1.0/start/<start>")
@app.route("/api/v1.0/start/<start>/<end>")
def name(start = None, end=None):
    #create the search variables
    start_date = start
    end_date = end

    #create a session link
    # session = Session(engine)

    #query for the date and precipitation
    if end_date == None:
        maxTemp = session.query(func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).scalar()
        minTemp = session.query(func.min(Measurement.tobs)).\
            filter(Measurement.date >= start_date).scalar()
        avgTemp = session.query(func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date).scalar()
    else:
        maxTemp = session.query(func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).scalar()
        minTemp = session.query(func.min(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).scalar()
        avgTemp = session.query(func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).scalar()

    #close out the session
    # session.close

    #create a dictionary
    weather_date = []
    weather_dict = {}
    weather_dict["Start_Date"] = start_date
    weather_dict["End_Date"] = end_date
    weather_dict["Avg_Temp"] = round(avgTemp,2)
    weather_dict["Max_Temp"] = maxTemp
    weather_dict["Min_Temp"] = minTemp
    weather_date.append(weather_dict)

    return jsonify(weather_date)


if __name__ == '__main__':
    app.run(debug=True)
    session.close()