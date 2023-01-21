from machine import Pin
from machine import ADC
from dht import DHT11, InvalidChecksum
import time, ntptime
import network
import urequests as requests


ssid = '...'
password = '...'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

adc = machine.ADC(4) 
time.sleep(1)

pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)

def date(st):
    return"{:4}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format( \
        st[0], st[1], st[2], st[3], st[4], st[5])

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
ntptime.settime()
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    request_headers = {'Content-Type': 'application/json'}
    url='https://3mya4jha58.execute-api.eu-west-1.amazonaws.com/live'
    while True:
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
        
        sensor_readings={'room': 'external','time': current_time, 'temperature': temperature, 'humidity': humidity}`
        request = requests.post(url,json=sensor_readings,headers=request_headers)
        request.close()
        
        time.sleep(300)










