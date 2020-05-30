from Chip import Chip
from Memory import Memory

mainMemory = Memory()

chip0 = Chip(0)
chip1 = Chip(1)

chip0.start()
chip1.start()