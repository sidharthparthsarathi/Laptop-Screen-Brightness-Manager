#Import Required Modules
import time,json,screen_brightness_control as sbc 
from boltiot import Bolt

#Api Key can be obtained from your bolt cloud account 
api_key = "692df97a-24d7-4e11-a575-f78a7f11a8f1"

#Device Id can be obtained from your bolt cloud account 
device_id  = "BOLT290870"

#Initializing Bolt Class
mybolt = Bolt(api_key, device_id)

#Minimum Brightness Of Your Screen
minm_br=6

#Infinite Loop
while True:
   
   #Test a block of code for errors
   try:

      #get the current level of brightness
      a=sbc.get_brightness()
      print("Current Brightness Value:",a)

      #store the data in json format
      response =json.loads(mybolt.analogRead('A0'))

      #store the value of the response in a variable
      c=response['value']

      #check if it is a number or not
      if(c.isnumeric()):
         print("Light Sensor Value Is:",c)

         #conver the light sensor value to match the brightness level
         b=int(int(c)*(100/1024))
         print("Converted Value Of Light Sensor Is:",b)

         #assign the value of b to br for future use
         br=b

         #check if sensor value is less than brightness level and according to that decrease the brightness
         if(b<a):

            #minimum level of brightness is 6
            if(a!=minm_br):
               if(b<minm_br):

                  #minimum brightness can't be below 6 in windows
                  br=minm_br
               print("Your Brightness Will Be Decreased To:",br)

               #to produce a low frequency sound when brightness decreases
               mybolt.analogWrite('1','120')
               time.sleep(0.7)

               #off the buzzer after 0.7 seconds
               mybolt.digitalWrite('1','LOW')
               if(b<7):
                  for i in range(a-1,minm_br-1,-1):
                     
                     #Set brightness in Decreasing order 
                     sbc.set_brightness(i)
               elif(b>minm_br):
                  for i in range(a-1,int(b)-1,-1):

                     #Set brightness in Decreasing order 
                     sbc.set_brightness(i)

         #check if sensor value is more than brightness level and according to that increase the brightness
         elif(b>a):
            print("Your Brightness Will Be Increased To:",int(b))

            #to produce a high frequency sound when brightness decreases
            mybolt.analogWrite('1','255')
            time.sleep(0.7)

            #off the buzzer after 0.7 seconds
            mybolt.digitalWrite('1','LOW')
            if(b>minm_br):
               for i in range(a+1,int(b)+1):

                  #Set brightness in increasing order 
                  sbc.set_brightness(i)

      #if value of response is in string format then print it            
      else:
         print(c)

         #check for the condition "Command timed out" and allow buzzer to buzz
         if(c=="Command timed out"):
            mybolt.digitalWrite('1','HIGH')
            time.sleep(2)
            mybolt.digitalWrite('1','LOW')

   #Handle the errors
   except Exception as e: 
        print ("Error occured: Below are the details")
        print (e)
        mybolt.digitalWrite('1','HIGH')

        #allow the buzzer to buzz for 5 seconds
        time.sleep(5)

        #then off the buzzer
        mybolt.digitalWrite('1','LOW')

   #Puts the program execution on hold for 1 second
   time.sleep(0.5)
