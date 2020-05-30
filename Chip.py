from Processor import Processor
from L2 import L2
import threading

class Chip(threading.Thread):
  def __init__(self, number):
    threading.Thread.__init__(self)
    self.chip = number
    self.L2 = L2(number)
    self.procesors = []
    for i in range(2):
      self.procesors.append(Processor(i, number))
      self.procesors[i].start()
  
  def run(self):
    print("Chip " + str(self.chip) + " online")