#James Fuller, ID: 001523156
import csv
from MyHash import *
from Truck import *
from Pack import *

#Takes data from CSV file and assembles distance table and a dictionary of addresses and their index in the distance table
def load_distance_table(distanceTable, addressNameList):
    with open('WGUPSDistanceTable.csv') as tempData:                #Opens the csv file to be read
        for line in tempData.readlines():
            distanceTable.append(line.split('\n')[0].split(','))    #Removes the '\n' from the end of string, then splits each value data into set
        addressListTemp = distanceTable.pop(0)
        for i in range(len(addressListTemp)):                       #Takes the number value for the list of names
            addressNameList[addressListTemp[i]] = [i, []]           #Adds the distanceTable value for the address and a list of corresponding packages into dict
    floatDistanceTable = []
    for i in distanceTable:                                         #This goes through distance table and converts each string into float
        floatDistanceTable.append([float(j) for j in i])
    return floatDistanceTable, addressNameList

#Prints all items in truck, then prints last truck location and truck mileage
def  print_truck(truck, time):
    print("All packages in Truck #" + str(truck.number) +" at: " + time)
    for item in truck.priorityPackages:
        print(packageDict.retreive(item))
    for item in truck.standardPackages:
        print(packageDict.retreive(item))
    print("Truck last location: " + truck.location)
    print("Truck mileage: " + str(round(truck.mileage, 1)))
    print()

#A function which takes the number of minutes after 8 AM and outputs the time in standard 12 hour format
def time_function(time):                            
    daytime = "AM"
    if time >= 240:
        daytime = "PM"
    hour = str((8 + int(time/60)) % 12)
    if time % 60 >= 10:
        minute = str(int(round(time % 60)))
    else: 
        minute = '0' + str(int(time % 60))
    return hour + ':' + minute + " " + daytime

#Moves the truck through the stops until the requested time and prints all package values and the truck distance
def increment_truck(truck, time, endTime, packageDict, distanceTable):
    keyValueThisAddress = 0                                                     #This is the iD number of the current package being transported
    keyValueLast = 0                                                            #iD number of the previous package

    keyValueThisAddress = truck.priorityPackages[truck.currPackage]             #currPackage is the number this package sits in the truck's route order
    keyValueLast = truck.priorityPackages[truck.currPackage - 1]                #This finds the previous package iD
    distanceTableThis = packageDict.retreive(keyValueThisAddress).addressIndex  #This finds the index of the current package in the distance table list
    distanceTableLast = packageDict.retreive(keyValueLast).addressIndex         #Finds the index of the previous package

    while time <= endTime:                                                      #Loops the truck while the time is above the ending time to check in
        if truck.startTime <= time:                                             #As long as the truck has gone out
            if truck.startTime == time:                                         #When the truck starts moving
                keyValueThisAddress = truck.priorityPackages[0] #
                keyValueLast = 0

                distanceTableThis = 0                                           #Generates correct values for the hub in the distance table
                distanceTableLast = 0
                distanceTableThis = packageDict.retreive(keyValueThisAddress).addressIndex

                for package in truck.priorityPackages:                          #Initializes all the packages to "in transit"
                    packageDict.retreive(package).status = "in transit"
                if time == endTime:
                    print_truck(truck, time_function(endTime))
                    return truck
    
            #checks that this isn't the first and delivering the current package wont bring it past the endTime
            if truck.currPackage != (len(truck.priorityPackages) -1) and time < endTime:    #If this is not the last package
                #This is a hard to read line, but all it does is check that adding the next package wont take the truck over the endTime time.
                if (time + (distanceTable[distanceTableThis][packageDict.retreive(truck.priorityPackages[truck.currPackage+1]).addressIndex] * minutesPerMile)) > endTime: 
                    print_truck(truck, time_function(endTime))                              #Prints the truck and exits the loop if true
                    return truck

                elif truck.currPackage == -1:                                               #If this is the first package
                    truck.location = packageDict.retreive(keyValueThisAddress).address      #Updates mileage, time, location for truck
                    truck.mileage = distanceTable[0][distanceTableThis]
                    truck.time = (distanceTable[0][distanceTableThis] * minutesPerMile)
                    time += (distanceTable[0][distanceTableThis] * minutesPerMile)
                    packageDict.retreive(keyValueThisAddress).status = "Delivered: " + time_function(time)
                    truck.currPackage = 0

                else: #If this is any package other than first or last
                    keyValueThisAddress = truck.priorityPackages[truck.currPackage +1]      #Takes next address index
                    keyValueLast = truck.priorityPackages[truck.currPackage]

                    distanceTableThis = packageDict.retreive(keyValueThisAddress).addressIndex #Finds next address index
                    distanceTableLast = packageDict.retreive(keyValueLast).addressIndex     #Sets current address index

                    #Updates mileage, time, location for truck, delivery info for package and overall time
                    truck.location = packageDict.retreive(keyValueThisAddress).address 
                    truck.mileage += distanceTable[distanceTableLast][distanceTableThis]
                    truck.time += (distanceTable[distanceTableLast][distanceTableThis] * minutesPerMile)
                    time += (distanceTable[distanceTableLast][distanceTableThis] * minutesPerMile)
                    packageDict.retreive(keyValueThisAddress).status = "Delivered: " + time_function(time)
                    truck.currPackage += 1                                                      #Increments value to next package in list
            else:                                                                               #If this is the last package on truck
                truck.location = 'Hub'                                                          #Moves truck back to hub
                truck.mileage += distanceTable[distanceTableThis][0]                            #Adds distance returning to hub to mileage
                print_truck(truck, time_function(endTime))                                      #Prints truck and returns truck with completed route
                return truck
        else:
            time += 1                                                                           #Increments time upward if the truck hasn't started moving yet
    print_truck(truck, time_function(endTime))                                                  #Prints and returns the truck if the loop is broken without the truck moving
    return truck
            
