# Import the dependencies.
import datetime as dt

from flask import Flask, jsonify
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

# Create our session (link) from Python to the DB
session = Session(engine)

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
    # Find the most recent date in the data set.
    most_recent_date = dt.datetime.strptime(session.query(func.max(Measurement.date)).first()[0], '%Y-%m-%d').date()
    
    # Calculate the date one year from the last date in data set.
    target_date = most_recent_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    prcp_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between(target_date, most_recent_date))
    
    return 'Hi'

if __name__ == '__main__':
    app.run(debug=True)