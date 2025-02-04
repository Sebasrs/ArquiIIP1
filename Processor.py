from L1 import L1
import threading
import numpy as np
import time
import logging

logging.basicConfig(filename='log.log',level=logging.INFO)

availableInstructions = ["READ", "CALC", "WRITE"]

class Processor(threading.Thread):
  def __init__(self, number, chip):
    threading.Thread.__init__(self)
    self.chip = chip
    self.number = number
    self.L1 = L1(number, chip)

  def run(self):
    while(1):
      fullInstructionNoSplit = generateInstruction(self)
      logging.info('Procesador ' + str(self.number) + " del Chip " + str(self.chip.chip) + ": " + "Nueva instruccion generada: " + fullInstructionNoSplit)
      fullInstruction = fullInstructionNoSplit.split(' ')
      self.chip.UIManager.updateInstruction(self.chip.chip, self.number, fullInstructionNoSplit)
      kind = fullInstruction[1]
      if(kind == "WRITE"):
        logging.info('Procesador ' + str(self.number) + " del Chip " + str(self.chip.chip) + ": " + "Procesando instruccion WRITE")
        memAndData = fullInstruction[2].split(";")
        self.processWrite(memAndData[0], memAndData[1])
        logging.info('Procesador ' + str(self.number) + " del Chip " + str(self.chip.chip) + ": " + "Fin de intruccion WRITE")
      if(kind == "READ"):
        logging.info('Procesador ' + str(self.number) + " del Chip " + str(self.chip.chip) + ": " + "Procesando instruccion READ")
        self.processRead(fullInstruction[2])
        logging.info('Procesador ' + str(self.number) + " del Chip " + str(self.chip.chip) + ": " + "Fin de intruccion READ")
      if(kind == "CALC"):
        logging.info('Procesador ' + str(self.number) + " del Chip " + str(self.chip.chip) + ": " + "Procesando instruccion CALC")
        self.processCalc()
        logging.info('Procesador ' + str(self.number) + " del Chip " + str(self.chip.chip) + ": " + "Fin de intruccion CALC")
  
  def processWrite(self, memDir, data):
    logging.info('Procesador ' + str(self.number) + " del Chip " + str(self.chip.chip) + ": " + "Escribiendo el dato " + data + " en la direccion de memoria " + memDir)
    self.L1.write(memDir, data)
    self.chip.L2.write(memDir, data, self.number)
    self.chip.mainMemory.write(memDir, data, self.chip.chip)
    self.chip.connectionBus.append(["writeMiss", str(self.chip.chip), memDir])
    time.sleep(15)
  
  def processRead(self, memDir):
    logging.info('Procesador ' + str(self.number) + " del Chip " + str(self.chip.chip) + ": " + "Buscando direccion: " + memDir)
    L1Index = self.L1.onMemory(memDir)
    logging.info('Procesador ' + str(self.number) + " del Chip " + str(self.chip.chip) + ": " + "Buscando en L1: " + memDir)
    if(L1Index != -1):
      logging.info('Procesador ' + str(self.number) + " del Chip " + str(self.chip.chip) + ": " + "Cache hit en L1")
      self.L1.dataHitUpdate(L1Index)
      time.sleep(1)
    else:
      logging.warn('Procesador ' + str(self.number) + " del Chip " + str(self.chip.chip) + ": " + "Cache miss en L1")
      logging.info('Procesador ' + str(self.number) + " del Chip " + str(self.chip.chip) + ": " + "Buscando en L2: " + memDir)
      L2Index = self.chip.L2.onMemory(memDir)
      if(L2Index != -1):
        logging.info('Procesador ' + str(self.number) + " del Chip " + str(self.chip.chip) + ": " + "Cache hit en L2")
        self.chip.L2.dataHitUpdate(L2Index, "C" + str(self.chip.chip) + "P" + str(self.number))
        data = self.chip.L2.memory[L2Index]._data
        self.L1.writeRead(memDir, data)
        time.sleep(3)
      else:
        logging.warn("Chip " + str(self.chip.chip) + ": " + "Cache miss en L2")
        logging.info("Chip " + str(self.chip.chip) + ": " + "Buscando en memoria principal")
        data = self.chip.mainMemory.memory[int(memDir, 2)]._data
        logging.info("Chip " + str(self.chip.chip) + ": " + "Dato en memoria principal, direccion: " + memDir + ", dato: " + data)
        self.chip.mainMemory.addOwner("C" + str(self.chip.chip), int(memDir, 2))
        self.L1.writeRead(memDir, data)
        self.chip.L2.writeRead(memDir, data, self.number)
        self.chip.mainMemory.setState(self.chip.L2.memory[self.chip.L2.onMemory(memDir)]._state, int(memDir, 2))
        time.sleep(9)
    logging.info("Chip " + str(self.chip.chip) + ": Escribiendo readMiss en el bus de interconexion hacia el otro chip")
    self.chip.connectionBus.append(["readMiss", str(self.chip.chip), memDir])
  
  def processCalc(self):
    time.sleep(10)
      
def generateInstruction(self):
  instructionIndex = np.clip(np.random.poisson(1,1), a_min=0, a_max=2)[0]

  pickedInstruction = availableInstructions[instructionIndex]

  if(pickedInstruction == "READ"):
    memDir = np.clip(np.random.poisson(7,1), a_min=0, a_max=15)[0]
    return("P" + str(self.number) + "," + str(self.chip.chip) + ": " + str(pickedInstruction) + " " + "{:04b}".format(memDir))
  elif(pickedInstruction == "CALC"):
    return("P" + str(self.number) + "," + str(self.chip.chip) + ": " + str(pickedInstruction))
  elif(pickedInstruction == "WRITE"):
    memDir = np.clip(np.random.poisson(7,1), a_min=0, a_max=15)[0]
    data = hex(int(generateRandomBits(32), 2))
    return("P" + str(self.number) + "," + str(self.chip.chip) + ": " + str(pickedInstruction) + " " + "{:04b}".format(memDir) + ";" + data[2:].upper())

def generateRandomBits(bitAmount):
  binaryNumber = ""
  for i in range(bitAmount):
    binaryNumber += str(np.clip(np.random.poisson(1,1), a_min=0, a_max=1)[0])
  return binaryNumber