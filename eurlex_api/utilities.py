import logging
from SPARQLWrapper import SPARQLWrapper, JSON, CSV
# import pandas as pd
import json

# from .lib_cfg import config
logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName('DEBUG'))
logger.addHandler(logging.StreamHandler())


CELLAR_ENDPOINT = 'http://publications.europa.eu/webapi/rdf/sparql'


class CellarReader:
    """
    Stateful object to execute and get results from sparql queries on Cellar's endpoint
    """
    __definitions = [
        ('owl', 'http://www.w3.org/2002/07/owl#'),
        ('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
        ('rdfs', 'http://www.w3.org/2000/01/rdf-schema#'),
        ('skos', 'http://www.w3.org/2004/02/skos/core#'),
        ('dct', 'http://purl.org/dc/terms/'),
        ('xsd', 'http://www.w3.org/2001/XMLSchema#'),
    ]
    __results = None
    __sparql = None

    def __init__(self, definitions):
        """
        Definitions is a list of tuples containing the prefixes used by the query, for
        easier representation (some are predefined, see above)
        definitions = [(PREFIX, URI)|...]
        """
        self.__definitions += definitions
        self.__sparql = SPARQLWrapper(CELLAR_ENDPOINT)
        self.__sparql.setReturnFormat(JSON)
        logger.info('Cellar reader ready')

    def add_definition(self, prefix, uri):
        self.__definitions.append((prefix, uri))
        logger.info('Added prefix %s for uri %s', prefix, uri)

    def test(self):
        try:
            ret = sparql.queryAndConvert()
            print(ret)
        except Exception as e:
            logger.exception(e)
            raise RuntimeError('Failed')

    def execute(self, query, decorate=True):
        if decorate:
            query = self._decorate(query)

        self.__sparql.setQuery(query)
        try:
            self.__results = self.__sparql.queryAndConvert()
        except Exception as e:
            print(e.msg)
            print(e.args[0])
            #logger.exception(str(e))

    def getRawJson(self):
        if not  self.__results:
            raise RuntimeError('No results available')
        return self.__results

    def getJson(self):
        if not  self.__results:
            raise RuntimeError('No results available')
        return self.__results['results']['bindings']

    def getDict(self):
        if not  self.__results:
            raise RuntimeError('No results available')

        buffer = []
        for r in self.getJson() :
            element = {}
            for k in list(r.keys()):
                val = self._prefixOrURIOrWhatever(r[k]['value'])
                element[k] = val

            buffer.append(element)
        return buffer
#  Disabled, might be interesting later
#     def getDF(self):
#         df = pd.DataFrame.from_dict(self.getDict())
#         return df

    def _prefixOrURIOrWhatever(self, uri):
        for p,u in self.__definitions :
            if uri.startswith(u):
                key = uri[len(u):]
                return f"{p}:{key}"
        return uri

    def _decorate(self, query):
        buff = ""

        for p,u in self.__definitions :
            buff += f"PREFIX {p}: <{u}>\n"

        return f"{buff}\n{query}"
