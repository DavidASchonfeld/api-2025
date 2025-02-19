#External Libraries
from pprint import pprint
import pandas as pd
from pandas import DataFrame

# My Created Libraries
from api_requests import xmlOrJson
from outputTextWriter import OutputTextWriter

writer : OutputTextWriter = OutputTextWriter()

###### Test Smithsonian ######

## NMNH = National Museum of National History

# URL Reference: https://edan.si.edu/openaccess/apidocs/
testRequest_endStringRequest : str = "search"
testRequest_params : dict = {
    "q" : "gorilla"
}
from api_requests import Smithsonian_requests
dataReceived_request1_json : dict = Smithsonian_requests.sendRequest(testRequest_endStringRequest, testRequest_params)


writer.print("Test1")
writer.print("Test2")

writer.print_dict(dataReceived_request1_json, prettyPrint= True)

writer.print("Test1")
writer.print("Test2")
writer.print("\n--------------------------\n")

smithsonian_gorilla : DataFrame = DataFrame(dataReceived_request1_json)



##### Test ITIS ######

# "http://www.itis.gov/ITISWebService/services/ITISService/searchForAnyMatchPaged?srchKey=dolphin&pageSize=2&pageNum=1&ascend=false"
# testRequest_request : str = "searchForAnyMatchPaged?srchKey=dolphin&pageSize=2&pageNum=1&ascend=false"
testRequest_request : str = "searchForAnyMatchPaged?srchKey=gorilla&pageSize=2&pageNum=1&ascend=false"

from api_requests import ITIS_requests
dataReceived_request1_json : dict = ITIS_requests.sendRequest(testRequest_request, xmlOrJson.JSON)
dataReceived_request1_xml : dict = ITIS_requests.sendRequest(testRequest_request, xmlOrJson.XML)

if (dataReceived_request1_json == dataReceived_request1_xml):
    print("Results from JSON and XML are the same")
    # They are the same!
else:
    print("Results from JSON and XML are the same")

writer.print_dict(dataReceived_request1_json, prettyPrint= True)
writer.print("test3")

itis_gorilla : DataFrame = DataFrame(dataReceived_request1_json)

##################

mergeOne : DataFrame = pd.merge(smithsonian_gorilla, itis_gorilla, left_on = 'title_sort', right_on = 'name')

writer.print("\n--------------------\n")

print(mergeOne)

