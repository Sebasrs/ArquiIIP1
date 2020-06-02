class cacheBlockDir:
  def __init__(self):
    self._state = "DI"
    self._memDir = "0000"
    self._data = "00000000"
    self._owners = []

class L2:
  def __init__(self, chip):
    self.chip = chip
    self.memory = []
    for i in range(4):
      self.memory.append(cacheBlockDir())
    self.chip.UIManager.updateTableL2(self.chip.chip, self.memory)

  def write(self, memDir, data, who):
    ## Correspondencia directa
    cacheBlock = int(memDir, 2)%len(self.memory)

    self.memory[cacheBlock]._memDir = memDir
    self.memory[cacheBlock]._data = data
    self.memory[cacheBlock]._state = self.nextStateCPU("write", memDir)
    self.memory[cacheBlock]._owners = ["C" + str(self.chip.chip) + "P" + str(who)]

    self.chip.UIManager.updateTableL2(self.chip.chip, self.memory)
  
  def writeRead(self, memDir, data, who):
    ## Correspondencia directa
    cacheBlock = int(memDir, 2)%len(self.memory)

    self.memory[cacheBlock]._memDir = memDir
    self.memory[cacheBlock]._data = data
    self.memory[cacheBlock]._state = self.nextStateCPU("read", memDir)
    self.memory[cacheBlock]._owners = ["C" + str(self.chip.chip) + "P" + str(who)]

    self.chip.UIManager.updateTableL2(self.chip.chip, self.memory)

  def dataHitUpdate(self, index, owner):
    self.memory[index]._owners.append(owner)
    self.memory[index]._state = self.nextStateCPU("read", self.memory[index]._memDir)

    self.chip.UIManager.updateTableL2(self.chip.chip, self.memory)

  def nextStateCPU(self, operation, memDir):
    cacheBlock = self.onMemory(memDir)
    nextState = "DI"

    if(cacheBlock != -1):
      storedInCache = self.memory[cacheBlock]
      if(operation == "write"):
        nextState = "DM"
      elif(operation == "read"):
        if(storedInCache._state == "DI"):
          nextState = "DS"
        if(storedInCache._state == "DM"):
          nextState = "DM"
        if(storedInCache._state == "DS"):
          nextState = "DS"
    else:
      if(operation == "write"):
        nextState = "DM"
      elif(operation == "read"):
        nextState = "DS"
    
    return nextState

  def nextStateBus(self, busMsg, cacheBlock):
    nextState = "DI"
    if(self.memory[cacheBlock]._state == "DM"):
      if(busMsg == "writeMiss"):
        nextState = "DI"
      elif(busMsg == "readMiss"):
        nextState = "DS"
    if(self.memory[cacheBlock]._state == "DS"):
      if(busMsg == "writeMiss"):
        nextState = "DI"
      elif(busMsg == "readMiss"):
        nextState = "DS"
      elif(busMsg == "invalidate"):
        nextState = "DI"
    return(nextState)
  
  def onMemory(self, memDir):
    for i in range(len(self.memory)):
      storedInCache = self.memory[i]
      if(storedInCache._memDir == memDir and (storedInCache._state == "DS" or storedInCache._state == "DM")):
        return(i)
    return(-1)

  def checkState(self, busMessage, memDir):
    cacheBlock = self.onMemory(memDir)
    if(cacheBlock != -1):
      self.memory[cacheBlock]._state = self.nextStateBus(busMessage, cacheBlock)
      if(busMessage == "writeMiss"):
        self.memory[cacheBlock]._owners = []
      else:
        if("E" not in self.memory[cacheBlock]._owners):
          self.memory[cacheBlock]._owners.append("E")
        self.chip.connectionBus.append(["readMiss", str(self.chip.chip), memDir])
      self.chip.UIManager.updateTableL2(self.chip.chip, self.memory)