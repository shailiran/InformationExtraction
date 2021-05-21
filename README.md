# InformationExtraction

## :page_with_curl: General description
This is an information extraction system to answer natural language questions about Oscar-winning movies, using ontologies, Xpath, SPARQL, and HTML. <br/>
The data is collected from: https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films.  <br/>

## :question: Questions Format:
#### Questions About Specific Entities:
1. Who directed `<film>`?
2. Who produced `<film>`?
3. Is `<film>` based on a book?
4. When was `<film>` released?
5. How long is `<film>`?
6. Who starred in `<film>`?
7. Did <person> star in `<film>`?
8. When was `<person>` born?
9. What is the occupation of `<person>`?

#### General Questions:
1. How many films are based on books?
2. How many films starring `<person>` won an academy award?
3. How many `<occupation1>` are also `<occupation2>`?
  
## :arrow_forward: Execution Instructions:
To create the ontology run:<br />
```
  python film_qa.py create
```
Then, to ask a question run:<br />
```
  python film_qa.py question “<question>”
```
In question state the program will recieve a question in natural language, print the answer to the screen and stop it's run.

## :woman: Team Members
Rotem Brooks - rotembr10@gmail.com <br/>
Shai Liran - shailiran@gmail.com
