import requests
import re
import json
import utils
from requests_body import *

session = requests.Session()


def login(encrypted_mem_id):
    """Perform login and return session ID without persistent connection"""
    url = "https://sev01.gigp.vip/GAAndroidSer/AndWsService.svc"
    
    headers = {
        "Content-Type": "application/soap+xml; charset=utf-8",
        "Host": "sev01.gigp.vip",
        "SOAPAction": "http://tempuri.org/IAndWsService/IGetLogin"
    }

    body = getLoginRequestBody(encrypted_mem_id)

    try:
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()
        
        match = re.search(r'OK,(\d+),', response.text)
        if match:
            session_id = int(match.group(1))
            return session_id
        else:
            print("Login response format unexpected:", response.text)
            return None
            
    except requests.RequestException as e:
        print(f"Login failed: {str(e)}")
        return None



def getAndharBaharLastStatus(input_str):
    url = "https://sev01.gigp.vip/GAAndroidSer/AndWsService.svc"
    headers = {
        "Content-Type": "application/soap+xml; charset=utf-8",
        "Host": "sev01.gigp.vip",
        "SOAPAction": "http://tempuri.org/IAndWsService/IGetAndharBaharLastStatus"
    }
    body = getAndharBaharLastStatusRequestBody(input_str)

    try:
        response = session.post(url, headers=headers, data=body)
        response.raise_for_status()

        match = re.search(r"<IGetAndharBaharLastStatusResult>(.*?)</IGetAndharBaharLastStatusResult>", response.text)
        if match:
            encrypted_result = match.group(1)
            decrypted_result = utils.decrypt(encrypted_result)
            print(decrypted_result)

            timerVal = int(decrypted_result.split(':')[2].split(',')[1])
            drawId = int(decrypted_result.split(':')[2].split(',')[0])
            return timerVal+1,drawId
        else:
            print("Unexpected response format:", response.text)
            return None,None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None,None


def getAndharBaharDrawnoResult(input_str):
    url = "https://sev01.gigp.vip/GAAndroidSer/AndWsService.svc"
    headers = {
        "Content-Type": "application/soap+xml; charset=utf-8",
        "Host": "sev01.gigp.vip",
        "SOAPAction": "http://tempuri.org/IAndWsService/IGetAnharBaharDrawno"
    }
    body = getAndharBaharDrawNoRequestBody(input_str)

    for i in range(5):
        try:
            response = session.post(url, headers=headers, data=body)
            response.raise_for_status()
            print(response.text)

            match = re.search(r"<IGetAnharBaharDrawnoResult>(.*?)</IGetAnharBaharDrawnoResult>", response.text)
            if match:

                data = match.group(1).split(',')

                if len(data)!=5:
                    continue


                if data[0][-1] == data[1][-1]:
                    return 1,int(data[3]),int(data[4])
                
                else:
                    return 0,int(data[3]),int(data[4])
                
            else:
                print("Unexpected response format:", response.text)
                continue
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            continue
    return None, None, None