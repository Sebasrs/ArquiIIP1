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

  def write(self, cacheBlock, memDir, data):
    self.memory[cacheBlock - 1]._memDir = memDir
    self.memory[cacheBlock - 1]._data = data