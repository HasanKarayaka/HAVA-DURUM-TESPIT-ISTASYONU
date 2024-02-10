from machine import Pin , ADC, I2C,SoftI2C,UART,PWM
from bmp180 import BMP180
import network
import urequests
import random
import utime
from dht import DHT11, InvalidChecksum
from bmp085 import BMP180
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
ısık=Pin(15,Pin.IN)
pin = Pin(26, Pin.OUT, Pin.PULL_DOWN)
ısı = DHT11(pin)

Raindrop_AO = ADC(28)
soil = ADC(Pin(27))


i2c = SoftI2C(sda=Pin(0), scl=Pin(1), freq=100000)
bmp = BMP180(i2c)

ssid = "Komando"
password = "Erbaa6019"

def ConnectWiFi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        utime.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


ip = ConnectWiFi()


server = "http://api.thingspeak.com/"
apikey1= "UFI8UE2041NYES83"
apikey2="1RKRCNS40UB0UWCP"
apikey3="HW5213T6NJ9FFTHR"
apikey4="JPUNP0YW860BH0FA"
field = 1



def hava():
    if ısık.value()==1:
        print("gündüz \n")
        uart.write("Gündüz")
    elif ısık.value()==0:
        print("Gece \n")
        uart.write("Gece")
        
 

def nem_algilama():
    min_moisture=0
    max_moisture=65535

    
    moisture = (soil.read_u16())*100/(max_moisture-min_moisture) 
    
    utime.sleep(1) 
    return moisture






def pressure():

    i2c = I2C(1, sda = Pin(2), scl = Pin(3), freq = 1000) 
    bmp = BMP180(i2c)
    bmp.oversample = 2
    bmp.sealevel = 101325
    tempC = bmp.temperature    
    pres_hPa = bmp.pressure    
    altitude = bmp.altitude    
    print(str(tempC)+"°C " +str(temp_f)+"°F " + str(pres_hPa)+"hPa "+ str(altitude))
    time.sleep_ms(100)  
    return pres_hPa,altitude

while True:
    temperature = bmp.temperature
    pressure = bmp.pressure
    t  = (ısı.temperature)
    hava()
                     
     

    
    h = (ısı.humidity)
    print("Temperature: {}".format(ısı.temperature))
    print("Humidity: {}".format(ısı.humidity))
   
    
    
        
    print("Sıcaklık: {:.2f} °C, Basınç: {:.2f} hPa".format(temperature, pressure / 100.0))
    
    
    moist=nem_algilama()
    
    
    #basinc,yukseklik=pressure()
    print("Topraktaki_nem",moist)
    #sensor.measure()
    #t=sensor.temperature()
    #h=sensor.humidity()
    
    #print("temperature: {}".format(sensor.temperature))
   # print("humudity: {}".format(sensor.humidity))
    
    #print(t)

    url1 = f"{server}/update?api_key={apikey1}&field{field}={t}"
    url2 = f"{server}/update?api_key={apikey2}&field{field}={moist}"
    url3 = f"{server}/update?api_key={apikey3}&field{field}={pressure}"
    #url4 = f"{server}/update?api_key={apikey4}&field{field}={moist}"
#     url2= f"{server}/update?api_key={apikey2}&field{field}={yukseklik}"
    request = urequests.post(url1)
    request = urequests.post(url2)
    request = urequests.post(url3)
    #request = urequests.post(url4)
#     request = urequests.post(url2)
    request.close()
    
    utime.sleep(20)