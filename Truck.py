class Truck:
    def __init__(self, number, startTime):
        self.number = number                                #ID number for the truck
        self.location = 'Hub'
        self.standardPackages = []                          #List of iDs for EOD delivery packages on the truck
        self.priorityPackages =[]                           #List of iDs for priority packages
        self.mileage = 0.0
        self.time = 0
        self.startTime = startTime                          #Time the truck leaves thereafter calculated as minutes from 8:00AM
        self.currPackage = -1

def load_trucks(truck1, truck2, truck3, packageDict, INIT_SIZE):
    routinePackages = []
    for i in range(1, INIT_SIZE +1):

        #All packages which need to be on truck 2 because of priority or late startTime
        if packageDict.retreive(i).truckPreference == 2 or packageDict.retreive(i).startDelay == 905:
            if packageDict.retreive(i).deadlineEffective != 'EOD':
                truck2.priorityPackages.append(i)
            else: 
                truck2.standardPackages.append(i)

        #If the package has no truck preference, has a deadline but has no start delay load it in truck 1 priority
        elif packageDict.retreive(i).truckPreference == 0 and packageDict.retreive(i).deadlineEffective != 'EOD' and packageDict.retreive(i).startDelay == 0:
            truck1.priorityPackages.append(i)

        #Add the package with a wrong address and late start delay into truck 3
        elif packageDict.retreive(i).startDelay == 1020:   
            truck3.standardPackages.append(i)

        #If none of these are true adds the package into the routine list
        else:
            routinePackages.append(i)

        #Goes through the list of routine packages and adds them to the trucks sequentially until each truck fills up
    for i in routinePackages:
        if len(truck1.priorityPackages + truck1.standardPackages) < 16:
            truck1.standardPackages.append(i)
        elif len(truck2.priorityPackages + truck2.standardPackages) < 16:
            truck2.standardPackages.append(i)
        else:
            truck3.standardPackages.append(i)
    return truck1, truck2, truck3

#Uses a greedy algorithm to sort packages by always going to the next closest stop
def optimize_truck_route(truck, distanceTable, packageDict):
    sortedPriority = []
    currIndex = 0                                                   #Tracks the column number for the current address
    nextIndex = 0                                                   #Holds the row number for the address being compared in address index
    
    for i in range(len(truck.priorityPackages)):                    #Goes through the list to find any 9:00AM delivery packages
        if packageDict.retreive(truck.priorityPackages[i]).deadline == "9:00 AM":
            sortedPriority.append(truck.priorityPackages[i])        #Adds the 9:00 AM package to the list first while removing it from the old list
            currIndex = packageDict.retreive(truck.priorityPackages[i]).addressIndex
            nextIndex = i
    if nextIndex != 0:
        truck.priorityPackages.pop(nextIndex)                       #Deletes added data point from old list, only works with 1 9:00am package

    #Does a greedy sort on all packages with deadlines by finding next address with the shortest distance
    while len(truck.priorityPackages) > 0:
        packNumber = 0                                              #The location in truck list to write new value
        shortestDistance = 99.9
        for i in range(len(truck.priorityPackages)):                #Goes through all remaining packages and finds the closest address
            thisAddressIndex = packageDict.retreive(truck.priorityPackages[i]).addressIndex
            if distanceTable[currIndex][thisAddressIndex] < shortestDistance:
                shortestDistance = distanceTable[currIndex][thisAddressIndex]
                nextIndex = thisAddressIndex
                packNumber = i    
        sortedPriority.append(truck.priorityPackages.pop(packNumber)) #Removes closest address and adds it to sorted list
        currIndex = nextIndex
    truck.priorityPackages = sortedPriority

    #Does the same greedy sort for all standard packages
    while len(truck.standardPackages) > 0:
        packNumber = 0                                              #The location in truck list to write new value
        shortestDistance = 99.9
        for i in range(len(truck.standardPackages)):
            thisAddressIndex = packageDict.retreive(truck.standardPackages[i]).addressIndex
            if distanceTable[currIndex][thisAddressIndex] < shortestDistance:
                shortestDistance = distanceTable[currIndex][thisAddressIndex]
                nextIndex = thisAddressIndex
                packNumber = i
        sortedPriority.append(truck.standardPackages.pop(packNumber)) #Adds the packages from the standard packages to the end of the previous list in sorted order
        currIndex = nextIndex
    truck.priorityPackages = sortedPriority                           #Adds the now sorted packages onto the truck
    return truck