import os
from typing import Any, Dict

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


def sendRequest_toITIS(endStringRequest : str, responseContentFormat : xmlOrJson) -> Dict[Any, Any]:
    requestToSend_full : str
    if (responseContentFormat == xmlOrJson.XML):
        requestToSend_full : str = os.path.join(itis_url_beginning, itis_receiveFormat.XML.value, endStringRequest)
    elif (responseContentFormat == xmlOrJson.JSON):
        requestToSend_full : str = os.path.join(itis_url_beginning, itis_receiveFormat.JSON.value, endStringRequest)
    else:
        raise TypeError("responseContentFormat should be \"XML\" or \"JSON\" but it is "+str(responseContentFormat))
    
    try:
        response : requests.Response = requests.get(requestToSend_full)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print("response.status_code: "+str(response.status_code))
        raise requests.exceptions.HTTPError("Response Status Code: "+str(response.status_code))
    except Exception as error:
        pass

    responseContent_dict : dict
    if (responseContentFormat == xmlOrJson.XML):

        root : etree._Element = etree.XML(response.content, etree.XMLParser())
        # print(etree.tostring(root))

        responseContent_dict : dict = xmltodict.parse(response.content)
    elif (responseContentFormat == xmlOrJson.JSON):
        responseContent_dict : dict = json.loads(response.content)

    return responseContent_dict



###### Test ######

# "http://www.itis.gov/ITISWebService/services/ITISService/searchForAnyMatchPaged?srchKey=dolphin&pageSize=2&pageNum=1&ascend=false"
testRequest_request : str = "searchForAnyMatchPaged?srchKey=dolphin&pageSize=2&pageNum=1&ascend=false"
dataReceived_request1_json : dict = sendRequest_toITIS(testRequest_request, xmlOrJson.JSON)
dataReceived_request1_xml : dict = sendRequest_toITIS(testRequest_request, xmlOrJson.XML)

if (dataReceived_request1_json == dataReceived_request1_xml):
    print("Results from JSON and XML are the same")
    # They are the same!
else:
    print("Results from JSON and XML are the same")
##################