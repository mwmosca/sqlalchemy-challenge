# Import the dependencies.
import datetime as dt

from flask import Flask, jsonify
from numpy import ravel
from pathlib import Path
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


#################################################
# Database Setup
#################################################
engine = create_engine(f"sqlite:///{Path('Resources', 'hawaii.sqlite')}")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route('/')
def welcome():
    return ('''
        Welcome to a neat-o climate app.<br/>
        <br/>
        Available Routes:<br/>
        /api/v1.0/precipitation<br/>
        /api/v1.0/stations<br/>
        /api/v1.0/tobs<br/>
        /api/v1.0/<start><br/>
        /api/v1.0/<start>/<end><br/>
    ''')


@app.route('/api/v1.0/precipitation')
def precipitation_analysis():
    with Session(engine) as session:
        # Find the most recent date in the data set.
        date_query = session.query(func.max(Measurement.date)).first()
        most_recent_date = dt.datetime.strptime(date_query[0], '%Y-%m-%d').date()
        
        # Calculate the date one year from the last date in data set.
        target_date = most_recent_date - dt.timedelta(days=365)

        # Perform a query to retrieve the data and precipitation scores
        prcp_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between(target_date, most_recent_date)).all()

    # Display the query result as a jsonified dictionary
    precipitation_analysis_results = dict(prcp_query)
    return jsonify(precipitation_analysis_results)


@app.route('/api/v1.0/stations')
def get_stations():
    with Session(engine) as session:
        # Perform a query to retrieve the station names
        station_query = session.query(Station.name).all()

    # Flatten the query result into a normal list to jsonify and display
    station_list = list(ravel(station_query))
    return jsonify(station_list)


@app.route('/api/v1.0/tobs')
def temperature_analysis():
    with Session(engine) as session:
        # Find the most recent date in the data set.
        date_query = session.query(func.max(Measurement.date)).first()
        most_recent_date = dt.datetime.strptime(date_query[0], '%Y-%m-%d').date()

        # Calculate the date one year from the last date in data set.
        target_date = most_recent_date - dt.timedelta(days=365)

        # Design a query to find the most active station
        station_count = func.count(Measurement.station)
        station_activity_query = session.query(Measurement.station, station_count).group_by(Measurement.station).order_by(station_count.desc()).all()
        most_active_station = station_activity_query[0].station

        # Using the most active station id query the last 12 months of temperature observation data for this station
        tobs_query = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.station == most_active_station, Measurement.date.between(target_date, most_recent_date)).all()

    # Display the query result as a jsonified dictionary
    temperature_analysis_results = dict(tobs_query)
    return jsonify(temperature_analysis_results)


if __name__ == '__main__':
    app.run(debug=True)