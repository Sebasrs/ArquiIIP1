class memoryBlock:
  def __init__(self, memDir):
    self._memDir = memDir
    self._data = "0"
    self._state = "DI"
    self._owners = []

class Memory:
  def __init__(self, UIManager):
    self.memory = []
    for i in range(16):
      self.memory.append(memoryBlock("{:04b}".format(i)))
    UIManager.updateTableMainMemory(self.memory)

  def write(self, memDir, data):
    self.memory[memDir]._data = data

  def read(self, memDir):
    return self.memory[memDir]._data