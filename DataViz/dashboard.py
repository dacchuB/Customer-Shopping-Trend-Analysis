import warnings
from flask import Blueprint,request,jsonify
from sqlalchemy.sql import text
from db import db
import datetime

dashboard_blueprint = Blueprint('dashboard_blueprint',__name__)

#todays visitors
@dashboard_blueprint.route('/today-visitors')
def todayVisitors():
     
     currentDate=datetime.datetime.today().strftime("%Y-%m-%d")
     sqltodayVisitors=text('SELECT COUNT(*) AS Today_visitors FROM visitors_log WHERE date="'+currentDate+'"')
     resultData=db.engine.execute(sqltodayVisitors)
     rawData=resultData.fetchall()

     jsonData=jsonify([dict(row) for row in rawData])
     return jsonData

#overall visitors
@dashboard_blueprint.route('/overral-visitors')
def overralVisitors():
     
    
     sqloverralVisitors=text('SELECT COUNT(*) AS overral_visitors FROM visitors_log')
     resultData=db.engine.execute(sqloverralVisitors)
     rawData=resultData.fetchall()

     jsonData=jsonify([dict(row) for row in rawData])
     return jsonData

#male visitors
@dashboard_blueprint.route('/male-visitors')
def maleVisitors():
     
     currentDate=datetime.datetime.today().strftime("%Y-%m-%d")
     sqlmaleVisitors=text('SELECT COUNT(*) AS male_visitors FROM visitors_log WHERE date="'+currentDate+'" AND gender=1')
     resultData=db.engine.execute(sqlmaleVisitors)
     rawData=resultData.fetchall()

     jsonData=jsonify([dict(row) for row in rawData])
     return jsonData

#female visitors
@dashboard_blueprint.route('/female-visitors')
def femaleVisitors():
     
     currentDate=datetime.datetime.today().strftime("%Y-%m-%d")
     sqlfemaleVisitors=text('SELECT COUNT(*) AS female_visitors FROM visitors_log WHERE date="'+currentDate+'" AND gender=2')
     resultData=db.engine.execute(sqlfemaleVisitors)
     rawData=resultData.fetchall()

     jsonData=jsonify([dict(row) for row in rawData])
     return jsonData

#Table data 
@dashboard_blueprint.route('/table-data')
def tabledata():
     
    currentDate=datetime.datetime.today().strftime("%Y-%m-%d")

    txtlabel=''
    x=''
    for a in range(1,6):
    
        if a==1:
            txtlabel='kids'
        elif a==2:
            txtlabel='Teenagers'
        elif a==3:
            txtlabel='Youngsters'
        elif a==4:
            txtlabel='Adults'
        elif a==5:
            txtlabel='Senior sitizen'

        for g in range(1,3): #g=gender
               #todays visitors
            sqltodayVisitors=text('SELECT COUNT(*) AS Today_visitors FROM visitors_log WHERE date="'+currentDate+'" AND gender='+str(g)+' AND age_group='+str(a)+'')
            resultData=db.engine.execute(sqltodayVisitors)
            rawData=resultData.fetchall()
            ageGroupGenderToday=rawData[0].Today_visitors


            #overral visitors
            sqloverralVisitors=text('SELECT COUNT(*) AS overral_visitors FROM visitors_log WHERE gender='+str(g)+' AND age_group='+str(a)+'')
            resultData=db.engine.execute(sqloverralVisitors)
            rawOData=resultData.fetchall()
            ageGroupGenderOverral=rawOData[0].overral_visitors

            gText=''
            if g==1:
                gText='Male'
            elif g==2:
                gText='Female'

            x+='{"gender":"'+gText+'","age_group":"'+txtlabel+'","Today_visitors":"'+str(ageGroupGenderToday)+'","overral_visitors":"'+str(ageGroupGenderOverral)+'"},'
               #end of the inner for loop
        #end of outer for loop
    x=x[:-1]
    jsonData='['+x+']'
    return jsonData
