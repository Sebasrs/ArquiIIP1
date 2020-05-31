class cacheBlockDir:
  def __init__(self):
    self._state = "DI"
    self._memDir = "0"
    self._data = "0"
    self._owners = []

class L2:
  def __init__(self, chip):
    self.chip = chip
    self.memory = []
    for i in range(4):
      self.memory.append(cacheBlockDir)

  def write(self, cacheBlock, memDir, data):
    self.memory[cacheBlock - 1]._memDir = memDir
    self.memory[cacheBlock - 1]._data = data