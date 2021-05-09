import rdflib
import requests
import lxml.html

WIKI_PREFIX = "http://en.wikipedia.org"
EXAMPLE_PREFIX = "http://example.org"

def create_ontology(url):
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



def add_directors(g, movie, info_box):
    directed_by = rdflib.URIRef(EXAMPLE_PREFIX + 'directed_by')
    directors = get_directors(info_box)
    for director in directors:
        director_graph = rdflib.URIRef(EXAMPLE_PREFIX + director.replace(" ", "_")) # TODO - use strip()?
        g.add((movie, directed_by, director_graph))


def get_directors(info_box):