if __name__ == "__main__":
    INIT_SIZE = 40                                  #Number of packages in program
    MPH = 18                                        #Average miles per hour of truck
    minutesPerMile = (1/(MPH/60))                   #The number of minutes each mile of traveling takes at 18MPH
    time = 0                                        #Calculated as minutes after 8:00 AM
    userTime = 0
    distanceTable = []                              #The table of all distances between addresses

    #A dictionary with all addresses as keys, and a definition with an index for the distance table and all matching packages
    addressNameList = {}                            
    packageDict = MyHash(INIT_SIZE)

    distanceTable, addressNameList = load_distance_table(distanceTable, addressNameList)
    packageDict, addressNameList = load_package_data(packageDict, addressNameList)

    #Create truck objects using truck number and planned start time
    truck1 = Truck(1, 0)
    truck2 = Truck(2, 65)
    truck3 = Truck(3, 140)

    #Load packages into trucks based on priority and start time
    truck1, truck2, truck3 = load_trucks(truck1, truck2, truck3, packageDict, INIT_SIZE)

    #Optimize routes with greedy algorithm and format truck for correct printing
    truck1 = optimize_truck_route(truck1, distanceTable, packageDict)
    truck2 = optimize_truck_route(truck2, distanceTable, packageDict)
    truck3 = optimize_truck_route(truck3, distanceTable, packageDict)
    print('Enter Time: Please use military time, and only times after 0800 accepted')

    userTime = (int(input()) - 800)
    userTime = (int(userTime/100)*60) + (userTime %100)
    while (userTime < 0) or userTime >= 960:
        print('Enter Time: Please use military time, and only times after 0800 accepted')
        userTime = (int(input()) - 800)
        userTime = (userTime/100*60) + (userTime %100)

    #Update relevant information from the package with a wrong address then re-sort truck packages
    if userTime >= 140:
        packageDict.retreive(9).address = "410 S State St., Salt Lake City"
        packageDict.retreive(9).zipCod = "84111"
        packageDict.retreive(9).addressIndex = packageDict.retreive(5).addressIndex
        truck3 = optimize_truck_route(truck3, distanceTable, packageDict)

    #Moves trucks along routes until userTime then prints status
    truck1 = increment_truck(truck1, time, userTime, packageDict, distanceTable)
    truck2 = increment_truck(truck2, time, userTime, packageDict, distanceTable)
    truck3 = increment_truck(truck3, time, userTime, packageDict, distanceTable)

    print()
    print("Total mileage for all trucks: " + str(round((truck1.mileage + truck2.mileage + truck3.mileage), 1)))