from flask import Flask, render_template
import random
import pymysql


app = Flask(__name__)

@app.route('/')
def home():
    tempareture=str(random.randint(20,30))
    humidity=str(random.randint(40,90))
    soil_humidity=str(random.randint(10,60))
    print(tempareture)
    print(humidity)
    print(soil_humidity)
    try:
        connection = pymysql.connect(
    host='localhost',            # MySQL sunucusunun adresi (örneğin, '127.0.0.1' veya 'localhost')
    user='furkan',                 # Veritabanı kullanıcı adı
    password='furkan',    # Kullanıcı şifresi
    database='sera_izleme'    # Veritabanı adı
)

        with connection.cursor() as cursor:
            sql = """
                INSERT INTO sera (Sicaklik, Nem, Toprak_nem)
                VALUES (%s, %s, %s)
                """
            cursor.execute(sql, (tempareture, humidity, soil_humidity))
            connection.commit()
    finally:
            connection.close()
    return render_template('index.html',tempareture=tempareture,humidity=humidity,soil_humidity=soil_humidity)

if __name__ == '__main__':
    app.run(debug=True)
