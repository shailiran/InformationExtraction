from build_ontology import *
import rdflib
import sys

EXAMPLE_PREFIX = "http://example.org/wiki/"

url = "https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"


def ask_question(question, ontology):
    g = rdflib.Graph()
    g.parse(ontology, format="nt")
    if "directed" in question:
        res = director_qestion(question, g)
    elif "produced" in question:
        res = producer_qestion(question, g)
    elif " book" in question:
        res = based_on_book_qestion(question, g, 0)
    elif "long is" in question:
        res = running_time_question(question, g)
    elif "starred in" in question:
        res = starred_in_question(question, g, 0)
    elif "released?" in question:
        res = released_question(question, g)
    elif "star in" in question:
        res = person_star_question(question, g, 0)
    elif "born?" in question:
        res = born_question(question, g)
    elif "occupation" in question:
        res = occupation_question(question, g, 0)
    elif "starring" in question:
        res = starring_question(question, g)
    elif "are also" in question:
        res = occupations_question(question, g)
    return res


def director_qestion(question, g):
    movie = "<" + EXAMPLE_PREFIX + question[13:-1].replace(" ", "_") + ">"
    q = "select ?p where{" \
        "" + movie + " <http://example.org/wiki/Directed_by> ?p."\
        "}"
    x = g.query(q)
    print(print_ans(fix_answer(list(x))))
    return print_ans(fix_answer(list(x)))


def producer_qestion(question, g):
    movie = "<" + EXAMPLE_PREFIX + question[13:-1].replace(" ", "_") + ">"
    q = "select ?p where{" \
        "" + movie + " <http://example.org/wiki/Produced_by> ?p."\
        "}"
    x = g.query(q)
    print(print_ans(fix_answer(list(x))))
    return print_ans(fix_answer(list(x)))


def based_on_book_qestion(question, g, external):
    if "starring" in question:
        # "How many films starring <person> are also based on books?"
        q_1 = "How many films are based on books"
        movies_based_on_books = based_on_book_qestion(q_1, g, 1)
        start_person = question.find("starring") + len("starring") + 1
        end_person = question.find("are") - len("are") + 2
        person = question[start_person:end_person]
        cnt = 0
        for movie in movies_based_on_books:
            q_2 = "Did " + person + " star in " + ans_format(movie) + "?"
            if person_star_question(q_2, g, 1) == "Yes":
                cnt += 1
        print(cnt)
    elif "a book" in question:
        movie = "<" + EXAMPLE_PREFIX + question[3:-17].replace(" ", "_") + ">"
        q = "select ?p where{" \
            "" + movie + " <http://example.org/wiki/Based_on> ?p."\
            "}"
        x = g.query(q)
        if len(list(x)) > 0:
            print("Yes")
            return "Yes"
        print("No")
        return "No"
    elif "books" in question:
        q = "select ?movie where{" \
            " ?movie <http://example.org/wiki/Based_on> ?p." \
            "}"
        x = g.query(q)
        if external == 1:
            return list(x)
        print(len(list(x)))
        return str(len(list(x)))
    return


def running_time_question(question, g):
    movie = "<" + EXAMPLE_PREFIX + question[12:-1].replace(" ", "_") + ">"
    q = "select ?t where{" \
        "" + movie + " <http://example.org/wiki/Running_time> ?t."\
        "}"
    x = g.query(q)
    print(print_ans(fix_answer(list(x))))
    return print_ans(fix_answer(list(x)))


def starred_in_question(question, g, internal):
    movie = "<" + EXAMPLE_PREFIX + question[15:-1].replace(" ", "_") + ">"
    q = "select ?p where{" \
        "" + movie + " <http://example.org/wiki/Starring> ?p."\
        "}"
    x = g.query(q)
    if internal == 1:
        return list(x)
    print(print_ans(fix_answer(list(x))))
    return print_ans(fix_answer(list(x)))


