# Import the dependencies.
import datetime as dt

from flask import escape, Flask, jsonify
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
# Global Constant Setup
#################################################
with Session(engine) as session:
    # Find the oldest date in the data set
    date_query = session.query(func.min(Measurement.date)).first()
    CONST_OLDEST_DATE = dt.datetime.strptime(date_query[0], '%Y-%m-%d').date()

    # Find the newest date in the data set.
    date_query = session.query(func.max(Measurement.date)).first()
    CONST_NEWEST_DATE = dt.datetime.strptime(date_query[0], '%Y-%m-%d').date()


#################################################
# Flask Routes
#################################################
@app.route('/')
def welcome():
    return (f'''
        Welcome to Matt's neat-o climate app!<br/>
        <br/>
        Available Routes:<br/>
        /api/v1.0/precipitation<br/>
        /api/v1.0/stations<br/>
        /api/v1.0/tobs<br/>
        /api/v1.0/{escape('<')}start{escape('>')}<br/>
        /api/v1.0/{escape('<')}start{escape('>')}/{escape('<')}end{escape('>')}<br/>
    ''')


@app.route('/api/v1.0/precipitation')
def get_precipitation_data():
    # Calculate the date one year from the last date in data set.
    target_date = CONST_NEWEST_DATE - dt.timedelta(days=365)
    
    with Session(engine) as session:
        # Perform a query to retrieve the data and precipitation scores
        prcp_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between(target_date, CONST_NEWEST_DATE)).all()

    # Display the query result as a jsonified dictionary
    precipitation_data = dict(prcp_query)
    return jsonify(precipitation_data)


@app.route('/api/v1.0/stations')
def get_stations():
    with Session(engine) as session:
        # Perform a query to retrieve the station names
        station_query = session.query(Station.name).all()

    # Flatten the query result into a normal list to jsonify and display
    station_list = list(ravel(station_query))
    return jsonify(station_list)


@app.route('/api/v1.0/tobs')
def get_temperature_data():
    # Calculate the date one year from the last date in data set.
    target_date = CONST_NEWEST_DATE - dt.timedelta(days=365)
    
    with Session(engine) as session:
        # Design a query to find the most active station
        station_count = func.count(Measurement.station)
        station_activity_query = session.query(Measurement.station, station_count).group_by(Measurement.station).order_by(station_count.desc()).all()
        most_active_station = station_activity_query[0].station

        # Using the most active station id query the last 12 months of temperature observation data for this station
        tobs_query = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.station == most_active_station, Measurement.date.between(target_date, CONST_NEWEST_DATE)).all()

    # Display the query result as a jsonified dictionary
    temperature_data = dict(tobs_query)
    return jsonify(temperature_data)


@app.route('/api/v1.0/<start>')
def get_temperature_stats_start(start):
    # Ensure input date is valid
    start_date = string_to_date(start)
    if type(start_date) is str: return start_date

    # Query for temperature stats from the start date to the most recent date
    tobs_query = get_temperature_stats(start_date, CONST_NEWEST_DATE)

    # Flatten the query result into a normal list to jsonify and display
    temperature_stats = list(ravel(tobs_query))
    return jsonify(temperature_stats)


@app.route('/api/v1.0/<start>/<end>')
def get_temperature_stats_start_end(start, end):
    # Ensure input dates are valid
    start_date = string_to_date(start)
    if type(start_date) is str: return f'Start date {start_date}'
    end_date = string_to_date(end)
    if type(end_date) is str: return f'End date {end_date}'
    if end_date < start_date: return 'ERROR: The end date cannot occur before the start date.'

    # Query for temperature stats in the requested range
    tobs_query = get_temperature_stats(start_date, end_date)

    # Flatten the query result into a normal list to jsonify and display
    temperature_stats = list(ravel(tobs_query))
    return jsonify(temperature_stats)


#################################################
# Functions
#################################################
def get_temperature_stats(start_date, end_date):
    with Session(engine) as session:
        # Query for temperature stats in the requested range
        tobs_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date.between(start_date, end_date)).all()
    
    return tobs_query


def string_to_date(date_string : str):
    try:
        # If date_string is formatted incorrectly, strptime will throw an exception
        date = dt.datetime.strptime(date_string, '%Y-%m-%d').date()
        
        # Ensure date is within the range of the dataset
        if date < CONST_OLDEST_DATE or date > CONST_NEWEST_DATE:
            date = f'ERROR:<br><br>The date must be between {CONST_OLDEST_DATE} and {CONST_NEWEST_DATE}.'
    
    except ValueError:
        date = '''ERROR:<br><br>
        
        Please enter the date in one of the following formats:<br>
        yyyy-m-d<br>
        yyyy-mm-d<br>
        yyyy-m-dd<br>
        yyyy-mm-dd'''
    
    return date


if __name__ == '__main__':
    app.run(debug=True)
