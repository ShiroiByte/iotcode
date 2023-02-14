import pyrebase
import dht11
import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.D10, 30)

config = {
  "apiKey": "JwQlZC5W9czYMFErcDB0OXSAr5N9c4kNHxSw68PA",
  "authDomain": "smarthome-35e3f.firebaseapp.com",
  "databaseURL": "https://smarthome-35e3f-default-rtdb.europe-west1.firebasedatabase.app/",
  "storageBucket": "smarthome-35e3f.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

instance = dht11.DHT11(pin = 24)
maxtemp = 0
mintemp = 50
while True:
    result = instance.read()
    if result.humidity >= 80  and result.humidity!=0:
        response0 = {
            "HumidityState" : "BAD"
            }
        db.update(response0)
        
    if result.humidity < 80  and result.humidity!=0:
        response1 = {
            "HumidityState" : "GOOD"
            }
        db.update(response1)
        
    if result.temperature>maxtemp:
        maxtemp = result.temperature
        response2 = {
            "Max" : maxtemp
            }
        db.update(response2)
    if result.temperature<mintemp and result.temperature!=0:
        mintemp = result.temperature
        response3 = {
            "Min" : mintemp
            }
        db.update(response3)
    data = {
        "Temperature" : result.temperature,
        "Humidity" : result.humidity
    }
    if result.temperature!=0 and result.humidity!=0:
        db.update(data)
        time.sleep(3)
    getHex = db.child("hex").get()
    h = getHex.val().lstrip('#')
    converted = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    pixels.fill(converted)
    
    