def released_question(question, g):
    movie = "<" + EXAMPLE_PREFIX + question[9:-10].replace(" ", "_") + ">"
    q = "select ?t where{" \
        "" + movie + " <http://example.org/wiki/Released_on> ?t."\
        "}"
    x = g.query(q)
    print(print_ans(fix_answer(list(x))))
    return print_ans(fix_answer(list(x)))


def born_question(question, g):
    person = "<" + EXAMPLE_PREFIX + question[9:-6].replace(" ", "_") + ">"
    q = "select ?d where{" \
        "" + person + " <http://example.org/wiki/Born_on> ?d."\
        "}"
    x = g.query(q)
    print(print_ans(fix_answer(list(x))))
    return print_ans(fix_answer(list(x)))


def person_star_question(question, g, internal):
    start_movie = question.find(" in ") + 4
    movie = "<" + EXAMPLE_PREFIX + question[start_movie:-1].replace(" ", "_") + ">"
    end_person = question.find(" star ")
    person = "<" + EXAMPLE_PREFIX + question[4:end_person].replace(" ", "_") + ">"
    stars_movie = starred_in_question("Who starred in " + question[start_movie:], g, 1)
    for star in stars_movie:
        star = URIRef_to_string(star)
        if star == person[1:-1]:
            if internal == 1:
                return  "Yes"
            print("Yes")
            return "Yes"
    if internal == 1:
        return "No"
    print("No")
    return "No"


def occupation_question(question, g, internal):
    start_index = question.find(" of ") + 4
    person = "<" + EXAMPLE_PREFIX + question[start_index:-1].replace(" ", "_") + ">"
    q = "select ?o where{" \
        "" + person + " <http://example.org/wiki/Occupation> ?o." \
                      "}"
    x = g.query(q)
    if internal == 1:
        return list(x)
    print(print_ans(fix_answer(list(x))))
    return print_ans(fix_answer(list(x)))


def starring_question(question, g):
    end_person = question.find(" won ")
    person = "<" + EXAMPLE_PREFIX + question[24:end_person].replace(" ", "_") + ">"

    q = "select ?movies where{" \
        " ?movies <http://example.org/wiki/Starring>" + person + "." \
        "}"
    x = g.query(q)
    print(str(len(list(x))))
    return str(len(list(x)))


def occupations_question(question, g):
    start_occupation1 = question.find(" many ") + len(" many ")
    end_occupation1 = question.find(" are ")
    occupation_1 = "<" + EXAMPLE_PREFIX + question[start_occupation1:end_occupation1].replace(" ", "_") + ">"
    start_occupation2 = question.find(" also ") + len(" also ")
    occupation_2 = "<" + EXAMPLE_PREFIX + question[start_occupation2:-1].replace(" ", "_") + ">"

    q1 = "select ?person where{" \
        " ?person <http://example.org/wiki/Occupation>" + occupation_1 + "." \
        "}"
    cnt = 0
    persons = list(g.query(q1))
    for person in persons:
        person = URIRef_to_string(person)[len(EXAMPLE_PREFIX):]
        occupations_to_check = occupation_question("What is the occupation of " + person + "?", g, 1)
        for oc in occupations_to_check:
            tmp = "<" + URIRef_to_string(oc) + ">"
            if tmp == occupation_2:
                cnt += 1
    print(str(cnt))
    return cnt



def URIRef_to_string(ans):
    return str(ans).replace('(rdflib.term.URIRef(', '').replace('),)', '')[1:-1]


def ans_format(ans):
    return URIRef_to_string(ans).replace("_", " ")[len(EXAMPLE_PREFIX):]


def fix_answer(list_ans):
    res = []
    for ans in list_ans:
        res.append(ans_format(ans))
    return sorted(res)

def print_ans(ans_lst):
    return ', '.join([str(elem) for elem in ans_lst])



def main():
    args = sys.argv
    if args[1] == 'create':
        create_ontology(url)
    elif args[1] == 'question':
        ask_question(args[2], 'ontology.nt')


if __name__ == "__main__":
    main()
