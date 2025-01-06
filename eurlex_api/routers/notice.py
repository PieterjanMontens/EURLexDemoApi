from fastapi import APIRouter, Query
from eurlex_api.utilities import CellarReader
from fastapi.responses import JSONResponse
import eurlex_api.queries as queries
from typing import Annotated

router = APIRouter()

prefixes = [
    ('cdm', 'http://publications.europa.eu/ontology/cdm#'),
    ('dct', 'http://purl.org/dc/terms/'),
    ('ann', 'http://publications.europa.eu/ontology/annotation#'),
    ('auth', 'http://publications.europa.eu/ontology/authority/'),
    ('euvoc', 'http://publications.europa.eu/ontology/euvoc#'),
    ('eli', 'http://data.europa.eu/eli/ontology#'),
    ('cmr', 'http://publications.europa.eu/ontology/cdm/cmr#')
]

clr = CellarReader(prefixes)


# ############## ROUTE
# ####################
@router.get("/notice/{celex}", tags=["notice"])
async def notice(
        # celex: Annotated[str, Query(
        #     description="Document CELEX number",
        #     openapi_examples={
        #         "Regulation 666/2013": {
        #             "summary": "Commission Regulation",
        #             "description": "valid CELEX number",
        #             "value": "32013R0666"
        #         }
        #     }
        # )]
        celex: str):
    """
    Notice endpoint
    /notice/[celex] provides the metadata notice from the specified document
    """
    mask = queries.NOTICE
    query = mask.replace('%CELEX%', celex)
    clr.execute(query)
    return JSONResponse(content=clr.getJson())

