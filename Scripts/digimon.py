## digimon ##

import edizon

saveFileBuffer = edizon.getSaveFileBuffer()

# initialize variables

# sets the current selected slot for digiconvert
digiconvert_slot = 0
fieldguide_slot = 0

def getDummyValue():
    strArgs = edizon.getStrArgs()
    type = strArgs[0]
    if type == "digiconvert":
        global digiconvert_slot
        return digiconvert_slot + 1
    elif type == "digiconvert_all":
        return getDigiConvertBool()
    elif type == "fieldguide":
        global fieldguide_slot
        return fieldguide_slot + 1
    elif type == "fieldguide_all":
        return getFieldGuideBool()
        
def getDigiConvertBool():
    # checks if theres any digiconvert percentage that is 0
    # if theres is, then set widget value to 0, else to 1
    
    # digiconvert percentage starts at address 0xB012; first digimon/slot in digiconvert list
    address = int("B012", 16)
    valueSize = 2
    getBool = 1
    
    # 346 as in the 346 slots in digiconvert list; may change in the future
    for slot in range(346):
        value = 0
        # slot * 4 meaning the 4 bytes per digimon in the list
        for i in range(0, valueSize):
            value = value | (saveFileBuffer[address + (slot*4) + i] << i * 8)
            if value == 0:
                getBool = 0
                break;
            
    return getBool
    
def getFieldGuideBool():
    # checks if theres any field guide value that is 0
    # if theres is, then set widget value to 0, else to 1
    
    # field guide value starts at address 9D0; first digimon/slot in field guide list
    address = int("9D0", 16)
    valueSize = 2
    getBool = 1
    
    # 351 as in the 351 slots in field guide list; may change in the future
    for slot in range(351):
        value = 0
        # slot * 8 meaning the 8 bytes per digimon in the list
        for i in range(0, valueSize):
            value = value | (saveFileBuffer[address + (slot*8) + i] << i * 8)
            if value == 0:
                getBool = 0
                break;
            
    return getBool
    
def setDummyValue(value):
    global digiconvert_slot
    global fieldguide_slot
    
    strArgs = edizon.getStrArgs()
    type = strArgs[0]
    if type == "digiconvert":
        value -= 1
        digiconvert_slot = value
    elif type == "digiconvert_all":
        setDigiConvertAll()
    elif type == "fieldguide":
        value -= 1
        fieldguide_slot = value
    elif type == "fieldguide_all":
        setFieldGuideAll()
        
def setDigiConvertAll():
    # sets all the digiconvert to 200%
    
    # digiconvert percentage starts at address 0xB012; first digimon/slot in digiconvert list
    address = int("B012", 16)
    # byte size = 2
    valueSize = 2 
    # value 200 being 200%
    value = 200
    
    # 346 as in the 346 slots in digiconvert list; may change in the future
    for slot in range(346):
        # slot * 4 meaning the 4 bytes per digimon in the list
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*4) + i] = (value & (0xFF << i * 8)) >> (i * 8)
            
def setFieldGuideAll():
    # set all field guide list to 3, meaning digimon is digiconvertible in-game
    
    # field guide value starts at address 9D0; first digimon/slot in field guide list
    address = int("9D0", 16)
    # byte size = 4
    valueSize = 4
    # value 3 = digiconvertible in-game
    value = 3
    
    # 351 as in the 351 slots in digiconvert list; may change in the future
    for slot in range(351):
        # slot * 8 meaning the 8 bytes per digimon in the list
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*8) + i] = (value & (0xFF << i * 8)) >> (i * 8)
        
def getValueFromSaveFile():
    strArgs = edizon.getStrArgs()
    intArgs = edizon.getIntArgs()
    address = int(strArgs[0], 16)
    valueSize = intArgs[0]
    
    value = 0
    
    if len(strArgs) == 2:
        type = strArgs[1]
        value = getCustValueFromSaveFile(address, type, valueSize, value)
    else:
        for i in range(0, valueSize):
            value = value | (saveFileBuffer[address + i] << i * 8)
            
    return value
  
def getCustValueFromSaveFile(custAddress, custType, custValueSize, custValue):
    global digiconvert_slot
    global fieldguide_slot
    
    if custType == "digiconvert":
        for i in range(0, custValueSize):
            custValue = custValue | (saveFileBuffer[custAddress + (digiconvert_slot*4) + i] << i * 8)
    elif custType == "digiconvert_id":
        for i in range(0, custValueSize):
            custValue = custValue | (saveFileBuffer[custAddress + (digiconvert_slot*4) + i] << i * 8)
    elif custType == "fieldguide":
        for i in range(0, custValueSize):
            custValue = custValue | (saveFileBuffer[custAddress + (fieldguide_slot*8) + i] << i * 8)
    elif custType == "fieldguide_id":
        for i in range(0, custValueSize):
            custValue = custValue | (saveFileBuffer[custAddress + (fieldguide_slot*8) + i] << i * 8)
    
    return custValue

def setValueInSaveFile(value):
    strArgs = edizon.getStrArgs()
    intArgs = edizon.getIntArgs()
    address = int(strArgs[0], 16)
    valueSize = intArgs[0]
    
    if len(strArgs) == 2:
        type = strArgs[1]
        setCustValueInSaveFile(value, address, type, valueSize)
    else:
        for i in range(0, valueSize):
            saveFileBuffer[address + i] = (value & (0xFF << i * 8)) >> (i * 8)
            
def setCustValueInSaveFile(value, address, type, valueSize):
    global digiconvert_slot
    global fieldguide_slot
    
    if type == "digiconvert":
        for i in range(0, valueSize):
            saveFileBuffer[address + (digiconvert_slot*4) + i] = (value & (0xFF << i * 8)) >> (i * 8)
    elif type == "digiconvert_id":
        pass
    elif type == "fieldguide":
        for i in range(0, valueSize):
            saveFileBuffer[address + (fieldguide_slot*8) + i] = (value & (0xFF << i * 8)) >> (i * 8)
    elif type == "fieldguide_id":
        pass

def getModifiedSaveFile():
    return saveFileBuffer
