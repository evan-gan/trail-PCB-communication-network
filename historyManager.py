class HistoryManager:
    history:list[str] = []
    MSG_Draft:str = ""
    scroll = 0
    
    def __init__(self) -> None:
        pass

    #For messages receved via lora
    def addMSG(self, MSG):
        self.history.append(MSG)

    def setMSG_Draft(self, newDraft):
        self.MSG_Draft = newDraft

    def appendToDraft(self, char):
        self.MSG_Draft += char

    def deleteLastCharFromDraft(self):
        self.MSG_Draft = self.MSG_Draft[:-1]

    def draftSent(self):
        self.addMSG(self.MSG_Draft)
        self.MSG_Draft = ""
    
    #DO NOT TOUCH, NEEDED IN DISPLAY
    def getHistory(self):
        return self.history
    def getMSG_Draft(self):
        return self.MSG_Draft



    
    #TODO: Implement store/restore from flash mem