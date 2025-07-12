import sqlite3
import random
import time

def generate_sensor_data():
    soil_moisture = random.uniform(20, 60)  # %
    temperature = random.uniform(20, 35)    # °C
    humidity = random.uniform(50, 90)       # %
    rainfall = random.choice([0, 0, 0, 1])  # ~25% chance of rain
    return soil_moisture, temperature, humidity, rainfall

def insert_data():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    soil_moisture, temperature, humidity, rainfall = generate_sensor_data()
    c.execute('''
        INSERT INTO sensor_data (soil_moisture, temperature, humidity, rainfall)
        VALUES (?, ?, ?, ?)
    ''', (soil_moisture, temperature, humidity, rainfall))
    conn.commit()
    conn.close()

    print(f"Inserted -> Soil: {soil_moisture:.2f}% | Temp: {temperature:.2f}°C | Hum: {humidity:.2f}% | Rain: {rainfall}")

if __name__ == "__main__":
    while True:
        insert_data()
        time.sleep(5)  # wait 5 seconds before inserting next data
