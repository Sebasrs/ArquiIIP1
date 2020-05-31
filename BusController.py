import threading

class BusController(threading.Thread):
  def __init__(self, otherChipMessage):
    threading.Thread.__init__(self)
    self.busMessage = busMessage
    self.otherChipMessage = otherChipMessage

  def run(self):
    while(1):
      if(self.busMessage != ""):
        print(self.busMessage)
        self.busMessage = ""
      if(self.otherChipMessage != ""):
        print(self.otherChipMessage)
        self.otherChipMessage = ""
