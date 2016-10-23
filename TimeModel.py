from datetime import datetime
import urllib2
import json
import math
import numpy as np

class UrgentCareCenter:
    def __init__(self, entry):
        entry_array = entry.split(',')
        self.name = entry_array[0]
        self.address = entry_array[1].replace(';', ',')
        self.monday_hours = [datetime.strptime(entry_array[2].split('-')[0].rstrip().lstrip(), '%I:%M %p'),
                             datetime.strptime(entry_array[2].split('-')[1].rstrip().lstrip(), '%I:%M %p')]
        self.tuesday_hours = [datetime.strptime(entry_array[3].split('-')[0].rstrip().lstrip(), '%I:%M %p'),
                              datetime.strptime(entry_array[3].split('-')[1].rstrip().lstrip(), '%I:%M %p')]
        self.wednesday_hours = [datetime.strptime(entry_array[4].split('-')[0].rstrip().lstrip(), '%I:%M %p'),
                                datetime.strptime(entry_array[4].split('-')[1].rstrip().lstrip(), '%I:%M %p')]
        self.thursday_hours = [datetime.strptime(entry_array[5].split('-')[0].rstrip().lstrip(), '%I:%M %p'),
                               datetime.strptime(entry_array[5].split('-')[1].rstrip().lstrip(), '%I:%M %p')]
        self.friday_hours = [datetime.strptime(entry_array[6].split('-')[0].rstrip().lstrip(), '%I:%M %p'),
                             datetime.strptime(entry_array[6].split('-')[1].rstrip().lstrip(), '%I:%M %p')]
        self.saturday_hours = [datetime.strptime(entry_array[7].split('-')[0].rstrip().lstrip(), '%I:%M %p'),
                               datetime.strptime(entry_array[7].split('-')[1].rstrip().lstrip(), '%I:%M %p')]
        try:
            self.sunday_hours = [datetime.strptime(entry_array[8].split('-')[0].rstrip().lstrip(), '%I:%M %p'),
                                 datetime.strptime(entry_array[8].split('-')[1].rstrip().lstrip(), '%I:%M %p')]
        except:
            self.sunday_hours = [datetime.strptime('01:00 am', '%I:%M %p'), datetime.strptime('01:00 am', '%I:%M %p')]


class EmergencyRoom:
    def __init__(self, entry):
        entry_array = entry.split(',')
        self.name = entry_array[0]
        self.address = entry_array[1].replace(';', ',')

def ER_wait_time(ER, day, time):
    names = ['St. Joseph\'s Health Centre','Mount Sinai Hospital','Women\'s College Hospital','St. Michael\'s Hospital','The Hospital for Sick Children','Sunnybrook Health Sciences Centre','Toronto General Hospital','Toronto Western Hospital','North York General Hospital','Etobicoke General Hospital','Humber River Hospital','Michael Garron Hospital','The Scarborough Hospital','West Park Healthcare Centre','Credit Valley Hospital','Mississauga Hospital','MacKenzie Health','Markham Stouffville Hospital','Brampton Civic Hospital']
    # Times that are not available are replaced with 2.2 (provincial average)
    total_time = [2.3,2.6,2.2,2.9,2.2,2.6,2.5,2.6,2.0,2.0,2.9,2.2,2.1,2.2,2.5,2.2,2.9,3.3,2.3]
    for index in range(len(total_time)):
        total_time[index] = total_time[index] / 2.2

    wait_times = [[5.1,4.5,3.6,4.2,4.5,4.3,4.4,4.6],[5.6,4.7,3.7,4.1,4.2,4.1,4.2,4.6],[5.4,4.6,3.6,4.1,4.2,4.0,4.0,4.3],[5.1,4.6,3.5,4.0,4.1,4.1,4.1,4.5],[5.2,4.6,3.7,4.1,4.3,4.2,4.2,4.7],[5.8,4.7,3.6,3.7,3.9,3.8,3.9,4.2],[5.2,5.1,3.6,3.8,4.0,3.8,3.8,4.2]]

    if(day == 'Monday'):
        day_index = 0
    elif(day == 'Tuesday'):
        day_index = 1
    elif(day == 'Wednesday'):
        day_index = 2
    elif(day == 'Thursday'):
        day_index = 3
    elif(day == 'Friday'):
        day_index = 4
    elif(day == 'Saturday'):
        day_index = 5
    else:
        day_index = 6

    day_times = wait_times[day_index]
    true_index = time / (180 * 60 * 1.0)
    first_index = int(math.floor(true_index))
    last_index = int(math.ceil(true_index))
    wait_time = day_times[first_index] * (1 - (true_index - first_index)) + (true_index - first_index) * day_times[last_index]

    try:
        index = names.index(ER)
        return total_time[index] * wait_time
    except:
        print(ER)
        return 'Error'

