import os
from datetime import datetime
from pprint import pprint
from pprint import pformat

from constants import outputTextsFolderName



class OutputTextWriter:

    outputTextFileName : str

    def __init__(self):
       self.outputTextFileName = os.path.join(outputTextsFolderName, str(datetime))
    
    def print(self, inString: str) -> str:
        print(inString)
        with open(self.outputTextFileName, "w") as textFile:
            textFile.write(inString)
        return inString

    def print_dict(self, inDict: dict, prettyPrint : bool = False) -> str:
        
        ## Pretty Print
        if (prettyPrint):

            ## Terminal
            pprint(inDict)

            ## Print to Text File
            with open(self.outputTextFileName, "w") as textFile:
                pprint(inDict, stream=textFile)

            return pformat(inDict, indent = 4)
    
        ## Regular String Printing (aka non-Pretty Print)
        else: ## Not Pretty Print
            return self.print(str(inDict))