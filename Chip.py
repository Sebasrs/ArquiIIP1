from Processor import Processor
from L2 import L2
import threading

class Chip(threading.Thread):
  def __init__(self, number, mainMemory, UIManager):
    threading.Thread.__init__(self)
    self.chip = number
    self.mainMemory = mainMemory
    self.procesors = []
    self.UIManager = UIManager
    for i in range(2):
      self.procesors.append(Processor(i, self))
      self.procesors[i].start()
    self.L2 = L2(self)
  
  def run(self):
    print("Chip " + str(self.chip) + " online")
