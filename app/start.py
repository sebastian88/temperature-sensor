from machine import Pin,reset
import time, ntptime
import network
import urequests as requests
from .dht import DHT11
from . import secrets


def flash(led, times):
    while times > 0:
        led.on()
        time.sleep(0.2)
        led.off()
        time.sleep(0.2)
        times = times - 1

def date(st):
    return"{:4}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format( \
        st[0], st[1], st[2], st[3], st[4], st[5])

def setup():
    wlan = network.WLAN(network.STA_IF)
    
    if not wlan.isconnected():
        wlan.active(True)
        wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

        # Wait for connect or fail
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            time.sleep(1)
        # Handle connection error
        if wlan.status() != 3:
            raise RuntimeError('network connection failed')

        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )

    time.sleep(1)

    pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
    sensor = DHT11(pin)
    led = Pin("LED", Pin.OUT)
    
    time_got = False
    while time_got is False:
        try:
            ntptime.settime()
            time_got = True
        except Exception as e:
            print(e)
    return sensor, led

def readTemperature(sensor):
    current_time = date(time.localtime())
    
    temperature_got = False
    temperature = None
    humidity = None
    while temperature_got is False:
        try:
            temperature = sensor.temperature
            humidity = sensor.humidity
            temperature_got = True
        except Exception as e:
            print(e)
    
    sensor_readings={'room': secrets.ROOM,'time': current_time, 'temperature': temperature, 'humidity': humidity}
    request = requests.post(secrets.URL,json=sensor_readings,headers={'Content-Type': 'application/json'})
    request.close()


def run():
    count = 0
    while True:
        exception = ''
        try:
            sensor, led = setup()

            if exception:
                error={'message': exception}
                requests.post('https://eonii83wfz2ze2u.m.pipedream.net', error, headers={'Content-Type': 'application/json'})
                exception = ''
            
            flash(led, secrets.ROOM)
            time.sleep(1.0)
            flash(led, secrets.ROOM)
            time.sleep(1.0)
            flash(led, secrets.ROOM)
            time.sleep(1.0)
            flash(led, secrets.ROOM)


            while True:
                readTemperature(sensor)
                time.sleep(300)
                count += 1
                if count >= 300:
                    reset()

        except Exception as e:
            exception = e

        time.sleep(60)
        count += 100
