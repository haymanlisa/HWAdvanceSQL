import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#SQL ALCHMEY
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


#FLASK
app = Flask(__name__)

#ROUTES AND FUNCTION
@app.route("/")
def welcome(): 
    return """
    THIS IS A API GUIDE TO USE MY API <br>
     precipitation ===> /api/v1.0/precipitation <br>
     stations ===> /api/v1.0/stations <br>
     temp ===> /api/v1.0/tobs <br>
     calc_temp ===> /api/v1.0/yy-mm-dd/yy-mm-dd <br>
    """

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    last_12month = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    a = [{k:v} for k,v in last_12month]

    return jsonify(a)
    

@app.route("/api/v1.0/stations")
def stations():

    result = session.query(Station.station).all()
    stations = list(np.ravel(result))
    
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp():

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    num_temp = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
    
    temp = list(np.ravel(num_temp))

    return jsonify(temp)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start=None, end=None):
    t = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if end == None:
        calc_temp = session.query(*t).filter(Measurement.date >= start).filter(Measurement.date <= '2015-08-08').all()
        return jsonify(calc_temp)
    
    else:
        calc_temp = session.query(*t).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        return jsonify(calc_temp)







if __name__ == '__main__':
    app.run(debug=True)



