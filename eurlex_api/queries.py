RECENT_OJ = """
SELECT  ?aba ?creation group_concat(distinct ?rtype;separator=";") as ?group_rt  ?exp ?title ?number ?year ?serie ?reference_oj ?oj_psi
WHERE
{
    ?aba  cmr:creationDate            ?creation;
          cdm:work_has_resource-type  ?rtype.
    OPTIONAL
    {
        ?exp  cdm:expression_belongs_to_work  ?aba;
              cdm:expression_uses_language    <http://publications.europa.eu/resource/authority/language/%LANGUAGE%>;
              cdm:expression_title            ?title.
    }
    ?aba  cdm:official-journal-act_number                       ?number;
          cdm:official-journal-act_year                         ?year;
          cdm:official-journal-act_part_of_collection_document  ?serie;
          cdm:resource_legal_reference_oj-act                   ?reference_oj;
          owl:sameAs                                            ?oj_psi.
    FILTER (
        regex(str(?oj_psi), '/oj/')
    )
    FILTER (
        xsd:datetime(substr(str(xsd:datetime(?creation)), 1, 19)) >
                                   xsd:datetime(substr(str(xsd:datetime(now()) - xsd:duration('%PERIOD%')), 1, 19))
    )
}
ORDER BY DESC(?serie) DESC(?creation)
"""

NOTICE = """
SELECT *
WHERE
{
    ?doc cdm:resource_legal_id_celex ?doc_celex.
    FILTER(str(?doc_celex)='%CELEX%')
    ?doc ?predicate ?object.
}
"""
