class cacheBlock:
  def __init__(self):
    self._state = "I"
    self._memDir = "0000"
    self._data = "00000000"

class L1:
  def __init__(self, processor, chip):
    self.processor = processor
    self.chip = chip
    self.memory = []
    for i in range(2):
      self.memory.append(cacheBlock())

  def write(self, memDir, data):
    ## Correspondencia directa
    cacheBlock = int(memDir, 2)%len(self.memory)

    self.memory[cacheBlock]._memDir = memDir
    self.memory[cacheBlock]._data = data
    self.memory[cacheBlock]._state = self.nextStateCPU("write", memDir)

    self.printMemory()

  def nextStateCPU(self, operation, memDir):
    cacheBlock = self.onMemory(memDir)
    nextState = "I"

    if(cacheBlock != -1):
      storedInCache = self.memory[cacheBlock]
      if(operation == "write"):
        nextState = "M"
      elif(operation == "read"):
        if(storedInCache._state == "I"):
          nextState = "S"
        if(storedInCache._state == "M"):
          nextState = "M"
        if(storedInCache._state == "S"):
          nextState = "S"
    else:
      if(operation == "write"):
        nextState = "M"
      elif(operation == "read"):
        nextState = "S"
    
    return nextState

  def printMemory(self):
    for i in range(len(self.memory)):
      print(str(i) + "  " + str(self.memory[i]._memDir) + "  " + self.memory[i]._state + "  " + self.memory[i]._data)

  def nextStateBus(self, busMsg, cacheBlock):
    nextState = "I"
    if(self.memory[cacheBlock]._state == "M"):
      if(busMsg == "writeMiss"):
        nextState = "I"
      elif(busMsg == "readMiss"):
        nextState = "S"
    if(self.memory[cacheBlock]._state == "S"):
      if(busMsg == "writeMiss"):
        nextState = "I"
      elif(busMsg == "readMiss"):
        nextState = "S"
      elif(busMsg == "invalidate"):
        nextState = "I"
    return(nextState)

  def onMemory(self, memDir):
    for i in range(2):
      storedInCache = self.memory[i]
      if(storedInCache._memDir == memDir and (storedInCache._state == "S" or storedInCache._state == "M")):
        return(i)
    return(-1)