#graph
@dashboard_blueprint.route('/graph-data')
def graphdata():
    x=''
    for m in range(1,13):
        sqlMonthData=text('SELECT COUNT(*) AS monthly_visitors FROM visitors_log WHERE MONTH(date)="'+str(m)+'"')
        resultdata=db.engine.execute(sqlMonthData)
        rawData=resultdata.fetchall()
        totalMothlyVisitors =rawData[0].monthly_visitors
        x+='{"month":"'+str(totalMothlyVisitors)+'"},'
    x=x[:-1]

    jsonData='['+x+']'
    return jsonData

@dashboard_blueprint.route('/graph-data1')
def graphdata1():
    x=''
    for m in range(1,5):
        sqlMonthData=text('SELECT COUNT(*) AS monthly_visitors FROM visitors_log WHERE item_purchased="'+str(m)+'"')
        resultdata=db.engine.execute(sqlMonthData)
        rawData=resultdata.fetchall()
        totalMothlyVisitors =rawData[0].monthly_visitors
        x+='{"month":"'+str(totalMothlyVisitors)+'"},'
    x=x[:-1]

    jsonData='['+x+']'
    return jsonData

@dashboard_blueprint.route('/graph-data2')
def graphdata2():
    x=''
    for m in range(1,6):
        sqlMonthData = text('SELECT COUNT(*) AS monthly_visitors FROM visitors_log WHERE review_rate="'+str(m)+'"')
        resultdata = db.engine.execute(sqlMonthData)
        rawData=resultdata.fetchall()
        totalMothlyVisitors =rawData[0].monthly_visitors
        x+='{"month":"'+str(totalMothlyVisitors)+'"},'
    x=x[:-1]

    jsonData='['+x+']'
    return jsonData

@dashboard_blueprint.route('/graph-data3')
def graphdata3():
    data = []

    for category in ['review_rate', 'item_purchased']:
        values = []

        for value in range(1, 6):
            sqlData = text(f'SELECT COUNT(*) AS monthly_visitors FROM visitors_log WHERE {category}="{str(value)}"')
            resultdata = db.engine.execute(sqlData)
            rawData = resultdata.fetchall()
            totalMonthlyVisitors = rawData[0].monthly_visitors

            values.append(totalMonthlyVisitors)

        data.append({
            'category': category,
            'values': values
        })

    return jsonify(data)


@dashboard_blueprint.route('/graph-data4')
def graphdata4():
    data = []

    for category in ['age_group', 'item_purchased']:
        for value in range(1, 6):
            sqlData = text(f'SELECT COUNT(*) AS monthly_visitors FROM visitors_log WHERE {category}="{str(value)}"')
            resultdata = db.engine.execute(sqlData)
            rawData = resultdata.fetchall()
            totalMonthlyVisitors = rawData[0].monthly_visitors

            data.append({
                'category': category,
                'value': totalMonthlyVisitors,
                'label': str(value)
            })

    return jsonify(data)


@dashboard_blueprint.route('/graph-data5')
def graphdata5():
    current_date = datetime.date.today()
    
    # Monthly data
    monthly_data = get_data_for_timeframe('month', current_date)

    # Weekly data
    weekly_data = get_data_for_timeframe('week', current_date)

    # Daily data
    daily_data = get_data_for_timeframe('day', current_date)

    return jsonify({'monthly': monthly_data, 'weekly': weekly_data, 'daily': daily_data})


