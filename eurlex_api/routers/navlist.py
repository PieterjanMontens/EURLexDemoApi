from fastapi import APIRouter
from fastapi.responses import JSONResponse
from eurlex_api.utilities import CellarReader
import eurlex_api.queries as queries

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

# For period syntax, see https://www.datypic.com/sc/xsd/t-xsd_duration.html#:~:text=The%20format%20of%20xsd%3Aduration,date%20and%20time%2C%20nH%20is


# ############## ROUTE
# ####################
@router.get("/list/todayoj", tags=["list"])
async def today():
    mask = queries.RECENT_OJ
    query = mask.replace('%LANGUAGE%', 'ENG') \
                .replace('%PERIOD%', 'P1D')
    clr.execute(query)
    return JSONResponse(content=clr.getJson())


@router.get("/list/recent", tags=["list"])
async def recent():
    mask = queries.RECENT_OJ
    query = mask.replace('%LANGUAGE%', 'ENG') \
                .replace('%PERIOD%', 'P6D')
    clr.execute(query)
    return JSONResponse(content=clr.getJson())
