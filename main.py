from machine import Pin
from machine import ADC
from dht import DHT11, InvalidChecksum
import time, ntptime
import network
import urequests as requests
import wifi_secrets

try:

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_secrets.ssid, wifi_secrets.password)

    time.sleep(1)

    pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
    sensor = DHT11(pin)
    led = machine.Pin("LED", machine.Pin.OUT)

    def date(st):
        return"{:4}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format( \
            st[0], st[1], st[2], st[3], st[4], st[5])

    def flash(times):
        while times > 0:
            led.on()
            time.sleep(0.2)
            led.off()
            time.sleep(0.2)
            times = times - 1

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
    request_headers = {'Content-Type': 'application/json'}
    
    time_got = False
    while time_got is False:
        try:
            ntptime.settime()
            time_got = True
        except Exception as e:
            print(e)

    flash(wifi_secrets.room)
    time.sleep(1.0)
    flash(wifi_secrets.room)
    time.sleep(1.0)
    flash(wifi_secrets.room)
    

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
        
        sensor_readings={'room': wifi_secrets.room,'time': current_time, 'temperature': temperature, 'humidity': humidity}
        request = requests.post(wifi_secrets.url,json=sensor_readings,headers=request_headers)
        request.close()
        time.sleep(300)
            
except Exception as e:
    print(e)

time.sleep(60)
