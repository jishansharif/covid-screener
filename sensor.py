from smbus2 import SMBus
from mlx90614 import MLX90614


def run_sensor(sensor):
    temperature=[] #stores all the temperatures 
    nonsense=0 #avoids the non-sensical temperatures
    amount=10 #how many times sensor measures the temperatures
    values=0 #tracks how many times the sensor measured the temperature
    min_human=34 #minimum body temperature allowed 
    max_human=44 #maximum body temperature allowed 

    while values<amount: #gets the temperature for given amount times
        temp=sensor.get_object_1() #activates the sensor
        
        if temp>min_human and temp<max_human:#checks if the temperature makes sense
            temperature.append(temp) #adds the temperature to the list
            value+=1 #updates the amount of times sensor was used
            
        else: #if the value does not make sense
            nonsense+=1 #increases the non-sensical values
            
            if nonsense==5: #once there are 5 non sensical values measured
                nonsense=0 #resets the non-sensical values 
                print("Please stay in the range of the sensor for accrurate value")
                #Lets the user know to stay within the sensors' range

    average=sum(temperature)/len(temperature) #calculates the average of all temperatures 
    
    if average>min_human and average<max_human: #checks if it is valid
        return average #returns the average
    
    else: #if it is invalid
        run_sensor(sensor) #runs the sensor again
        
         
bus=SMBus(1)
sensor=MLX90614(bus, address=0x5A)
average=run_sensor(sensor)
bus.close()
