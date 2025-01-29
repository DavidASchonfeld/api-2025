import os
from typing import Union

import pandas as pd
from pandas import DataFrame

import requests
import pprint
from enum import Enum


# from xml.etree import ElementTree
# from defusedxml.ElementTree
# from defusedxml.ElementTree import parse
# from defusedxml.ElementTree import iterparse
# Python safeguard library for parsing XML
from lxml import etree
import lxml

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
        if (responseContentFormat == xmlOrJson.XML):
            
            root : etree._Element = etree.XML(response.content, etree.XMLParser())
            print(type(root))
            print(etree.tostring(root))
        elif (responseContentFormat == xmlOrJson.JSON):
            print("TODO: JSON stuff")
            pass




        # return response._content
    


# "http://www.itis.gov/ITISWebService/services/ITISService/searchForAnyMatchPaged?srchKey=dolphin&pageSize=2&pageNum=1&ascend=false"
testRequest_request : str = "searchForAnyMatchPaged?srchKey=dolphin&pageSize=2&pageNum=1&ascend=false"
sendRequest_toITIS(testRequest_request, xmlOrJson.XML)


# print("urlToSend: "+urlToSend)
# responseOne_original_json : requests.Response = requests.get(urlToSend)

# For getting all results, too long for defusedxml to process
# "http://www.itis.gov/ITISWebService/services/ITISService/searchForAnyMatch?srchKey=dolphin

# For getting 1 page of results
# http://www.itis.gov/ITISWebService/services/ITISService/searchForAnyMatchPaged?srchKey=Zy&pageSize=100&pageNum=1&ascend=false


# responseOne_original_json_content : bytes = responseOne_original_json.content
# print(responseOne_original_json.status_code)
# print(responseOne_original_json_content)
# print('------------------')

# root = etree.fromstring()
# responseOne_parsed = ElementTree.parse(responseOne_original.content)
# events = ElementTree.iterparse(responseOne_contents)
# for event, elem in events:
#     pass
#     print('i')


# TODO:
# Process XML
# Process JSON

# pprint.pprint(responseOne_parsed)