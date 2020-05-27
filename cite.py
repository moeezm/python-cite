""" main.py """
import re
from datetime import date
from bs4 import BeautifulSoup
from dateutil import parser
import requests

# Date format strings

def get_first_author(citation):
    """
    Takes the first author from a citation, i.e., returns author if there's one or the first index from a list of authors
    """
    try:
        return citation["author"]
    except KeyError:
        if len(citation["authors"]) > 0:
            return citation["authors"][0]

def get_author_or_title(citation):
    """
    Returns the author if it exists, or returns the title
    """
    first_author = get_first_author(citation)
    if not first_author:
        return citation["title"]
    else:
        return format_name(first_author)

def get_data_from_searches(soup, searches):
    """
    Takes a bs4 object and a list of dictionary searches and returns the data got
    Essentially a wrapper for find()
    Mostly taken from https://github.com/thenaterhood/python-autocite/blob/master/src/python_autocite/lib/datafinder.py
    """
    for s in searches:
        element = soup.find(attrs=s)
        if element is not None:
            try:
                return element['content']
            except KeyError:
                return element.text
    return None

def fromisoformat(date_string):
    """
    Because apparently Transcrypt's datetime library doesn't include this
    """
    parts = date_string.split("-")
    parts = [int(part) for part in parts]
    return date(parts[0], parts[1], parts[2])

def mla_date(date):
    """
    date is a date object
    For example: 6 July 2015
    """
    FORMAT_STRING = "%d %B %Y"
    SHORTENED_MONTH_NAMES = {
            "January": "Jan.",
            "February": "Feb.",
            "March": "Mar.",
            "April": "Apr.",
            "May": "May",
            "June": "June",
            "July": "July",
            "August": "Aug.",
            "September": "Sept.",
            "October": "Oct.",
            "November": "Nov.",
            "December": "Dec."
        }
    formatted_date = date.strftime(FORMAT_STRING)
    parts = formatted_date.split(" ")
    if parts[0][0] == "0": # check if number is zero padded and replace it with regular decimal number
        parts[0] = parts[0][1]
    parts[1] = SHORTENED_MONTH_NAMES[parts[1]]
    return ' '.join(parts)
    
def wrap(text, char='*'):
    """
    Takes a string, text, and wraps it with char on either side
    E.g.
    wrap("hello") -> "*hello*"
    wrap("hi", "~~") -> "~~hi~~"
    """
    return char + text + char

def is_roman_numeral(numeral):
    REGEX_STRING = r"^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$" # from https://stackoverflow.com/a/267405
    numeral = numeral.upper()
    return bool(re.search(REGEX_STRING, numeral))

def is_suffix(s):
    """
    Takes a string and decides if it's a suffix, like "Jr.", "Sr.", "II", etc.
    """
    suffix_list = ["Jr.", "Sr.", "Jnr.", "Snr."]
    if s in suffix_list or is_roman_numeral(s): return True
    return False

def format_name(name):
    """
    Takes a string of a name like "John Doe" and returns "Doe, John"
    E.g.
    "John Doe" -> "Doe, John"
    "Anne Francis Wysocki" -> "Wysocki, Anne Frances"
    "Martin Luther King, Jr." -> "King, Martin Luther, Jr."
    """
    name_data = name.split(" ")
    name_data = [part.replace(',', '') for part in name_data]
    if len(name_data) == 1:
        return name
    if is_suffix(name_data[-1]):
        suffix = name_data[-1]
        last_name = name_data[-2]
        first_name = " ".join(name_data[:-2])
        return f"{last_name}, {first_name}, {suffix}"
    else:
        last_name = name_data[-1]
        first_name = " ".join(name_data[:-1])
        return f"{last_name}, {first_name}"

