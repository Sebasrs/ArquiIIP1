from Chip import Chip
from Memory import Memory

mainMemory = Memory()
bus = ""

chip0 = Chip(0, mainMemory)
chip1 = Chip(1, mainMemory)

chip0.start()
chip1.start()