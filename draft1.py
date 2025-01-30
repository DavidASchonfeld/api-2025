import os
from typing import Union

import pandas as pd
from pandas import DataFrame

import requests
import pprint
from enum import Enum

from lxml import etree
import json
import xmltodict

# ITIS stands for "Integrated Taxonomic Information System"

import constants

itis_url_beginning : str = "http://www.itis.gov/ITISWebService/"
class itis_receiveFormat(Enum):
    XML = "services/ITISService"
    JSON = "jsonservice"

class xmlOrJson(Enum):
    XML = 0
    JSON = 1


def sendRequest_toITIS(endStringRequest : str, responseContentFormat : xmlOrJson) -> Union[bytes, None]:
    requestToSend_full : str
    if (responseContentFormat == xmlOrJson.XML):
        requestToSend_full : str = os.path.join(itis_url_beginning, itis_receiveFormat.XML.value, endStringRequest)
    elif (responseContentFormat == xmlOrJson.JSON):
        requestToSend_full : str = os.path.join(itis_url_beginning, itis_receiveFormat.JSON.value, endStringRequest)
    else:
        raise TypeError("responseContentFormat should be \"XML\" or \"JSON\" but it is "+str(responseContentFormat))
    
    response : requests.Response = requests.get(requestToSend_full)
    if (response.status_code >= 400):
        print("response.status_code: "+str(response.status_code))
        return
    elif (response.status_code == 200):
        ## All good

        #TODO: Finish this method
        print("response.content:")
        print(str(response.content))
        print("---------")
        if (responseContentFormat == xmlOrJson.XML):

            root : etree._Element = etree.XML(response.content, etree.XMLParser())
            print(type(root))
            print(etree.tostring(root))

            testDict : dict = xmltodict.parse(response.content)
            print(testDict)
        elif (responseContentFormat == xmlOrJson.JSON):
            print("TODO: JSON stuff")
            jsonObject : dict = json.loads(response.content)
            print(jsonObject)

    else:
        raise NotImplementedError("Code that responds to Response Codes that are <400 and NOT 200 are not implemented yet.")


        # return response._content
    

# "http://www.itis.gov/ITISWebService/services/ITISService/searchForAnyMatchPaged?srchKey=dolphin&pageSize=2&pageNum=1&ascend=false"
testRequest_request : str = "searchForAnyMatchPaged?srchKey=dolphin&pageSize=2&pageNum=1&ascend=false"
sendRequest_toITIS(testRequest_request, xmlOrJson.JSON)
