from flask import Flask, render_template, jsonify
import random
import pymysql
from datetime import datetime


app = Flask(__name__)

def get_db_inf():
     return pymysql.connect(
        host='localhost',            
        user='furkan',               
        password='furkan',          
        database='sera_izleme',    
        cursorclass=pymysql.cursors.DictCursor  
    )

@app.route('/')
def home():
    tempareture=str(random.randint(20,30))
    humidity=str(random.randint(40,90))
    soil_moisture=str(random.randint(10,60))
    times=datetime.now()
    timestamp=times.strftime("%Y-%m-%d %H:%M:%S")
    # print(tempareture)
    # print(humidity)
    # print(soil_moisture)
    # print(timestamp)
    try:
        connection=get_db_inf()

        with connection.cursor() as cursor:
            sql = """
                INSERT INTO sera (tempareture, humidity, soil_moisture, timestamp)
                VALUES (%s, %s, %s, %s)
                """
            cursor.execute(sql, (tempareture, humidity, soil_moisture, timestamp))
            connection.commit()
            querys = """
                SELECT tempareture, humidity, soil_moisture, timestamp 
                FROM sera 
                WHERE timestamp >= NOW() - INTERVAL 10 MINUTE
                ORDER BY timestamp DESC
                LIMIT 10;
            """
            cursor.execute(querys)
            getdata = cursor.fetchall()
           
    finally:
            connection.close()
    return render_template('index.html',tempareture=tempareture,humidity=humidity,soil_moisture=soil_moisture,getdata=getdata)



@app.route('/api/sensor-data', methods=['GET'])
def get_sensor_data():
    try:
        connection = get_db_inf()
        with connection.cursor() as cursor:
            query = """
                SELECT tempareture, humidity, soil_moisture, timestamp 
                FROM sera 
                ORDER BY timestamp DESC;
            """
            cursor.execute(query)
            rows = cursor.fetchall()    
            
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()
       
watering_status = False
@app.route('/api/watering', methods=['POST'])
def toggle_watering():
    global watering_status
    
    watering_status = not watering_status

    if watering_status:
        message = "Sulama başlatıldı"
    else:
        message = "Sulama kapatıldı"

    return jsonify({'message': message})
if __name__ == '__main__':
    app.run(debug=True)
