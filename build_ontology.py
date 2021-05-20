import rdflib
import requests
import lxml.html


WIKI_PREFIX = "http://en.wikipedia.org"
EXAMPLE_PREFIX = "http://example.org/wiki/"
EXAMPLE_PREFIX_WOWIKI = "http://example.org"
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
        movie = rdflib.URIRef(f'{EXAMPLE_PREFIX_WOWIKI}{link}')
        res = requests.get(WIKI_PREFIX + link)
        doc = lxml.html.fromstring(res.content)
        info_box = doc.xpath("//table[contains(@class, 'infobox')]")
        create_relations(info_box, movie)

    for person_url in urls:
        res = requests.get(person_url)
        doc = lxml.html.fromstring(res.content)
        info_box = doc.xpath("//table[contains(@class, 'infobox')]")
        name = person_url.split("/")[-1]
        add_person(info_box, name)
    g.serialize("ontology.nt", format="nt")


def create_relations(info_box, movie):
    add_relation_by_type(info_box, movie, 'Directed by')
    add_relation_by_type(info_box, movie, 'Produced by')
    add_relation_by_type(info_box, movie, 'Starring')
    add_release_date(info_box, movie)
    add_based_on(info_box, movie)
    add_running_time(info_box, movie)

def add_relation_by_type(info_box, movie, relation):
    fixed_relation = relation.replace(" ", "_")
    relation_for_ontology = rdflib.URIRef(EXAMPLE_PREFIX + fixed_relation)
    if relation == 'Directed by':
        entities = get_directors_info(info_box)
    elif relation == 'Produced by':
        entities = get_producers_info(info_box)
    else:
        entities = get_actors_info(info_box)
    for entity in entities:
        # Undefeated movie
        if entity == ' ':
            continue
        entity_graph = rdflib.URIRef(EXAMPLE_PREFIX + entity.strip().replace(" ", "_"))
        g.add((movie, relation_for_ontology, entity_graph))


def get_directors_info(info_box):
    if info_box != []:
        entities = info_box[0].xpath("//table//th[contains(text(), 'Directed by')]/../td/a/@href |"
                                        "//table//th[contains(text(), 'Directed by')]/../td/text() |"
                                        "//table//th[contains(text(), 'Directed by')]/../td/div/ul/li/a/@href |"
                                        "//table//th[contains(text(), 'Directed by')]/../td/div/ul/li/text()")
        for i, entity in enumerate(entities):
            if "wiki" in entity:
                entities[i] = entity[6:]
        entities_urls = info_box[0].xpath("//table//th[contains(text(), 'Directed by')]/../td/a/@href |"
                                          "//table//th[contains(text(), 'Directed by')]/../td/div/ul/li/a/@href")
        add_urls(entities_urls)
        return entities


def get_producers_info(info_box):
    if info_box != []:
        entities = info_box[0].xpath("//table//th[contains(text(), 'Produced by')]/../td/a/@href |"
                                        "//table//th[contains(text(), 'Produced by')]/../td/text() |"
                                        "//table//th[contains(text(), 'Produced by')]/../td/div/ul/li/a/@href |"
                                        "//table//th[contains(text(), 'Produced by')]/../td/div/ul/li/text()")
        for i, entity in enumerate(entities):
            if "wiki" in entity:
                entities[i] = entity[6:]
        entities_urls = info_box[0].xpath("//table//th[contains(text(), 'Produced by')]/../td/a/@href |"
                                          "//table//th[contains(text(), 'Produced by')]/../td/div/ul/li/a/@href")
        add_urls(entities_urls)
        return entities


def get_actors_info(info_box):
    if info_box != []:
        entities = info_box[0].xpath("//table//th[contains(text(),'Starring' )]/../td/a/@href |"
                                        "//table//th[contains(text(),'Starring')]/../td/text() |"
                                        "//table//th[contains(text(),'Starring')]/../td/div/ul/li/a/@href |"
                                        "//table//th[contains(text(),'Starring')]/../td/div/ul/li/text()")
        for i, entity in enumerate(entities):
            if "wiki" in entity:
                entities[i] = entity[6:]
        entities_urls = info_box[0].xpath("//table//th[contains(text(),'Starring')]/../td/a/@href |"
                                          "//table//th[contains(text(),'Starring')]/../td/div/ul/li/a/@href")
        add_urls(entities_urls)
        return entities

def add_release_date(info_box, movie):
    if info_box == []:
        return
    dates = info_box[0].xpath("//table//th/div[contains(text(),'Release date')]/../../td//span[contains(@class, 'bday dtstart published updated')]/text()")
    if len(dates) == 0:
        return
    for date in dates:
        date_graph = rdflib.URIRef(EXAMPLE_PREFIX + date)
        relation = rdflib.URIRef(EXAMPLE_PREFIX + 'Released_on')
        g.add((movie, relation, date_graph))