def generate_book_citation(data):
    """
    data schema:
    {
        "authors": [] list of space separated first then last name (e.g. ["John Doe", "Jane Doe", "Bram Stoker"]
        "title": "" string containing the full title of the book
        "city": "" string containing the city of publication (optional)
        "publisher": "" string containing the name of the publisher
        "publication_year": 0 integer representing the year of publication
    }
    """
    blocks = []

    # Names
    no_of_authors = len(data["authors"])
    if no_of_authors > 0:
        first_author = format_name(data["authors"][0])
        if no_of_authors == 1:
            s = first_author
        elif no_of_authors == 2:
            s = f"{first_author}, and {data['authors'][1]}"
        else:
            s = f"{first_author}, et al"
        s = s[:-1] if s[-1] == "." else s
        blocks.append(s)
        
    # Title
    blocks.append(wrap(data["title"]))

    # Publication Details
    s = f"{data['publisher']}, {data['publication_year']}" 
    if data["city"]:
        s = f"{data['city']}, " + s
    blocks.append(s)

    return ". ".join(blocks)

def generate_webpage_citation(data):
    """
    data schema:
    {
        "author": "" string containing author name (first then last, space separated)
        "title": "" string containing title of webpage
        "website": "" string containing the title of the entire website
        "url": "" string containing the url of the webpage
        "publication_date": "" string containing the date of publication
        "accessed_date": "" string containing the date the website was accessed (default: today)
    }
    """
    blocks = []

    # Author
    if data["author"]:
        blocks.append(format_name(data["author"]))

    # Titles, date, and url
    formatted_title = wrap(data["title"] + ".", '"')
    if data["publication_date"]:
        pub_date = fromisoformat(data["publication_date"])
        blocks.append(f"{formatted_title} {wrap(data['website'])}, {mla_date(pub_date)}, {data['url']}")
    else:
        blocks.append(f"{formatted_title} {wrap(data['website'])}, {data['url']}")

    # Accessed Date
    if data["accessed_date"]:
        acc_date = fromisoformat(data["accessed_date"])
    else:
        acc_date = date.today()
    blocks.append(f"Accessed {mla_date(acc_date)}")

    return ". ".join(blocks)

def get_data_from_webpage(url):
    """
    Takes a string of the url and tries to get all relevant information for citation
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    data = {
            "accessed_date": date.today().isoformat()
        }

    author_searches = [
            {'name': 'author'},
            {'property': 'article:author'},
            {'property': 'author'},
            {'rel': 'author'}
        ]
    author = get_data_from_searches(soup, author_searches)

    title_searches = [
            {'property': 'og:title'}
        ]
    title = get_data_from_searches(soup, title_searches)
    
    website_name_searches = [
            {'property': 'og:site_name'}
        ]
    website_name = get_data_from_searches(soup, website_name_searches)
    
    publication_date_searches = [
            {'name': 'data'},
            {'property': 'published_time'},
            {'name': 'timestamp'},
            {'class': 'submitted-date'},
            {'class': 'posted-on'},
            {'class': 'timestamp'},
            {'class': 'date'}
        ]
    publication_date = get_data_from_searches(soup, publication_date_searches)
    if publication_date is not None:
        publication_date = parser.parse(publication_date).isoformat()[0:10]

    data["author"] = author
    data["title"] = title
    data["website"] = website_name
    data["url"] = url
    data["publication_date"] = publication_date
    
    return data

def auto_cite_webpage(url):
    return generate_webpage_citation(get_data_from_webpage(url))

def generate_citation(data):
    """
    Takes a dictionary representing any type of citation, but must have a "type" key that determines what type of citation it is

    Example:
    "type": "book" -> run generate_book_citation
    """
    mapping = {
            "book": generate_book_citation,
            "webpage": generate_webpage_citation
        }

    type_of_citation = data.pop('type')
    return mapping[type_of_citation](data)

def generate_citations(data):
    """
    Takes a variable amount of citations, in JSON format, and returns a works cited page. Essentially wraps generate_citation multiple times and handles sorting, etc. "data" represents a list of citations (len() can be 1) or simply a dictionary representing one citation.
    """
    if len(data) == 1: # Simply return citation if there's only one
        return generate_citation(data[0])

    if type(data) is dict:
        return generate_citation(data)

    # No else clause because the true case will terminate the function
    sorted_citations = sorted(data, key=get_author_or_title)
    result = []

    prevAuthor = "" # placeholder value
    for citation in sorted_citations:
        first_author = get_first_author(citation)
        if first_author == prevAuthor and first_author != "":
            try:
                citation["author"] = "---"
            except KeyError:
                citation["authors"] = ["---"]
        else:
            prevAuthor = first_author 
        result.append(generate_citation(citation))

    return "\n".join(result)

