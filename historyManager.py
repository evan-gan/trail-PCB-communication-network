import ujson

class HistoryManager:
    #No restore needed:
    scroll = 0
    dataStoreFileName = "history_data.json"
    #Varables
    displayName = ""
    history:list[str] = []
    MSG_Draft:str = ""

    def __init__(self) -> None:
        self.restoreHistory()

    #For messages receved via lora
    def addMSG(self, MSG):
        self.history.append(MSG)
        self.saveHistory()

    def setMSG_Draft(self, newDraft):
        self.MSG_Draft = newDraft
        self.saveHistory()

    def appendToDraft(self, char):
        self.MSG_Draft += char
        self.saveHistory()

    def deleteLastCharFromDraft(self):
        self.MSG_Draft = self.MSG_Draft[:-1]
        self.saveHistory()

    def draftSent(self):
        self.addMSG(self.MSG_Draft)
        self.MSG_Draft = ""
    
    def setDisplayName(self,name):
        self.displayName = name
        self.saveHistory()

    def clearHistory(self):
        self.history = []
        self.MSG_Draft = ""
        self.saveHistory()
    #DO NOT TOUCH, NEEDED IN DISPLAY
    def getHistory(self):
        return self.history
    def getMSG_Draft(self):
        return self.MSG_Draft


    def restoreHistory(self):
        historyStuff = self.read_array_from_flash(self.dataStoreFileName)
        self.displayName = historyStuff["displayName"] # type: ignore
        self.MSG_Draft = historyStuff["MSG_Draft"] # type: ignore
        self.history = historyStuff["history"] # type: ignore

    def saveHistory(self):
        self.write_array_to_flash(self.dataStoreFileName, {
            'displayName': self.displayName, #type: ignore
            'MSG_Draft': self.MSG_Draft, # type: ignore
            'history': self.history # type: ignore
        })

    # Function to write array to flash memory
    def write_array_to_flash(self, filename, array):
        try:
            # Serialize array to JSON string
            json_str = ujson.dumps(array)
            
            # Write JSON string to a file
            with open(filename, 'w') as file:
                file.write(json_str)
            print("Array written to flash memory successfully.")
        except Exception as e:
            print(f"Error writing to flash memory: {e}")

    # Function to read array from flash memory
    def read_array_from_flash(self, filename):
        try:
            # Read JSON string from the file
            with open(filename, 'r') as file:
                json_str = file.read()
            
            # Deserialize JSON string to array
            array = ujson.loads(json_str)
            print("Array read from flash memory successfully.")
            return array
        except Exception as e:
            print(f"Error reading from flash memory: {e}")
            return None