def add_based_on(info_box, movie):
    if info_box == []:
        return
    book = info_box[0].xpath("//table//th[contains(text(),'Based on')]/../td//i/a/text() |"
                             "//table//th[contains(text(),'Based on')]/../td//a/text() |"
                             "//table//th[contains(text(),'Based on')]/../td/div/i/text()")
    if len(book) == 0:
        return
    book_graph = rdflib.URIRef(EXAMPLE_PREFIX + book[0].replace(" ", "_"))
    relation = rdflib.URIRef(EXAMPLE_PREFIX + 'Based_on')
    g.add((movie, relation, book_graph))

def add_running_time(info_box, movie):
    if info_box == []:
        return
    times = info_box[0].xpath("//table//th/div[contains(text(),'Running time')]/../../td/text() |"
                             "//table//th/div[contains(text(),'Running time')]/../../td//li/text()")
    if len(times) == 0:
        return
    relation = rdflib.URIRef(EXAMPLE_PREFIX + 'Running_time')
    for time in times:
        time_graph = rdflib.URIRef(EXAMPLE_PREFIX + time.strip().replace(" ", "_"))
        g.add((movie, relation, time_graph))


def add_urls(entities_urls):
    for url in entities_urls:
        url_with_prefix = WIKI_PREFIX + url
        if url_with_prefix not in urls:
            urls.add(url_with_prefix)


def add_person(info_box, name):
    if info_box == []:
        return
    add_person_by_type(info_box, name, 'Born')
    add_person_by_type(info_box, name, 'Occupation')


def add_person_by_type(info_box, name, relation):
    if name == "Gary_Gilbert": # TODO - check!
        return
    name_graph = rdflib.URIRef(EXAMPLE_PREFIX + name)
    if relation == 'Born':
        add_bday(info_box, name_graph)
    elif relation == 'Occupation':
        add_occupation(info_box, name_graph)


def add_bday(info_box, name_graph):
    bday = info_box[0].xpath("//table//th[contains(text(),'Born')]/../td//span[contains(@class, 'bday')]/text() |"
                             "//table//th[contains(text(),'Born')]/../td[contains(@class,'infobox-data')]/text()")
    if len(bday) == 0:
        # print(name_graph)
        return
    if "/" in bday[0]:
        bday_graph = rdflib.URIRef(EXAMPLE_PREFIX + bday[0].strip().split("/")[0])
    elif " " in bday[0]:
        if "age" not in bday[0]:
            bday_graph = rdflib.URIRef(EXAMPLE_PREFIX + bday[0].split(" ")[-1])
        else:
            bday_graph = rdflib.URIRef(EXAMPLE_PREFIX + bday[0].split(" ")[0].split(";")[-1])
    else:
        bday_graph = rdflib.URIRef(EXAMPLE_PREFIX + bday[0].replace(".", "-"))

    relation = rdflib.URIRef(EXAMPLE_PREFIX + 'Born_on')
    g.add((name_graph, relation, bday_graph))


#
# Birthday = infobox[0].xpath( "//table//th[contains(text(), 'Born')]/../td/div/ul/li/span/span[contains(@class,'bday')]/text() |"
#             "//table//th[contains(text(), 'Born')]/../td/div/ul/li/span/span[contains(@class,'bday')]/text()|"
#             "//table//th[contains(text(), 'Born')]/../td[text() !=' ']/span/span[contains(@class,'bday')]/text()|"
#             "//table//th[contains(text(), 'Born')]/../td/span/span[contains(@class,'bday')]/text()|"
#             "//table//th[contains(text(), 'Born')]/../td/span/div/ul/li/span/span[contains(@class,'bday')]/text() |"
#             "//table//th[contains(text(), 'Born')]/../td/span/span[contains(@class,'bday')]/text()|"
#             "//table//th[contains(text(), 'Born')]/../td/div/div/ul/li/span/span[contains(@class,'bday')]/text()|"
#                                      "//table//th[contains(text(), 'Born')]/../td/span/span/span[contains(@class,'bday')]/text()")

def add_occupation(info_box, name_graph):
    occupations = info_box[0].xpath("//table//th[contains(text(),'Occupation')]/../td[contains(@class, 'infobox-data role')]/text() |"
                                   "//table//th[contains(text(),'Occupation')]/../td[contains(@class, 'infobox-data role')]/a/text() |"
                                   "//table//th[contains(text(),'Occupation')]/../td[contains(@class, 'infobox-data role')]/div//li/text()")

    relation = rdflib.URIRef(EXAMPLE_PREFIX + 'Occupation')
    if len(occupations) == 1:
        occupations = occupations[0].split(",")

    for occupation in occupations:
        occupation_str = occupation.strip().lower().replace(" ", "_")
        if len(occupation_str) < 2:
            continue
        occupation_graph = rdflib.URIRef(EXAMPLE_PREFIX + occupation_str)
        g.add((name_graph, relation, occupation_graph))









