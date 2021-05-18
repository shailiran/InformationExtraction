import rdflib
import requests
import lxml.html


WIKI_PREFIX = "http://en.wikipedia.org"
EXAMPLE_PREFIX = "http://example.org"
url = "https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"


def create_ontology(url):
    global g
    global urls
    urls = set()
    g = rdflib.Graph()
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    movies_links = doc.xpath("""//table[contains(@class, 'wikitable sortable')]
                        //tr[td[2]//a/text()[number(.) > 2009]]/td[1]//a[@href]/@href""")
    for link in movies_links:
        movie = rdflib.URIRef(f'{EXAMPLE_PREFIX}{link}')
        res = requests.get(WIKI_PREFIX + link)
        doc = lxml.html.fromstring(res.content)
        info_box = doc.xpath("//table[contains(@class, 'infobox')]")
        create_relations(info_box, movie)

    for person_url in urls:
        res = requests.get(person_url)
        doc = lxml.html.fromstring(res.content)
        info_box = doc.xpath("//table[contains(@class, 'infobox')]")
        add_person(info_box)
    g.serialize("ontology.nt", format="nt")


def create_relations(info_box, movie):
    add_relation_by_type(info_box, movie, 'Directed by')
    add_relation_by_type(info_box, movie, 'Produced by')
    add_relation_by_type(info_box, movie, 'Written by')
    add_relation_by_type(info_box, movie, 'Starring')



def add_relation_by_type(info_box, movie, relation):
    fixed_relation = relation.replace(" ", "_")
    relation1 = rdflib.URIRef(EXAMPLE_PREFIX + "/" + fixed_relation)
    if relation == 'Directed by':
        entities = get_directors_info(info_box)
    elif relation == 'Produced by':
        entities = get_producers_info(info_box)
    elif relation == 'Written by':
        entities = get_writers_info(info_box)
    else:
        entities = get_actors_info(info_box)
    for entity in entities:
        # Undefeated movie
        if entity == ' ':
            continue
        entity_graph = rdflib.URIRef(EXAMPLE_PREFIX + "/" + entity.replace(" ", "_")) # TODO - use strip()?
        g.add((movie, relation1, entity_graph))


def get_directors_info(info_box):
    if info_box != []:
        entities = info_box[0].xpath("//table//th[contains(text(), 'Directed by')]/../td/a/text() |"
                                        "//table//th[contains(text(), 'Directed by')]/../td/text() |"
                                        "//table//th[contains(text(), 'Directed by')]/../td/div/ul/li/a/text() |"
                                        "//table//th[contains(text(), 'Directed by')]/../td/div/ul/li/text()")
        entities_urls = info_box[0].xpath("//table//th[contains(text(), 'Directed by')]/../td/a/@href |"
                                          "//table//th[contains(text(), 'Directed by')]/../td/div/ul/li/a/@href")
        for url in entities_urls:
            if url not in urls:
                urls.add(url)
        return entities


def get_producers_info(info_box):
    if info_box != []:
        entities = info_box[0].xpath("//table//th[contains(text(), 'Produced by')]/../td/a/text() |"
                                        "//table//th[contains(text(), 'Produced by')]/../td/text() |"
                                        "//table//th[contains(text(), 'Produced by')]/../td/div/ul/li/a/text() |"
                                        "//table//th[contains(text(), 'Produced by')]/../td/div/ul/li/text()")
        entities_urls = info_box[0].xpath("//table//th[contains(text(), 'Produced by')]/../td/a/@href |"
                                          "//table//th[contains(text(), 'Produced by')]/../td/div/ul/li/a/@href")
        for url in entities_urls:
            if url not in urls:
                urls.add(url)
        return entities


def get_writers_info(info_box):
    if info_box != []:
        entities = info_box[0].xpath("//table//th[contains(text(), 'Written by')]/../td/a/text() |"
                                        "//table//th[contains(text(), 'Written by')]/../td/text() |"
                                        "//table//th[contains(text(), 'Written by')]/../td/div/ul/li/a/text() |"
                                        "//table//th[contains(text(), 'Written by')]/../td/div/ul/li/text()")
        entities_urls = info_box[0].xpath("//table//th[contains(text(), 'Written by')]/../td/a/@href |"
                                          "//table//th[contains(text(), 'Written by')]/../td/div/ul/li/a/@href")
        for url in entities_urls:
            if url not in urls:
                urls.add(url)
        return entities


def get_actors_info(info_box):
    if info_box != []:
        entities = info_box[0].xpath("//table//th[contains(text(),'Starring' )]/../td/a/text() |"
                                        "//table//th[contains(text(),'Starring')]/../td/text() |"
                                        "//table//th[contains(text(),'Starring')]/../td/div/ul/li/a/text() |"
                                        "//table//th[contains(text(),'Starring')]/../td/div/ul/li/text()")
        entities_urls = info_box[0].xpath("//table//th[contains(text(),'Starring')]/../td/a/@href |"
                                          "//table//th[contains(text(),'Starring')]/../td/div/ul/li/a/@href")
        for url in entities_urls:
            if url not in urls:
                urls.add(url)
        return entities


def add_person(info_box):
    if info_box == []:
        return




create_ontology(url)
