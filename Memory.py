class memoryBlock:
  def __init__(self, memDir):
    self._memDir = memDir
    self._data = "00000000"
    self._state = "DI"
    self._owners = []

class Memory:
  def __init__(self, UIManager):
    self.memory = []
    for i in range(16):
      self.memory.append(memoryBlock("{:04b}".format(i)))
    self.UIManager = UIManager
    self.UIManager.updateTableMainMemory(self.memory)

  def write(self, memDir, data, chipNumber):
    self.memory[int(memDir,2)]._data = data
    self.memory[int(memDir,2)]._state = "DM"
    self.memory[int(memDir,2)]._owners = ["C" + str(chipNumber)]
    self.UIManager.updateTableMainMemory(self.memory)

  def read(self, memDir):
    return self.memory[memDir]._data

  def addOwner(self, owner, memDir):
    if(owner not in self.memory[memDir]._owners):
      self.memory[memDir]._owners.append(owner)
      self.UIManager.updateTableMainMemory(self.memory)

  def setState(self, state, memDir):
    self.memory[memDir]._state = state
    self.UIManager.updateTableMainMemory(self.memory)