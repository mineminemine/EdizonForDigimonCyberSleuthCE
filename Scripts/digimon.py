## digimon ##

import edizon

saveFileBuffer = edizon.getSaveFileBuffer()

## initialize variables
# sets the current selected slot for digiconvert
digiconvert_slot = 0
fieldguide_slot = 0
obtain_all_items_cs = 0
obtain_all_items_hm = 0

def getDummyValue():
    global digiconvert_slot
    global fieldguide_slot
    global obtain_all_items_cs
    global obtain_all_items_hm
    
    strArgs = edizon.getStrArgs()
    type = strArgs[0]
    if type == "inventory_all_cs":
        return obtain_all_items_cs
    elif type == "inventory_all_hm":
        return obtain_all_items_hm
    elif type == "digiconvert":
        return digiconvert_slot + 1
    elif type == "digiconvert_all_cs":
        return getDigiConvertBool("cs")
    elif type == "digiconvert_all_hm":
        return getDigiConvertBool("hm")
    elif type == "fieldguide":
        return fieldguide_slot + 1
    elif type == "fieldguide_all":
        return getFieldGuideBool()
        
def getDigiConvertBool(version = None):
    # checks if theres any digiconvert percentage that is 0
    # if theres is, then set widget value to 0, else to 1
    
    # digiconvert percentage starts at address 0xB012 or 0x6C7B2; first digimon/slot in digiconvert list
    if version == "cs":
        address = int("B012", 16)
    else:
        address = int("6C7B2", 16)
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
    if type == "inventory_all_cs":
        setInventoryAll("cs")
    elif type == "inventory_all_hm":
        setInventoryAll("hm")
    elif type == "digiconvert":
        value -= 1
        digiconvert_slot = value
    elif type == "digiconvert_all_cs":
        setDigiConvertAll("cs")
    elif type == "digiconvert_all_hm":
        setDigiConvertAll("hm")
    elif type == "fieldguide":
        value -= 1
        fieldguide_slot = value
    elif type == "fieldguide_all":
        setFieldGuideAll()
        
