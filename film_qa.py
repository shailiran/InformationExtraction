from build_ontology import *
import rdflib
import requests
import lxml.html

EXAMPLE_PREFIX = "http://example.org/wiki/"

url = "https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"
# create_ontology(url) #TODO - uncomment


def ask_question(question, ontology):
    g = rdflib.Graph()
    g.parse("ontology.nt", format="nt")
    if "directed" in question:
        director_qestion(question, g)
    elif "produced" in question:
        producer_qestion(question, g)
    elif "book" in question:
        based_on_book_qestion(question, g)
    elif "long is" in question:
        running_time_question(question, g)
    elif "starred in" in question:
        starred_in_question(question, g)
    elif "released?" in question:
        released_question(question, g)
    elif "star in" in question:
        person_star_question(question, g)
    elif "born?" in question:
        born_question(question, g)
    elif "occupation" in question:
        occupation_question(question, g)
    elif "starring" in question:
        starring_question(question, g)

def director_qestion(question, g):
    if "Who directed " in question:
        movie = "<" + EXAMPLE_PREFIX + question[13:-1].replace(" ", "_") + ">"
        q = "select ?p where{" \
            "" + movie + " <http://example.org/wiki/Directed_by> ?p."\
            "}"
        x = g.query(q)
        print(list(x))
    return


def producer_qestion(question, g):
    if "Who produced " in question:
        movie = "<" + EXAMPLE_PREFIX + question[13:-1].replace(" ", "_") + ">"
        print(movie)
        q = "select ?p where{" \
            "" + movie + " <http://example.org/wiki/Produced_by> ?p."\
            "}"
        x = g.query(q)
        print(list(x))
    return

def based_on_book_qestion(question, g):
    if "a book" in question:
        movie = "<" + EXAMPLE_PREFIX + question[3:-17].replace(" ", "_") + ">"
        print(movie)
        q = "select ?p where{" \
            "" + movie + " <http://example.org/wiki/Based_on> ?p."\
            "}"
        x = g.query(q)
        if len(list(x)) > 0:
            print("Yes")
            return
        print("No")
        return
    elif "books" in question:
        q = "select ?movie where{" \
            " ?movie <http://example.org/wiki/Based_on> ?p." \
            "}"
        x = g.query(q)
        print(len(list(x)))
        return len(list(x))
    return

def running_time_question(question, g):
    if "How long is " in question:
        movie = "<" + EXAMPLE_PREFIX + question[12:-1].replace(" ", "_") + ">"
        print(movie)
        q = "select ?t where{" \
            "" + movie + " <http://example.org/wiki/Running_time> ?t."\
            "}"
        x = g.query(q)
        print(list(x))
    return

def starred_in_question(question, g):
    if "Who starred in" in question:
        movie = "<" + EXAMPLE_PREFIX + question[15:-1].replace(" ", "_") + ">"
        print(movie)
        q = "select ?p where{" \
            "" + movie + " <http://example.org/wiki/Starring> ?p."\
            "}"
        x = g.query(q)
        print(list(x))
    return list(x)

def released_question(question, g):
    movie = "<" + EXAMPLE_PREFIX + question[9:-10].replace(" ", "_") + ">"
    print(movie)
    q = "select ?t where{" \
        "" + movie + " <http://example.org/wiki/Released_on> ?t."\
        "}"
    x = g.query(q)
    print(list(x))
    return

def born_question(question, g):
    person = "<" + EXAMPLE_PREFIX + question[9:-6].replace(" ", "_") + ">"
    print(person)
    q = "select ?d where{" \
        "" + person + " <http://example.org/wiki/Born_on> ?d."\
        "}"
    x = g.query(q)
    print(list(x))
    return

def person_star_question(question, g):
    start_movie = question.find("in") + 3
    movie = "<" + EXAMPLE_PREFIX + question[start_movie:-1].replace(" ", "_") + ">"
    end_person = question.find("star") - 1
    person = "<" + EXAMPLE_PREFIX + question[4:end_person].replace(" ", "_") + ">"
    stars_movie = starred_in_question("Who starred in " + question[start_movie:], g)
    for star in stars_movie:
        star = str(star).replace('(rdflib.term.URIRef(', '').replace('),)', '')[1:-1]
        if star == person[1:-1]:
            print("Yes")
            return
    print("No")
    return

def occupation_question(question, g):
    start_index = question.find("of") + 3
    person = "<" + EXAMPLE_PREFIX + question[start_index:-1].replace(" ", "_") + ">"
    print(person)
    q = "select ?o where{" \
        "" + person + " <http://example.org/wiki/Occupation> ?o." \
                      "}"
    x = g.query(q)
    print(list(x))
    return


def starring_question(question, g):
    end_person = question.find("won") - 1
    person = "<" + EXAMPLE_PREFIX + question[24:end_person].replace(" ", "_") + ">"

    q = "select ?movies where{" \
        " ?movies <http://example.org/wiki/Starring>" + person + "." \
        "}"
    x = g.query(q)
    print(len(list(x)))
    return len(list(x))


def test():
    ontology = "ontology.nt"
    # print(ask_question("Who directed Mank?", "ontology.nt"))
    entities_questions = ["Who directed Bao (film)?", "Who produced 12 Years a Slave (film)?",
                 "Is The Jungle Book (2016 film) based on a book?", "When was The Great Gatsby (2013 film) released?",
                 "How long is Coco (2017 film)?", "Who starred in The Shape of Water?",
                 "Did Octavia Spencer star in The Shape of Water?", "When was Chadwick Boseman born?",
                 "What is the occupation of Emma Watson?", "How many films starring Meryl Streep won an academy award?",
                 "Who produced Brave (2012 film)?", "Is Brave (2012 film) based on a book?"]
    # for question in entities_questions:
    #     print(question)
    #     ask_question(question, ontology)
    #     print("########################", '\n')

    general_questions = ['How many films are based on books?',
                         'How many films starring Leonardo DiCaprio won an academy award?']
    for question in general_questions:
        print(question)
        ask_question(question, ontology)
        print("########################", '\n')

test()