def UCC_wait_time():
    return (np.random.exponential(scale=15)/60.0)

def time_within(time, open, close):
    if((time > int(open.strftime('%H'))*3600 + int(open.strftime('%M'))*60) and (time < int(close.strftime('%H'))*3600
        + int(close.strftime('%M'))*60)):
        return True
    else:
        return False

def is_open(UCC,date,time):
    if(date == 'Monday'):
        return(time_within(time, UCC.monday_hours[0], UCC.monday_hours[1]))
    elif(date == 'Tuesday'):
        return(time_within(time,UCC.tuesday_hours[0],UCC.tuesday_hours[1]))
    elif(date == 'Wednesday'):
        return(time_within(time, UCC.wednesday_hours[0], UCC.wednesday_hours[1]))
    elif(date == 'Thursday'):
        return(time_within(time,UCC.thursday_hours[0],UCC.thursday_hours[1]))
    elif(date == 'Friday'):
        return(time_within(time,UCC.friday_hours[0],UCC.friday_hours[1]))
    elif(date == 'Saturday'):
        return(time_within(time,UCC.saturday_hours[0],UCC.saturday_hours[1]))
    elif(date == 'Sunday'):
        return(time_within(time,UCC.sunday_hours[0],UCC.sunday_hours[1]))
    else:
        return False

def TravelTimesCar(origin, centers):
    origin = origin.replace(' ','+')
    destinations = ""
    for element in centers:
        destinations += (element.address.replace(' ','+') + '|')
    response = urllib2.urlopen('https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=' + origin + '&destinations=' + destinations)
    travel_data = json.loads(response.read())
    travel_times = []
    for element in travel_data['rows'][0]['elements']:
        travel_times.append(int(element['duration']['value']))
    return travel_times

def TravelTimesTransit(origin, centers):
    origin = origin.replace(' ','+')
    destinations = ""
    for element in centers:
        destinations += (element.address.replace(' ','+') + '|')
    response = urllib2.urlopen('https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=' + origin + '&destinations=' + destinations + '&mode=transit&key=AIzaSyDs8-5I2cCwDZaQ5B84I_YbWXo5fIIOyuk')
    travel_data = json.loads(response.read())
    travel_times = []
    for element in travel_data['rows'][0]['elements']:
        travel_times.append(int(element['duration']['value']))
    return travel_times

