class memoryBlock:
  def __init__(self):
    self._data = "0"

class Memory:
  def __init__(self):
    self.memory = []
    for i in range(16):
      self.memory.append(memoryBlock)

  def write(self, memDir, data):
    self.memory[memDir]._data = data

  def read(self, memDir):
    return self.memory[memDir]._data