class FrontEndManager:
  def __init__(self, P0L1C0, P1L1C0, L2C0, P0L1C1, P1L1C1, L2C1, mainMemory, P0C0Ins, P1C0Ins, P0C1Ins, P1C1Ins):
    self.P0L1C0 = P0L1C0
    self.P1L1C0 = P1L1C0
    self.L2C0 = L2C0
    self.P0L1C1 = P0L1C1
    self.P1L1C1 = P1L1C1
    self.L2C1 = L2C1
    self.mainMemory = mainMemory
    self.P0C0Ins = P0C0Ins
    self.P1C0Ins = P1C0Ins
    self.P0C1Ins = P0C1Ins
    self.P1C1Ins = P1C1Ins

  def updateInstruction(self, chip, processor, instruction):
    if(chip == 0):
      if(processor == 0):
        self.P0C0Ins.set(instruction)
      if(processor == 1):
        self.P1C0Ins.set(instruction)
    if(chip == 1):
      if(processor == 0):
        self.P0C1Ins.set(instruction)
      if(processor == 1):
        self.P1C1Ins.set(instruction)

  def updateTableL1(self, processor, chip, memory):
    startingIndex = 0
    memoryToUse = ""
    if(processor == 0):
      if(chip == 0):
        memoryToUse = self.P0L1C0
      elif(chip == 1):
        startingIndex = 36
        memoryToUse = self.P0L1C1
    elif(processor == 1):
      if(chip == 0):
        startingIndex = 8
        memoryToUse = self.P1L1C0
      elif(chip == 1):
        startingIndex = 44
        memoryToUse = self.P1L1C1
    iterations = 0
    for i in range(len(memory)):
      memoryToUse[startingIndex + iterations*4].set(str(i))
      memoryToUse[startingIndex + iterations*4 + 1].set(memory[i]._memDir)
      memoryToUse[startingIndex + iterations*4 + 2].set(memory[i]._state)
      memoryToUse[startingIndex + iterations*4 + 3].set(memory[i]._data)
      iterations += 1
  
  def updateTableL2(self, chip, memory):
    startingIndex = 0
    memoryToUse = ""
    if(chip == 0):
      startingIndex = 16
      memoryToUse = self.L2C0
    elif(chip == 1):
      startingIndex = 52
      memoryToUse = self.L2C1
    iterations = 0
    for i in range(len(memory)):
      memoryToUse[startingIndex + iterations*5].set(str(i))
      memoryToUse[startingIndex + iterations*5 + 1].set(memory[i]._memDir)
      memoryToUse[startingIndex + iterations*5 + 2].set(memory[i]._state)
      memoryToUse[startingIndex + iterations*5 + 3].set(memory[i]._owners)
      memoryToUse[startingIndex + iterations*5 + 4].set(memory[i]._data)
      iterations += 1
  
  def updateTableMainMemory(self, memory):
    startingIndex = 72
    memoryToUse = self.mainMemory
    iterations = 0
    for i in range(len(memory)):
      memoryToUse[startingIndex + iterations*4].set(memory[i]._memDir)
      memoryToUse[startingIndex + iterations*4 + 1].set(memory[i]._state)
      memoryToUse[startingIndex + iterations*4 + 2].set(memory[i]._owners)
      memoryToUse[startingIndex + iterations*4 + 3].set(memory[i]._data)
      iterations += 1