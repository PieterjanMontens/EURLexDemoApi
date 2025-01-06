from fastapi import APIRouter
from ..lib_cfg import config
from ..utilities import logger
import httpx
from fastapi.responses import JSONResponse
import xml.etree.ElementTree as ET
import json
router = APIRouter()

# ############## ROUTE
# ####################


@router.get("/search/quick")
async def search_quick(q: str = ''):
    logger.info('Received quick query request:%s', q)
    response = await get_results('quick', q)
    return JSONResponse(content=response)


@router.get("/search/expert")
async def search_quick(q: str = ''):
    logger.info('Received expert query request:%s', q)
    response = await get_results('expert', q)
    return JSONResponse(content=response)

# ####### SOAP *MAGIC*
# ####################
QUICK_TEMPLATE = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:sear="http://eur-lex.europa.eu/search">
  <soap:Header>
    <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" soap:mustUnderstand="true">
      <wsse:UsernameToken xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" wsu:Id="UsernameToken-1">
        <wsse:Username>%USER%</wsse:Username>
        <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">%TOKEN%</wsse:Password>
      </wsse:UsernameToken>
    </wsse:Security>
  </soap:Header>
    <soap:Body>
    <sear:searchRequest>
      <sear:expertQuery><![CDATA[QUICK_SEARCH ~ "%QUERY%"]]></sear:expertQuery>
      <sear:page>1</sear:page>
      <sear:pageSize>20</sear:pageSize>
      <sear:searchLanguage>fr</sear:searchLanguage>
    </sear:searchRequest>
  </soap:Body>
</soap:Envelope>
"""

EXPERT_TEMPLATE = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:sear="http://eur-lex.europa.eu/search">
  <soap:Header>
    <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" soap:mustUnderstand="true">
      <wsse:UsernameToken xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" wsu:Id="UsernameToken-1">
        <wsse:Username>%USER%</wsse:Username>
        <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">%TOKEN%</wsse:Password>
      </wsse:UsernameToken>
    </wsse:Security>
  </soap:Header>
    <soap:Body>
    <sear:searchRequest>
      <sear:expertQuery><![CDATA[QUICK_SEARCH ~ "%QUERY%"]]></sear:expertQuery>
      <sear:page>1</sear:page>
      <sear:pageSize>20</sear:pageSize>
      <sear:searchLanguage>fr</sear:searchLanguage>
    </sear:searchRequest>
  </soap:Body>
</soap:Envelope>
"""


async def fetch_data(url, headers, body):
    response = httpx.post(url, headers=headers, data=body)
    return response.text
    # Refuses to work for whatever reason
    # async with httpx.AsyncClient() as client:
    #    response = await client.post(url, headers=headers, data=body)
    #    logger.debug('Received reply')
    #    print(response)
    #    return response.text


async def get_results(queryType, query):
    if queryType == 'quick':
        rawquery = QUICK_TEMPLATE
    else:
        rawquery = EXPERT_TEMPLATE

    query = rawquery.replace('%USER%', config.key(['soap_api', 'user_name'])) \
                    .replace('%TOKEN%', config.key(['soap_api', 'user_token'])) \
                    .replace('%QUERY%', query)

    headers = {'Content-Type': 'application/soap+xml'}
    try:
        logger.info('Executing %s query', queryType)
        soapdata = await fetch_data(config.key(['soap_api', 'endpoint']), headers, query)
        jsondata = soap2json(soapdata)
        return jsondata
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        print(f"HTTP error occurred: {exc.response.status_code}")


def soap2json(soap_response):
    # Parse the XML content
    namespaces = {
        'env': 'http://www.w3.org/2003/05/soap-envelope',
        '': 'http://eur-lex.europa.eu/search'
    }
    root = ET.fromstring(soap_response)

    # Locate the Body element in the SOAP response
    body = root.find('env:Body', namespaces)
    if body is None:
        raise ValueError("SOAP Body not found in the response.")

    # Extract the first child of the Body (actual payload content)
    payload = list(body)[0]

    # Recursive function to convert XML to dictionary
    def xml_to_dict(element):
        children = list(element)
        if not children:
            return element.text.strip() if element.text else None
        return {child.tag.split('}')[-1]: xml_to_dict(child) for child in children}

    # Convert the payload to a dictionary
    result = {payload.tag.split('}')[-1]: xml_to_dict(payload)}

    return result
