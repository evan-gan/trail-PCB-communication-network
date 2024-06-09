class HistoryManager:
    history:list[str] = []
    MSG_Draft:str = "Me: How long will that take?"
    scroll = 0

    def addMSG(self, MSG):
        self.history.append(MSG)

    def getHistory(self):
        return self.history

    def getMSG_Draft(self):
        return self.MSG_Draft
    
    def setMSG_Draft(self, newDraft):
        self.MSG_Draft = newDraft
    #TODO: Implement store/restore from flash mem