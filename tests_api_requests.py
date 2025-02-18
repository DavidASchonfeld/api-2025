from api_requests import sendRequest_toITIS
from api_requests import sendRequest_toSmithsonian

from api_requests import xmlOrJson

from pprint import pprint

from outputTextWriter import OutputTextWriter






writer : OutputTextWriter = OutputTextWriter()

###### Test Smithsonian ######

## NMNH = National Museum of National History

# URL Reference: https://edan.si.edu/openaccess/apidocs/
testRequest_endStringRequest : str = "search"
testRequest_params : dict = {
    "q" : "gorilla"
}
dataReceived_request1_json : dict = sendRequest_toSmithsonian(testRequest_endStringRequest, testRequest_params)

writer.print("Test1")
writer.print("Test2")

writer.print_dict(dataReceived_request1_json, prettyPrint= True)

writer.print("Test1")
writer.print("Test2")


# writer.print_dict(dataReceived_request1_json, True)


###### Test ITIS ######

# "http://www.itis.gov/ITISWebService/services/ITISService/searchForAnyMatchPaged?srchKey=dolphin&pageSize=2&pageNum=1&ascend=false"
# testRequest_request : str = "searchForAnyMatchPaged?srchKey=dolphin&pageSize=2&pageNum=1&ascend=false"
# dataReceived_request1_json : dict = sendRequest_toITIS(testRequest_request, xmlOrJson.JSON)
# dataReceived_request1_xml : dict = sendRequest_toITIS(testRequest_request, xmlOrJson.XML)

# if (dataReceived_request1_json == dataReceived_request1_xml):
#     print("Results from JSON and XML are the same")
#     # They are the same!
# else:
#     print("Results from JSON and XML are the same")
# print(dataReceived_request1_json)
# ##################