#I am Kobena Wiredu(kobenaw@yahoo.com)
#Just recently learnt python/Micropython. Please email me if you optimise the code

# Below details from Nextion Editor
# I use 3.2 NX4024J032 Enhance nextion display but should work for yours too
#It is recommended to make the vscope attribute global

"""
// Declare your Nextion objects - Example (page id = 0, component id = 1, component name = "b0") 
NexText tState = NexText(0, 3, "tState"); 
NexButton bOn = NexButton(0, 1, "bOn");
NexButton bOff = NexButton(0, 2, "bOff");
NexSlider h0 = NexSlider(0, 4, "h0");
NexText tSlider = NexText(0, 5, "tSlider"); #numeric slider used tSlider.val=h0.val set in nextion Editor
NexText tTempC = NexText(1, 3, "tTempC");
NexText tTempF = NexText(1, 6, "tTempF");
NexProgressBar jHumidity = NexProgressBar(1, 7, "jHumidity");
NexText tHumidity = NexText(1, 8, "tHumidity");
NexButton bUpdate = NexButton(1,10, "bUpdate");
"""
#Function to read DHT22 Sensor by RandomNerdTutorials.com
#Modified slightly by Kobena

def read_sensor():
  global temp, temp_percentage, hum,tempF
  temp = temp_percentage = hum = tempF = 0
  try:
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
      msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))

      temp_percentage = (temp+6)/(40+6)*(100)
      # uncomment for Fahrenheit
      tempF = temp * (9/5) + 32.0
      #temp_percentage = (temp-21)/(104-21)*(100)

      hum = round(hum, 2)
      return(msg)
    else:
      return('Invalid sensor readings.')
  except OSError as e:
    return('Failed to read sensor.')


end_cmd=b'\xFF\xFF\xFF'

global myframe
myframe = bytearray(7)

uart=UART(1,tx=25,rx=26,baudrate=9600)

def send(cmd):
    global response1
    uart.write(cmd)
    uart.write(end_cmd)
    time.sleep_ms(100)
    response1 = uart.read()
    #print("Response:", response1)

def send_and_get():
    global processlist
    #time.sleep_ms(100)
    uart.readinto(myframe)
    #print(myframe)  #Enable this for debugging
    processlist = list(myframe)
    #print(processlist) #Enable this for debugging
    #print(processlist[2]) #Enable this for debugging

#Just retrieve text on bON #Enable below for debugging
"""
send("get bOn.txt")
mylist = list(response1)
    
#delete the last 3 xffs
del mylist[-3:]
byteObj = bytes(mylist)
mychar = byteObj.decode("utf-8")

if (mychar == "pON"):
    print('Everything is ok')
"""
while True:    
    while not uart.any():       
    
        if uart.any():
            break  
     
    send_and_get()
    #print(myframe)   
    #print(processlist)
    #print(processlist[2])
    
    #bOn is activated
    if processlist[2] == 1:
        led.value(1)
        #tState.setText("State: on");
        send("tState.txt=\"status:on\"")
        print('LED is ON')
        
    #bOff is activated
    elif processlist[2] == 2:
        led.value(0)
        send("tState.txt=\"status:off\"")
        print('LED is OFF')
        
    #Slider
    elif processlist[2] == 4:
        send("get h0.val")
        time.sleep_ms(100)
        mylist = list(response1)    
        #delete the last 3 xffs
        del mylist[-3:]
        print(mylist)
        print('Slider Position: ',mylist[1])
        
        frequency = 5000
        led_pwm = PWM(Pin(5), frequency)
        for duty_cycle in range(0, 100):
            led_pwm.duty(mylist[1])
            time.sleep(0.005)

    elif processlist[2] == 10:
        read_sensor()
        #send("tTempC.txt=\"28.2\"")
        send("tTempC.txt=\""+str(temp)+"\"")
        send("tTempF.txt=\""+str(tempF)+"\"")
        send("tHumidity.txt=\""+str(hum)+"\"")
        send("jHumidity.val="+str(int(hum)))
    else:
        read_sensor()
        send("tTempC.txt=\""+str(temp)+"\"")
        send("tTempF.txt=\""+str(tempF)+"\"")
        send("tHumidity.txt=\""+str(hum)+"\"")
        send("jHumidity.val="+str(int(hum)))
    
    