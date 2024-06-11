# Import the dependencies.
import numpy as np
import os
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
Measurement = Base.classes.measurement

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available routes."""
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

#LKF
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    # Query for the last 12 months of precipitation data:
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').all()
    session.close()

    # Convert the query results to a dictionary with date as the key and prcp as the value:
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    results = session.query(Measurement.station).distinct().all()
    session.close()

    # Convert the query results to a list
    station_list = list(np.ravel(results))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations (tobs) for previous year."""
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').all()
    session.close()

    # Convert the query results to a list of dictionaries:
    temperature_observations = [
        {"date": date, "tobs": tobs} for date, tobs in results]

    return jsonify(temperature_observations)


@app.route("/api/v1.0/<start>")
def temperature_start(start):
    """Return TMIN, TAVG, TMAX."""
 
    # Query for TMIN, TAVG, and TMAX
    results = session.query(func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    # Convert the query results to a dictionary
    temperature_data = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return jsonify(temperature_data)


@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end):
    """Return JSON list of TMIN, TAVG, and TMAX for the date range."""

    # Query for TMIN, TAVG, and TMAX for the date range
    results = session.query(func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    # Convert the query results to a dictionary
    temperature_data = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return jsonify(temperature_data)


# Run the Flask app:
if __name__ == "__main__":
    app.run()
