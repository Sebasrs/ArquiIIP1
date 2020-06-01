from Chip import Chip
from Memory import Memory
from FrontEndManager import FrontEndManager
import tkinter as tk

#UI
root = tk.Tk()
root.title("Arquitectura de computadores II")
root.state('zoomed')

PInstructionsVars = []

for i in [0, 2]:
  textVariable = tk.StringVar()
  PInstructionsVars.append(textVariable)
  label = tk.Label(root, textvariable=textVariable, bg='#b0d2d4', fg='black', borderwidth=1, relief="solid")
  label.config(font=('Arial', 14))
  label.grid(column=i, row = 0, sticky = 'news')

for i in [0, 2]:
  textVariable = tk.StringVar()
  PInstructionsVars.append(textVariable)
  label = tk.Label(root, textvariable=textVariable, bg='#b0d2d4', fg='black', borderwidth=1, relief="solid")
  label.config(font=('Arial', 14))
  label.grid(column=i, row = 1, sticky = 'news')

## Generate tables
tablesNames = ["L1-P0-C0", "L1-P1-C0", "L2-C0", "L1-P0-C1", "L1-P1-C1", "L2-C1", "Memoria Principal"]
tableHeadingsL1 = ["Bloque de cache", "Dirección de memoria", "Estado", "Dato"]
tableHeadingsL2 = ["Bloque de cache", "Dirección de memoria", "Estado", "Dueños", "Dato"]
tableHeadingsMain = ["Dirección de memoria", "Estado", "Dueños", "Dato"]
columnPos = [0, 2, 1, 0, 2, 1, 1]
rowPos = [0, 0, 1, 2, 2, 3, 4]
tableSize = [4,4,6,4,4,6,18]

stringvarsChips = []
thisVars = []

for i in range(len(tablesNames)):
  cacheL1P0C0 = tk.Frame(root)
  cacheL1P0C0.grid(column=columnPos[i], row=rowPos[i] + 2, sticky = 'news')
  
  root.rowconfigure(rowPos[i], weight=1)
  root.columnconfigure(columnPos[i], weight=1)

  label = tk.Label(cacheL1P0C0, text=tablesNames[i], bg='#c6e697', fg='black', borderwidth=1, relief="solid")
  label.config(font=('Arial', 14))
  label.grid(row=0, column=0, sticky = 'news', columnspan=len(tablesNames[i]))
  cacheL1P0C0.columnconfigure(0, weight=1)

  for row in range(1,tableSize[i]):
    if(tableSize[i] == 4):
      tableHeadings = tableHeadingsL1
    elif(tableSize[i] == 6):
      tableHeadings = tableHeadingsL2
    elif(tableSize[i] == 18):
      tableHeadings = tableHeadingsMain
    for column in range(len(tableHeadings)):
      if(row == 1):
        label = tk.Label(cacheL1P0C0, text=tableHeadings[column], bg='white', fg='black', borderwidth=1, relief="solid")
        label.config(font=('Arial', 14))
      else:
        dirVar = tk.StringVar()
        thisVars.append(dirVar)
        label = tk.Label(cacheL1P0C0, textvariable=dirVar, relief="solid", borderwidth=1)
        label.config(font=('Arial', 12))
      label.grid(row=row, column=column, sticky = 'news')
      cacheL1P0C0.columnconfigure(column, weight=1)
  
  stringvarsChips.append(thisVars)

UIManager = FrontEndManager(stringvarsChips[0], stringvarsChips[1], stringvarsChips[2], stringvarsChips[3], stringvarsChips[4], stringvarsChips[5], stringvarsChips[6], PInstructionsVars[0], PInstructionsVars[1], PInstructionsVars[2], PInstructionsVars[3])

mainMemory = Memory(UIManager)

connectionBus = []

chip0 = Chip(0, mainMemory, UIManager, connectionBus)
chip1 = Chip(1, mainMemory, UIManager, connectionBus)

chip0.start()
chip1.start()

root.mainloop()