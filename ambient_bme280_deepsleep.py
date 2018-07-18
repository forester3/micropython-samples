import machine
import network
import bme280
import ambient
import esp

ssid = "ess-id"
password =  "passwd"
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

if( i2c.scan()[0] == 0x76 ):
    bme = bme280.BME280(i2c=i2c)
    am = ambient.Ambient(ch-id, 'write-key')

    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    while station.isconnected() == False: pass
    print( station.ifconfig() )

    print(bme.values)
    data = bme.read_compensated_data()
    r = am.send({'d1': data[0] / 100.0, 'd2': data[2] / 1024.0, 'd3': data[1] / 25600.0})
    print(r.status_code)
    r.close()
    esp.deepsleep( 600 * 1000000 )
else:
    print('BME280 error!')
    