def setInventoryAll(version = None):
    ### obtain all items except for key items
    ## Don't thank me for this, thank AnalogMan @ GBATemp
    
    # inventory starts at either 0x3EB30 or 0xA02D0
    if version == "cs":
        address = int("3EB30", 16)
    else:
        address = int("A02D0", 16)
    # byte size = 4
    valueSize = 4
    value = 0
    
    USABLE_ITEM = 0; EQUIP_ITEM = 1; FARM_ITEM = 2; KEY_TEM = 3; MEDAL_ITEM = 4; ACCESSORY_ITEM = 5
    
    consumables = list(range(1, 34)) + list(range(50, 59)) + list(range(60, 68)) + list(range(70, 80)) + list(range(90, 92)) \
                    + list(range(100, 107)) + list(range(110, 128)) + list(range(200, 231))
    equipment = list(range(301, 404))
    farms = list(range(501,510)) + list(range(520, 540))
    medals = list(range(1001,1701))
    accessories = [10101, 12401, 10201, 12501, 10301, 10302, 12601, 
                10401, 10501, 10502, 12701, 12702, 12801, 
                12901, 13001, 10701, 10801, 10901, 10902, 
                13101, 13102, 13201, 11001, 11101, 13301, 
                13401, 11201, 11301, 13501, 11401, 11402, 
                11403, 13601, 11501, 11601, 13701, 13801, 
                13901, 11701, 11702, 11703, 14001, 14101, 
                11801, 11802, 14201, 11901, 12001, 12002, 
                12003, 14301, 12101, 12102, 12103, 14401, 
                14402, 14501, 12201, 12301, 12302, 12303]
    
    slot = 0
    unknownId = 1065353217 # this is the unknown 4 bytes at the start of every item; gonna keep it as it is for now
    itemQty = 95
    medalQty = 1
    for consumable in consumables:
        checking = 0
        for i in range(0, valueSize):
            checking = checking | (saveFileBuffer[address + (slot*24) + 8 + i] << i * 8)
        if checking == KEY_TEM:
            slot+=1
        # the beginning of any item; the unknown parts, usual value is as above unknownId
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + i] = (unknownId & (0xFF << i * 8)) >> (i * 8)
        # item type
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 8 + i] = (USABLE_ITEM & (0xFF << i * 8)) >> (i * 8)
        # item id
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 12 + i] = (consumable & (0xFF << i * 8)) >> (i * 8)
        # unknown, supposedly to be same as item id
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 16 + i] = (consumable & (0xFF << i * 8)) >> (i * 8)
        # item quantity
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 20 + i] = (itemQty & (0xFF << i * 8)) >> (i * 8)
        slot+=1
    for eqp in equipment:
        checking = 0
        for i in range(0, valueSize):
            checking = checking | (saveFileBuffer[address + (slot*24) + 8 + i] << i * 8)
        if checking == KEY_TEM:
            slot+=1
        # the beginning of any item; the unknown parts, usual value is as above unknownId
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + i] = (unknownId & (0xFF << i * 8)) >> (i * 8)
        # item type
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 8 + i] = (EQUIP_ITEM & (0xFF << i * 8)) >> (i * 8)
        # item id
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 12 + i] = (eqp & (0xFF << i * 8)) >> (i * 8)
        # unknown, supposedly to be same as item id
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 16 + i] = (eqp & (0xFF << i * 8)) >> (i * 8)
        # item quantity
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 20 + i] = (itemQty & (0xFF << i * 8)) >> (i * 8)
        slot+=1
    for farm in farms:
        checking = 0
        for i in range(0, valueSize):
            checking = checking | (saveFileBuffer[address + (slot*24) + 8 + i] << i * 8)
        if checking == KEY_TEM:
            slot+=1
        # the beginning of any item; the unknown parts, usual value is as above unknownId
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + i] = (unknownId & (0xFF << i * 8)) >> (i * 8)
        # item type
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 8 + i] = (FARM_ITEM & (0xFF << i * 8)) >> (i * 8)
        # item id
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 12 + i] = (farm & (0xFF << i * 8)) >> (i * 8)
        # unknown, supposedly to be same as item id
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 16 + i] = (farm & (0xFF << i * 8)) >> (i * 8)
        # item quantity
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 20 + i] = (itemQty & (0xFF << i * 8)) >> (i * 8)
        slot+=1
    for medal in medals:
        checking = 0
        for i in range(0, valueSize):
            checking = checking | (saveFileBuffer[address + (slot*24) + 8 + i] << i * 8)
        if checking == KEY_TEM:
            slot+=1
        # the beginning of any item; the unknown parts, usual value is as above unknownId
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + i] = (unknownId & (0xFF << i * 8)) >> (i * 8)
        # item type
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 8 + i] = (MEDAL_ITEM & (0xFF << i * 8)) >> (i * 8)
        # item id
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 12 + i] = (medal & (0xFF << i * 8)) >> (i * 8)
        # unknown, supposedly to be same as item id
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 16 + i] = (medal & (0xFF << i * 8)) >> (i * 8)
        # item quantity
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 20 + i] = (medalQty & (0xFF << i * 8)) >> (i * 8)
        slot+=1
    for accessory in accessories:
        checking = 0
        for i in range(0, valueSize):
            checking = checking | (saveFileBuffer[address + (slot*24) + 8 + i] << i * 8)
        if checking == KEY_TEM:
            slot+=1
        # the beginning of any item; the unknown parts, usual value is as above unknownId
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + i] = (unknownId & (0xFF << i * 8)) >> (i * 8)
        # item type
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 8 + i] = (ACCESSORY_ITEM & (0xFF << i * 8)) >> (i * 8)
        # item id
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 12 + i] = (accessory & (0xFF << i * 8)) >> (i * 8)
        # unknown, supposedly to be same as item id
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 16 + i] = (accessory & (0xFF << i * 8)) >> (i * 8)
        # item quantity
        for i in range(0, valueSize):
            saveFileBuffer[address + (slot*24) + 20 + i] = (itemQty & (0xFF << i * 8)) >> (i * 8)
        slot+=1
    
    if version == "cs":
        global obtain_all_items_cs
        obtain_all_items_cs = 1
    else:
        global obtain_all_items_hm
        obtain_all_items_hm = 1

def setDigiConvertAll(version = None):
    # sets all the digiconvert to 200%
    
    # digiconvert percentage starts at address 0xB012 or 0x6C7B2; first digimon/slot in digiconvert list
    if version == "cs":
        address = int("B012", 16)
    else:
        address = int("6C7B2", 16)
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
