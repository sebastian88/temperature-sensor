from machine import reset
import time

def connectToWifiAndUpdate():
    import machine, network, gc, app.secrets as secrets
    time.sleep(1)
    print('Memory free', gc.mem_free())

    from app.ota_updater import OTAUpdater

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    otaUpdater = OTAUpdater('https://github.com/sebastian88/temperature-sensor', headers={'Authorization': 'token {}'.format(secrets.TOKEN)}, main_dir='app', secrets_file="secrets.py")
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del(otaUpdater)
        gc.collect()

def startApp():
    from app import start
    start.run()


while True:
    error_count = 0
    try:
        connectToWifiAndUpdate()
        startApp()

    except Exception:
        error_count += 1
        if error_count >= 20:
            reset()
        time.sleep(300)