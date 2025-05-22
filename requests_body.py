import utils

def getAndharBaharLastStatusRequestBody(value):
    encrypted_str = utils.encrypt(value)

    request_body = f'''<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:a="http://www.w3.org/2005/08/addressing"
            xmlns:s="http://www.w3.org/2003/05/soap-envelope">
  <s:Header>
    <a:Action s:mustUnderstand="1">http://tempuri.org/IAndWsService/IGetAndharBaharLastStatus</a:Action>
    <a:MessageID>urn:uuid:9f960604-1092-441a-b063-7bb69c720f08</a:MessageID>
    <a:ReplyTo>
      <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
    </a:ReplyTo>
    <a:To s:mustUnderstand="1">https://sev07.gigp.vip/GAAndroidSer/AndWsService.svc</a:To>
  </s:Header>
  <s:Body>
    <IGetAndharBaharLastStatus xmlns="http://tempuri.org/">
      <abindata>{encrypted_str}</abindata>
    </IGetAndharBaharLastStatus>
  </s:Body>
</s:Envelope>'''

    return request_body



def getAndharBaharDrawNoRequestBody(value):

    encrypted_drawId = utils.encrypt(str(value))

    request_body = f"""<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:a="http://www.w3.org/2005/08/addressing" xmlns:s="http://www.w3.org/2003/05/soap-envelope">
  <s:Header>
    <a:Action s:mustUnderstand="1">http://tempuri.org/IAndWsService/IGetAnharBaharDrawno</a:Action>
    <a:MessageID>urn:uuid:c44c7acf-06e0-4553-9ba9-fa3e9616c094</a:MessageID>
    <a:ReplyTo>
      <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
    </a:ReplyTo>
    <a:To s:mustUnderstand="1">https://sev07.gigp.vip/GAAndroidSer/AndWsService.svc</a:To>
  </s:Header>
  <s:Body>
    <IGetAnharBaharDrawno xmlns="http://tempuri.org/">
      <abdrawno>{encrypted_drawId}</abdrawno>
    </IGetAnharBaharDrawno>
  </s:Body>
</s:Envelope>"""

    return request_body




def getLoginRequestBody(encrypted_mem_id):
    request_body = f"""<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:a="http://www.w3.org/2005/08/addressing" xmlns:s="http://www.w3.org/2003/05/soap-envelope">
    <s:Header>
        <a:Action s:mustUnderstand="1">http://tempuri.org/IAndWsService/IGetLogin</a:Action>
        <a:MessageID>urn:uuid:ab072085-7b1b-4eca-b368-8da9f7198f2f</a:MessageID>
        <a:ReplyTo>
            <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
        </a:ReplyTo>
        <a:To s:mustUnderstand="1">https://sev01.gigp.vip/GAAndroidSer/AndWsService.svc</a:To>
    </s:Header>
    <s:Body>
        <IGetLogin xmlns="http://tempuri.org/">
            <mem_id>{encrypted_mem_id}</mem_id>
        </IGetLogin>
    </s:Body>
</s:Envelope>"""

    return request_body