from flask import Blueprint,request
from sqlalchemy.sql import text
from db import db
import datetime


visitor_blueprint = Blueprint('visitor_blueprint',__name__)

@visitor_blueprint.route('/log-visitors',methods=['POST'])
def addVisitorData():
    gender=request.form['gender']
    ageGroup=request.form['age_group']
    currentDate=datetime.datetime.today().strftime("%Y-%m-%d")
    currentTime=datetime.datetime.now().strftime("%H:%M:%S")
    itemPurchased=request.form['item_purchased']
    reviewRate=request.form['review_rate']  
    Location=request.form['location']
    paymentMethod=request.form['payment_method']


    sql=text('INSERT INTO  visitors_log(gender,age_group,date,time,item_purchased,review_rate,location,payment_method) VALUES('+str(gender)+','+str(ageGroup)+',"'+currentDate+'","'+currentTime+'",'+str(itemPurchased)+','+str(reviewRate)+',"'+str(Location)+'",'+str(paymentMethod)+')')
    db.engine.execute(sql)

    return "data logged successfully"