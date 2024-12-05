# Import the dependencies.
import datetime as dt
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
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
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
    """List all available API routes with explanations."""
    return (
        f"<h1>Welcome to the Climate Analysis API</h1>"
        f"<p>Available Routes:</p>"
        f"<ul>"
        f"<li>/api/v1.0/precipitation - Retrieve the last 12 months of precipitation data as JSON</li>"
        f"<li>/api/v1.0/stations - Get a list of all weather observation stations as JSON</li>"
        f"<li>/api/v1.0/tobs - Retrieve the temperature observations (TOBS) for the most active station for the last 12 months</li>"
        f"<li>/api/v1.0/&lt;start&gt; - Replace &lt;start&gt; with a date (YYYY-MM-DD) to get TMIN, TAVG, and TMAX for all dates after the start date</li>"
        f"<li>/api/v1.0/&lt;start&gt;/&lt;end&gt; - Replace &lt;start&gt; and &lt;end&gt; with dates (YYYY-MM-DD) to get TMIN, TAVG, and TMAX for the date range (inclusive)</li>"
        f"</ul>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    """The last 12 months of data"""
    session = Session(engine)

    # Get the most recent date in the dataset
    latest_date = session.query(func.max(Measurement.date)).scalar()
    latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')
    one_year_ago = latest_date - dt.timedelta(days=365)

    # Query precipitation data for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    # Convert query results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in results}

    # Close the session
    session.close()

    # Return the JSON representation
    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of all stations"""
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station).all()

    # Convert query results to a list
    stations_list = [station[0] for station in results]

    # Close the session
    session.close()

    # Return the JSON representation of the list
    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return temperature observations for the most active station for the previous year."""
    session = Session(engine)

    # Find the most active station
    most_active_station = (
        session.query(Measurement.station)
        .group_by(Measurement.station)
        .order_by(func.count(Measurement.station).desc())
        .first()[0]
    )

    # Get the most recent date in the dataset
    latest_date = session.query(func.max(Measurement.date)).scalar()
    latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')
    one_year_ago = latest_date - dt.timedelta(days=365)

    # Query temperature observations for the most active station for the last 12 months
    results = (
        session.query(Measurement.date, Measurement.tobs)
        .filter(Measurement.station == most_active_station)
        .filter(Measurement.date >= one_year_ago)
        .all()
    )

    # Convert query results to a list of dictionaries
    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in results]

    # Close the session
    session.close()

    # Return the JSON representation
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start, end=None):
    """
    Return TMIN, TAVG, and TMAX for a specified start date, 
    or start-end date range if both are provided.
    """
    session = Session(engine)

    # Base query to calculate TMIN, TAVG, TMAX
    sel = [
        func.min(Measurement.tobs).label("TMIN"),
        func.avg(Measurement.tobs).label("TAVG"),
        func.max(Measurement.tobs).label("TMAX")
    ]

    # Debugging: Check input values
    print(f"Start Date: {start}")
    if end:
        print(f"End Date: {end}")

    if end:
        # Query for start-end date range
        results = (
            session.query(*sel)
            .filter(Measurement.date >= start)
            .filter(Measurement.date <= end)
            .all()
        )
    else:
        # Query for dates greater than or equal to the start date
        results = (
            session.query(*sel)
            .filter(Measurement.date >= start)
            .all()
        )

    # Debugging: Check query results
    print(f"Query Results: {results}")

    # Close the session
    session.close()

    # Handle empty results
    if not results or results[0][0] is None:
        return jsonify({
            "Error": "No data found for the specified date range. Please check your input."
        }), 404

    # Extract the result and format it as a dictionary
    temperature_data = {
        "Start Date": start,
        "End Date": end if end else "All dates after start",
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    # Return the JSON representation
    return jsonify(temperature_data)




if __name__ == '__main__':
    app.run(debug=True)

