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

from constants import api_keys

class xmlOrJson(Enum):
        XML = 0
        JSON = 1




class apiRequestsLibrary:
    requestLimitPerHour : int
    guideReferences : list[str]
    api_url_beginning : str


    def __init__(self):
        pass
    def sendRequest(self):
        pass

class ITIS_requests(apiRequestsLibrary):
    requestLimitPerHour = 0
    guideReferences = [
        "https://www.itis.gov/ws_searchApiDescription.html", 
        "https://www.itis.gov/ws_description.html"
    ]
    api_url_beginning : str = "http://www.itis.gov/ITISWebService/"

    class itis_receiveFormat(Enum):
        XML = "services/ITISService"
        JSON = "jsonservice"


    @classmethod
    def sendRequest(cls : type, endStringRequest : str, responseContentFormat : xmlOrJson) -> Dict[Any, Any]:
        # requestToSend_full : str
        if (responseContentFormat == xmlOrJson.XML):
            requestToSend_full : str = os.path.join(cls.api_url_beginning, cls.itis_receiveFormat.XML.value, endStringRequest)
        elif (responseContentFormat == xmlOrJson.JSON):
            requestToSend_full : str = os.path.join(cls.api_url_beginning, cls.itis_receiveFormat.JSON.value, endStringRequest)
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


class Smithsonian_requests(apiRequestsLibrary):
    requestLimitPerHour = 1000
    guideReferences = [
        "https://edan.si.edu/openaccess/apidocs/"
    ]
    api_url_beginning : str = "https://api.si.edu/openaccess/api/v1.0"

    @classmethod
    def sendRequest(cls : type, endStringRequest : str, inParams : dict) -> Dict[Any, Any]:
        
        requestToSend_full : str = os.path.join(cls.api_url_beginning, endStringRequest)

        inParams["api_key"] = api_keys["Data.Gov"]

        try:
            response : requests.Response = requests.get(requestToSend_full, params = inParams)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            print("response.status_code: "+str(response.status_code))
            raise requests.exceptions.HTTPError("Response Status Code: "+str(response.status_code))
        except Exception as error:
            pass

        ## JSON Response
        responseContent_dict : dict = json.loads(response.content)

        return responseContent_dict












# ## Original Methods:


# class itis_receiveFormat(Enum):
#     XML = "services/ITISService"
#     JSON = "jsonservice"

# api_url_beginnings : dict = {
#     "itis" : "http://www.itis.gov/ITISWebService/",
#     "smithsonian" : "https://api.si.edu/openaccess/api/v1.0"
# }

# # ITIS API References:
# # -- https://www.itis.gov/ws_searchApiDescription.html
# # -- https://www.itis.gov/ws_description.html 



# def sendRequest_toITIS(endStringRequest : str, responseContentFormat : xmlOrJson) -> Dict[Any, Any]:
#     requestToSend_full : str
#     if (responseContentFormat == xmlOrJson.XML):
#         requestToSend_full : str = os.path.join(api_url_beginnings["itis"], itis_receiveFormat.XML.value, endStringRequest)
#     elif (responseContentFormat == xmlOrJson.JSON):
#         requestToSend_full : str = os.path.join(api_url_beginnings["itis"], itis_receiveFormat.JSON.value, endStringRequest)
#     else:
#         raise TypeError("responseContentFormat should be \"XML\" or \"JSON\" but it is "+str(responseContentFormat))
    
#     try:
#         response : requests.Response = requests.get(requestToSend_full)
#         response.raise_for_status()
#     except requests.exceptions.HTTPError:
#         print("response.status_code: "+str(response.status_code))
#         raise requests.exceptions.HTTPError("Response Status Code: "+str(response.status_code))
#     except Exception as error:
#         pass

#     responseContent_dict : dict
#     if (responseContentFormat == xmlOrJson.XML):

#         root : etree._Element = etree.XML(response.content, etree.XMLParser())
#         # print(etree.tostring(root))

#         responseContent_dict : dict = xmltodict.parse(response.content)
#     elif (responseContentFormat == xmlOrJson.JSON):
#         responseContent_dict : dict = json.loads(response.content)

#     return responseContent_dict


# # Smithsonian API Reference: https://edan.si.edu/openaccess/apidocs/
# def sendRequest_toSmithsonian(endStringRequest : str, inParams : dict) -> Dict[Any, Any]:
    
#     requestToSend_full : str = os.path.join(api_url_beginnings["smithsonian"], endStringRequest)

#     inParams["api_key"] = api_keys["Data.Gov"]

#     try:
#         response : requests.Response = requests.get(requestToSend_full, params = inParams)
#         response.raise_for_status()
#     except requests.exceptions.HTTPError:
#         print("response.status_code: "+str(response.status_code))
#         raise requests.exceptions.HTTPError("Response Status Code: "+str(response.status_code))
#     except Exception as error:
#         pass

#     ## JSON Response
#     responseContent_dict : dict = json.loads(response.content)

#     return responseContent_dict

