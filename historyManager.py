class HistoryManager:
    history = []
    # MSG_Draft: str = "Me: How long will that take?"
    scroll = 0

    def __init__(self, userID, displayName):
        self.displayName = displayName
        self.userID = userID

    def addSentMSG(self, MSG):
        self.addMSG(MSG, self.userID, self.displayName)
        
    def addMSG(self, MSG, userID, displayName):
        self.history.append({
            "userID": userID,
            "message": MSG,
            "displayName": displayName
        })

    # def getHistory(self):
    #     return self.history

    # def getMSG_Draft(self):
    #     return self.MSG_Draft

    # def setMSG_Draft(self, newDraft):
    #     self.MSG_Draft = newDraft

    def getHistoryAsJSON(self):
        return self.history
    # TODO: Implement store/restore from flash mem
