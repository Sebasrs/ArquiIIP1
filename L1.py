class cacheBlock:
  def __init__(self):
    self._state = "I"
    self._memDir = "0"
    self._data = "0"

class L1:
  def __init__(self, processor, chip):
    self.processor = processor
    self.chip = chip
    self.memory = []
    for i in range(2):
      self.memory.append(cacheBlock)

  def write(self, cacheBlock, memDir, data):
    self.memory[cacheBlock - 1]._memDir = memDir
    self.memory[cacheBlock - 1]._data = data