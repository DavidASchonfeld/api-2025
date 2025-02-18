import os
from datetime import datetime

outputFolder : str = "TextOutputs"

class outputTextWriter:

    outputTextFileName : str

    def __init__(self):
       self.outputTextFileName = os.path.join(outputFolder, str(datetime))
    
    def print_textAndTerminal(inString: str):









outputTextFileName = os.path.join(outputFolder, str(datetime))
with open(outputTextFileName, "w"):
    file.write()