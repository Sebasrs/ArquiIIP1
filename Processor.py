from L1 import L1
import threading
import numpy as np
import time

availableInstructions = ["READ", "CALC", "WRITE"]

class Processor(threading.Thread):
  def __init__(self, number, chip):
    threading.Thread.__init__(self)
    self.chip = chip
    self.number = number
    self.L1 = L1(number, chip)

  def run(self):
    print("Procesor " + str(self.number) + " from chip " + str(self.chip) + " online")
    while(1):
      instruction = generateInstruction(self)
      time.sleep(2)

def generateInstruction(self):
  instructionIndex = np.clip(np.random.poisson(1,1), a_min=0, a_max=2)[0]

  pickedInstruction = availableInstructions[instructionIndex]

  if(pickedInstruction == "READ"):
    memDir = np.clip(np.random.poisson(7,1), a_min=0, a_max=15)[0]
    return("P" + str(self.number) + "," + str(self.chip) + ": " + str(pickedInstruction) + " " + "{:04b}".format(memDir))
  elif(pickedInstruction == "CALC"):
    return("P" + str(self.number) + "," + str(self.chip) + ": " + str(pickedInstruction))
  elif(pickedInstruction == "WRITE"):
    memDir = np.clip(np.random.poisson(7,1), a_min=0, a_max=15)[0]
    data = hex(int(generateRandomBits(16), 2))
    return("P" + str(self.number) + "," + str(self.chip) + ": " + str(pickedInstruction) + " " + "{:04b}".format(memDir) + ";" + data[2:].upper())

def generateRandomBits(bitAmount):
  binaryNumber = ""
  for i in range(bitAmount):
    binaryNumber += str(np.clip(np.random.poisson(1,1), a_min=0, a_max=1)[0])
  return binaryNumber