# Executing Code
def BestLocations(start,date,time_seconds):
    # Start: Current Location
    # Date is day of week: 'Monday', 'Tuesday', 'Wednesday', ...
    # time_seconds: time since midnight in seconds
    UCC_car_time = TravelTimesCar(start, UrgentCareCenters)
    ER_car_time = TravelTimesCar(start, EmergencyRooms)

    UCC_transit_time = TravelTimesTransit(start, UrgentCareCenters)
    ER_transit_time = TravelTimesTransit(start, EmergencyRooms)

    ERs = []
    UCCs = []
    ER_addresses = []
    UCC_addresses = []
    ER_wait_times = []
    UCC_wait_times = []
    ER_total_car_time = []
    UCC_total_car_time = []
    ER_total_transit_time = []
    UCC_total_transit_time = []

    for element in EmergencyRooms:
        ERs.append(element.name)
        ER_addresses.append(element.address)
        ER_wait_times.append(ER_wait_time(element.name,date,time_seconds))

    for element in UrgentCareCenters:
        UCCs.append(element.name)
        UCC_addresses.append(element.address)
        UCC_wait_times.append(UCC_wait_time())

    for index in range(len(EmergencyRooms)):
        ER_total_car_time.append(ER_car_time[index] + 3600*ER_wait_times[index])
        ER_total_transit_time.append(ER_transit_time[index] + 3600*ER_wait_times[index])

    for index in range(len(UrgentCareCenters)):
        UCC_total_car_time.append(UCC_car_time[index] + 3600*UCC_wait_times[index])
        UCC_total_transit_time.append(UCC_transit_time[index] + 3600*UCC_wait_times[index])

    venue_objects = EmergencyRooms + UrgentCareCenters
    venue = ERs + UCCs
    venue_addresses = ER_addresses + UCC_addresses
    venue_wait_times = ER_wait_times + UCC_wait_times
    # venue_car_time = ER_car_time + UCC_car_time
    # venue_transit_time = ER_transit_time + UCC_transit_time
    venue_total_car_time = ER_total_car_time + UCC_total_car_time
    venue_total_transit_time = ER_total_transit_time + UCC_total_transit_time
    venue_type = (['ER'] * len(ERs)) + (['UCC'] * len(UCCs))

    best_indicies = []
    best_venues = []
    best_addresses = []
    best_wait_times = []
    best_total_car_time = []
    best_total_transit_time = []
    best_venue_type = []

    temp_index = 0
    temp_total_car_time = 10000000
    for index in range(len(venue)):
        if(venue_type[index] == 'UCC' and is_open(venue_objects[index],date,time_seconds) == False):
            continue
        if(venue_total_car_time[index] < temp_total_car_time):
            temp_index = index
            temp_total_car_time = venue_total_car_time[index]

    best_indicies.append(temp_index)
    best_venues.append(venue[temp_index])
    best_addresses.append(venue_addresses[temp_index])
    best_wait_times.append(venue_wait_times[temp_index])
    best_total_car_time.append(venue_total_car_time[temp_index])
    best_total_transit_time.append(venue_total_transit_time[temp_index])
    best_venue_type.append(venue_type[temp_index])

    # Run 2 - Finding 2nd best location
    temp_total_car_time = 10000000
    for index in range(len(venue)):
        if(venue_type[index] == 'UCC' and is_open(venue_objects[index],date,time_seconds) == False):
            continue
        if(index in best_indicies):
            continue
        if(venue_total_car_time[index] < temp_total_car_time):
            temp_index = index
            temp_total_car_time = venue_total_car_time[index]

    best_indicies.append(temp_index)
    best_venues.append(venue[temp_index])
    best_addresses.append(venue_addresses[temp_index])
    best_wait_times.append(venue_wait_times[temp_index])
    best_total_car_time.append(venue_total_car_time[temp_index])
    best_total_transit_time.append(venue_total_transit_time[temp_index])
    best_venue_type.append(venue_type[temp_index])

    # Run 3 - Finding 3rd best location
    temp_total_car_time = 10000000
    for index in range(len(venue)):
        if(venue_type[index] == 'UCC' and is_open(venue_objects[index],date,time_seconds) == False):
            continue
        if(index in best_indicies):
            continue
        if(venue_total_car_time[index] < temp_total_car_time):
            temp_index = index
            temp_total_car_time = venue_total_car_time[index]

    best_indicies.append(temp_index)
    best_venues.append(venue[temp_index])
    best_addresses.append(venue_addresses[temp_index])
    best_wait_times.append(venue_wait_times[temp_index])
    best_total_car_time.append(venue_total_car_time[temp_index])
    best_total_transit_time.append(venue_total_transit_time[temp_index])
    best_venue_type.append(venue_type[temp_index])

    return [['Venues','Addresses','Wait Times','Total Time (Car)','Total Time (Transit)','Venue Type'],best_venues,best_addresses,best_wait_times,best_total_car_time,best_total_transit_time,best_venue_type]


if __name__ == "__main__":
    # Load locations - Reading Files
    ucc_file = open('UrgentCareCenters.csv')
    ucc_file.readline()
    ucc_file.readline()
    # print(input_file.readline())
    UrgentCareCenters = []
    for line in ucc_file:
        UrgentCareCenters.append(UrgentCareCenter(line))
    ucc_file.close()

    er_file = open('EmergencyRooms.csv')
    er_file.readline()
    er_file.readline()
    EmergencyRooms = []
    for line in er_file:
        EmergencyRooms.append(EmergencyRoom(line))
    er_file.close()

    list_of_lists = BestLocations("110 Simcoe Street", "Monday", 200)
    print(BestLocations("110 Simcoe Street", "Monday", 200))

    # for element in BestLocations('110 Charles St West, Toronto, Ontario','Thursday',35000):
    #     print(element)