import os
from datetime import datetime
from pprint import pprint
from pprint import pformat

from constants import outputTextsFolder_folderPath



class OutputTextWriter:

    outputTextFileName : str

    def __init__(self):
        try:
            if (os.access(outputTextsFolder_folderPath, os.W_OK) == False):
                raise PermissionError
        except PermissionError as e:
            raise PermissionError("outputTextWriter.py does not have permisison to create/write a text file in the target folder.")
        self.outputTextFileName : str = os.path.join(outputTextsFolder_folderPath, str(datetime.now())+".txt")

    def print(self, inString: str) -> str:
        print(inString)
        print(self.outputTextFileName)
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