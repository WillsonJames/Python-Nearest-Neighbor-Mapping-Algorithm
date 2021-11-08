class MyHash:
    def __init__(self, initSize):
        self.size = initSize                            #Variable for initial size of array
        self.mapping = []
        for item in range(initSize):                    #Loads the hash table with a blank space for every key to be entered
            self.mapping.append([])

    #Takes the input and outputs correct value in index
    def ahash(self, key):
        theHash = (key - 1)%40
        return theHash

    #Uses the ahash function to generate index, then adds new value point at this location
    def addVal(self, key, value):
        theHash = self.ahash(key)

    #Handles collisions by appending multiple items in list if it is not already blank
        if self.mapping[theHash] != []:
            self.mapping[theHash].append([key, value])
        else:
            self.mapping[theHash] = [key, value]
        return

    #Takes input and returns the package item at this location if it exists
    def retreive(self, key):
        thisHash = self.ahash(key)
        if self.mapping[thisHash][0] == key:
            return self.mapping[thisHash][1]
            
    #Handles collisions in lookup by going through all items with this key value and finding the correct item
        else:
            for item in range(len(self.mapping[thisHash])):
                if self.mapping[thisHash][item] == key:
                    return self.mapping[thisHash][item+1]

    #Takes input and prints the package item at this location if it exists
    def print(self, key):
        thisHash = self.ahash(key)
        if self.mapping[thisHash][0] == key:
            print(self.mapping[thisHash][1])
            return
            
    #Handles collisions in lookup by going through all items with this key value and finding the correct item
        else:
            for item in range(len(self.mapping[thisHash])):
                if self.mapping[thisHash][item] == key:
                    print(self.mapping[thisHash][item+1])
                    return




