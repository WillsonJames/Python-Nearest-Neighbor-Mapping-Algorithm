class Pack:
    def __init__(self, iD, address, city, zipCod, deadline, mass, truckPreference, linkedPacks, startDelay):
        self.iD = iD
        self.address = address                                          #Address packace to be delivered to
        self.addressIndex = 0                                           #Adresses location in the distance array
        self.city = city
        self.zipCod = zipCod
        self.deadline = deadline                                        #Time before which this package needs to be delivered
        self.deadlineEffective = deadline                               #The effective deadline after linking earliest deadline of packages with same address
        self.mass = mass                                                #Mass value of package
        self.truckPreference = truckPreference                          #Number of truck requested in note if applicable
        self.linkedPacks = linkedPacks                                  #Set of packages that must go with this one either because of link in notes
        self.startDelay = startDelay                                    #The earliest time this package can go out in minutes after 0800
        self.status =  'at the hub'                                     #current status of package delivery "at the hub", "in transit", or "delivered"

    #Overrides print function to print all relevant variables of package
    def __str__(self):                                
        printerPhrase = 'ID: ' + str(self.iD) + ' Address: ' + self.address + ", " + self.city + " " + self.zipCod + " Deadline: " + self.deadline + " Mass: " + self.mass + " Status: " + self.status
        return printerPhrase

#Takes packages from a csv file and formats their data into a package class
def load_package_data(packageDict, addressNameList):
    with open('WGUPS.csv') as tempData:                                 #Opens the csv file to be read
        for line in tempData.readlines():                               #Takes each line seperately since each line represents a package
            
            #Splits the package line, initiates each variable to create Pack object, then loads it with corresponding data point from the split line
            iD = 0
            iD = int(line.split(',')[0])
            address = ' '
            address = line.split(',')[1]
            city = ''
            city = line.split(',')[2]
            zipCod = ''
            zipCod = line.split(',')[4]
            deadline = ''
            deadline = line.split(',')[5]
            mass = ''
            mass = line.split(',')[6]

            #These varaibles are the special exceptions which come from the note instructions
            linkedPacks = set('')
            truckPreference = 0
            startDelay = 0

            #Each variable is updated if specific instructions from the note apply by checking against the first words
            if line.split(',')[7].startswith('Can only be on truck 2'):
                truckPreference = 2
            elif line.split(',')[7].startswith('Must be delivered with'):
                linkedPacks = set([13, 14, 15, 16, 19, 20, 21])
            elif line.split(',')[7].startswith('Delayed'):
                startDelay = 905
            elif line.split(',')[7].startswith('Wrong address'):
                startDelay = 1020

            #Adds the package iD as the name for the package in the hashtable, and uses the variables to create a pack object in dict
            tempPack = Pack(iD, address, city, zipCod, deadline, mass, truckPreference, linkedPacks, startDelay)
            packageDict.addVal(iD, tempPack)

    #Function which adds address index in distance table for each package
    packageDict.retreive(9).address = "ERROR"
    for i in range(1, 41):                                                                      #Takes indexes for all packages
        tempPack = packageDict.retreive(i)
        if i != 9:
            addressNameList[tempPack.address][1] = addressNameList[tempPack.address][1] + [i]   #Adds package number to adress dict
            tempPack.addressIndex = addressNameList[tempPack.address][0]                        #Adds adress index in pack class

    #Goes through address dictionary and links relevant stats for adresses with same package
    for packageList in addressNameList:                                              
        if len(addressNameList[packageList][1]) > 1:                                            #If more than one package have this address
            deadlineEffective = 'EOD'
            truckPreference = 0
            startDelay = 0
            for i in range(len(addressNameList[packageList][1])):

                #Finds truck preference of packages with same address
                if packageDict.retreive(addressNameList[packageList][1][i]).truckPreference != 0:
                    truckPreference = packageDict.retreive(addressNameList[packageList][1][i]).truckPreference

                #Finds earliest deadlines for packages with same address
                if packageDict.retreive(addressNameList[packageList][1][i]).deadline != 'EOD' and deadlineEffective != '9:00 AM':
                    deadlineEffective = packageDict.retreive(addressNameList[packageList][1][i]).deadline

                #Finds latest start delay of packages with same address   
                if packageDict.retreive(addressNameList[packageList][1][i]).startDelay != 0 and startDelay != 1020:
                    startDelay = packageDict.retreive(addressNameList[packageList][1][i]).startDelay

            for i in range(len(addressNameList[packageList][1])):

                #Links truck preference of packages with same address
                packageDict.retreive(addressNameList[packageList][1][i]).truckPreference = truckPreference

                #Links earliest deadlines for packages with same address
                packageDict.retreive(addressNameList[packageList][1][i]).deadlineEffective = deadlineEffective

                #Links start delay of packages with same address
                packageDict.retreive(addressNameList[packageList][1][i]).startDelay = startDelay
    #Returns the now filled dictionary
    return packageDict, addressNameList                                             