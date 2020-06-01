from Processor import Processor
from L2 import L2
import threading
import time

class Chip(threading.Thread):
  def __init__(self, number, mainMemory, UIManager, connectionBus):
    threading.Thread.__init__(self)
    self.chip = number
    self.mainMemory = mainMemory
    self.procesors = []
    self.UIManager = UIManager
    for i in range(2):
      self.procesors.append(Processor(i, self))
      self.procesors[i].start()
    self.L2 = L2(self)
    self.connectionBus = connectionBus
  
  def run(self):
    # message, chip, memDir
    while(1):
      if(len(self.connectionBus) != 0):
        if(self.connectionBus[0][1] != str(self.chip)):
          print("Message: " + self.connectionBus[0][0] + " from chip: " + self.connectionBus[0][1] + " on direction " + self.connectionBus[0][2] + " printed from chip: " + str(self.chip))
          for i in range(len(self.procesors)):
            self.procesors[i].L1.checkState(self.connectionBus[0][0], self.connectionBus[0][2])
          self.L2.checkState(self.connectionBus[0][0], self.connectionBus[0][2])
          self.connectionBus.pop(0)
      time.sleep(0.2)

  # operacion,procesador,direccionDeMemoria
  def busMsg(self, message):
    message = message.split(",")
    if(message[1] == "0"):
      self.procesors[1].L1.checkState(message[0], message[2])
    elif(message[1] == "1"):
      self.procesors[0].L1.checkState(message[0], message[2])