def get_data_for_timeframe(timeframe, current_date):
    data = []

    if timeframe == 'month':
        for m in range(1, 13):
            sqlMonthData = text('SELECT COUNT(*) AS visitors_count FROM visitors_log WHERE MONTH(date) = :month')
            resultdata = db.engine.execute(sqlMonthData, month=m)
            rawData = resultdata.fetchall()
            totalMonthlyVisitors = rawData[0].visitors_count
            data.append({'time': f'Month {m}', 'count': totalMonthlyVisitors})

    elif timeframe == 'week':
        for w in range(1, 5):  # Assuming there are 4 weeks in a month
            start_date = current_date - datetime.timedelta(days=current_date.weekday() + (w - 1) * 7)
            end_date = start_date + datetime.timedelta(days=6)
            sqlWeekData = text('SELECT COUNT(*) AS visitors_count FROM visitors_log WHERE date BETWEEN :start_date AND :end_date')
            resultdata = db.engine.execute(sqlWeekData, start_date=start_date, end_date=end_date)
            rawData = resultdata.fetchall()
            totalWeeklyVisitors = rawData[0].visitors_count
            data.append({'time': f'Week {w}', 'count': totalWeeklyVisitors})

    elif timeframe == 'day':
        for d in range(1, current_date.day + 1):
            sqlDayData = text('SELECT COUNT(*) AS visitors_count FROM visitors_log WHERE DAY(date) = :day')
            resultdata = db.engine.execute(sqlDayData, day=d)
            rawData = resultdata.fetchall()
            totalDailyVisitors = rawData[0].visitors_count
            data.append({'time': f'Day {d}', 'count': totalDailyVisitors})

    return data

@dashboard_blueprint.route('/graph-data6')
def graph_data6():
    # Assuming you have a table 'transactions' with columns: item_purchased, payment_method
    sql_data = text('SELECT item_purchased, payment_method, COUNT(*) AS count FROM visitors_log GROUP BY item_purchased, payment_method')
    result = db.engine.execute(sql_data)
    data = [{'item_purchased': row.item_purchased, 'payment_method': row.payment_method, 'count': row.count} for row in result]

    return jsonify(data)


@dashboard_blueprint.route('/graph-data7')
def graph_data7():
    # Assuming you have a table 'reviews' with a column 'review_rate'
    sql_data = text('SELECT review_rate FROM visitors_log')
    result = db.engine.execute(sql_data)
    data = [{'review_rate': row.review_rate} for row in result]

    return jsonify(data)

from sqlalchemy import text

@dashboard_blueprint.route('/graph-data8')
def graph_data8():
    # Assuming you have a table 'visitors_log' with columns 'gender' and 'purchase_count'
    sql_data_gender = text("""
        SELECT gender, COUNT(*) AS purchase_count
        FROM visitors_log
        WHERE item_purchased IS NOT NULL
        GROUP BY gender
    """)

    result_gender = db.engine.execute(sql_data_gender)

    data_gender = [{'gender': row.gender, 'purchase_count': row.purchase_count} for row in result_gender]

    return jsonify({'genderDistribution': data_gender})


@dashboard_blueprint.route('/graph-data9')
def graph_data9():
    # Assuming you have a table 'visitors_log' with columns 'gender', 'purchase_count', and 'location'
    sql_data_location = text("""
        SELECT location, gender, COUNT(*) AS purchase_count
        FROM visitors_log
        WHERE item_purchased IS NOT NULL
        GROUP BY location, gender
    """)

    result_location = db.engine.execute(sql_data_location)

    data_location = [{'location': row.location, 'gender': row.gender, 'purchase_count': row.purchase_count} for row in result_location]

    return jsonify({'locationDistribution': data_location})


@dashboard_blueprint.route('/graph-data11')
def graph_data11():
    # Assuming you have a table 'visitors_log' with columns 'location' and 'visitor_count'
    sql_data_location = text("""
        SELECT location, COUNT(*) AS visitor_count
        FROM visitors_log
        GROUP BY location
    """)

    result_location = db.engine.execute(sql_data_location)

    data_location = [{'location': row.location, 'visitor_count': row.visitor_count} for row in result_location]

    # Find the location with the maximum visitor count
    max_location = max(data_location, key=lambda x: x['visitor_count'])

    return jsonify({'locationData': data_location, 'maxLocation': max_location})
