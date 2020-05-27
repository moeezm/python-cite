from cite import *
from datetime import date
from copy import deepcopy

def test(function, test_cases):
    """
    test_cases is a list of lists where each sub list is the list of arguments, aka onne case
    """
    test_cases2 = deepcopy(test_cases)
    print(f"testing {function.__name__}...")
    for case in test_cases2:
        print(*case, sep=', ', end='')
        result = function(*case)
        print(f" -> {result}")
    print("\n")

# Test conversion from iso format
isoformat_test_cases = [
        ["2020-04-01"],
        ["1999-01-01"],
        ["2000-09-20"],
        ["2035-11-30"]
    ]
test(fromisoformat, isoformat_test_cases)

# Test MLA date formatting
mla_date_test_cases = [
        [date(2020, 9, 1)],
        [date(2020, 7, 1)],
        [date(2020, 1, 25)],
        [date.today()]
    ]
test(mla_date, mla_date_test_cases)

# Test Roman Numerals
roman_numeral_test_cases = [
            ["IV"],
            ["vi"],
            ["XM"]
        ]
test(is_roman_numeral, roman_numeral_test_cases)

# Test suffix detection
suffix_test_cases = [
        ["Jr."],
        ["Bob"],
        ["Sr."],
        ["II"],
        ["Jnr."],
        ["Snr."]
    ]
test(is_suffix, suffix_test_cases)

# Test name formatting
name_test_cases = [
        ["John Doe"],
        ["Martin Luther King, Jr."],
        ["Moeez Muhammad II"], # I don't know anyone named with II
        ["David Foster Wallace"],
        ["---"],
        ["Bob"]
    ]
test(format_name, name_test_cases)

# Test citations
book_citation_test_cases = [
        [{
            "authors": ["James Gleick"],
            "title": "Chaos: Making a New Science",
            "city": "",
            "publisher": "Penguin",
            "publication_year": 1987
        }],
        [{
            "authors": ["Paula Gillespie", "Neal Lerner"],
            "title": "The Allyn and Bacon Guide to Peer Tutoring",
            "city": "",
            "publisher": "Allyn and Bacon",
            "publication_year": 2000
        }],
        [{
            "authors": ["Moeez Muhammad II", "Moeez Muhammad III", "Moeez Muhammad IV"],
            "title": "Some Book",
            "city": "Toronto",
            "publisher": "Moeez Publishing",
            "publication_year": 2020
        }],
        [{
            "authors": [],
            "title": "Encyclopedia of Indiana",
            "city": "",
            "publisher": "Somerset",
            "publication_year": 1993
        }],
        [{
            "authors": ["---", "Bob"],
            "title": "Some Book: 2nd Edition",
            "city": "Toronto: 2nd Edition",
            "publisher": "NULL",
            "publication_year": 1900
        }],
        [{
            "authors": ["Some M Guy"],
            "title": "I'm Running Out Of Book Titles",
            "city": "",
            "publisher": "Random House",
            "publication_year": 1500
        }]
    ]
test(generate_book_citation, book_citation_test_cases)

# Website citations
website_citation_test_cases = [
        [{
            "author": "Susan Lundman",
            "title": "How to Make Vegetarian Chili",
            "website": "eHow",
            "url": "www.ehow.com/how_10727_make-vegetarian-chili.html",
            "publication_date": "",
            "accessed_date": "2020-03-01"
        }],
        [{
            "author": "",
            "title": "Athlete's Foot - Topic Overview",
            "website": "WebMD",
            "url": "www.webmd.com/generic-url",
            "publication_date": "2014-09-25",
            "accessed_date": ""
        }]

    ]
test(generate_webpage_citation, website_citation_test_cases)

# Test grabbing data from a url
website_data_get_test_cases = [
        ["https://arstechnica.com/information-technology/2012/12/report-data-caps-just-a-cash-cow-for-internet-providers/"],
        ["https://www.leaf.tv/articles/mexican-staple-foods/"]
    ]
test(get_data_from_webpage, website_data_get_test_cases)

# Test auto citing
test(auto_cite_webpage, website_data_get_test_cases)

# Test general citation
citation_test_cases = [
        [{
            "author": "Susan Lundman",
            "title": "How to Make Vegetarian Chili",
            "website": "eHow",
            "url": "www.ehow.com/how_10727_make-vegetarian-chili.html",
            "publication_date": "",
            "accessed_date": "",
            "type": "webpage"
        }],
        [{
            "authors": ["Paula Gillespie", "Neal Lerner"],
            "title": "The Allyn and Bacon Guide to Peer Tutoring",
            "city": "",
            "publisher": "Allyn and Bacon",
            "publication_year": 2000,
            "type": "book"
        }]
    ]
test(generate_citation, citation_test_cases)

# Test list of citations
citations_test_cases = [
        [[{
            "author": "Susan Lundman",
            "title": "How to Make Vegetarian Chili",
            "website": "eHow",
            "url": "www.ehow.com/how_10727_make-vegetarian-chili.html",
            "publication_date": "",
            "accessed_date": "",
            "type": "webpage"
        },
        {
            "authors": ["Paula Gillespie", "Neal Lerner"],
            "title": "The Allyn and Bacon Guide to Peer Tutoring",
            "city": "",
            "publisher": "Allyn and Bacon",
            "publication_year": 2000,
            "type": "book"
        },
        {
            "author": "Susan Lundman",
            "title": "How to Make Vegetarian Chili: The Reboot",
            "website": "eHow",
            "url": "www.ehow.com/some_page.html",
            "publication_date": "",
            "accessed_date": "2020-03-01",
            "type": "webpage"
        },
        {
            "author": "",
            "title": "Athlete's Foot - Topic Overview",
            "website": "WebMD",
            "url": "www.webmd.com/generic-url",
            "publication_date": "2014-09-25",
            "accessed_date": "",
            "type": "webpage"
        },
        {
            "authors": ["Moeez Muhammad II", "Moeez Muhammad III", "Moeez Muhammad IV"],
            "title": "Some Book",
            "city": "Toronto",
            "publisher": "Moeez Publishing",
            "publication_year": 2020,
            "type": "book"
        },
        {
            "authors": [],
            "title": "Encyclopedia of Indiana",
            "city": "",
            "publisher": "Somerset",
            "publication_year": 1993,
            "type": "book"
        }]]
    ]
test(generate_citations, citations_test_cases)

with open('output.txt', 'w+') as output:
    output.write(generate_citations(citations_test_cases[0][0]))
