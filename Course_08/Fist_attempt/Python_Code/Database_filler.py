import re
import regex
from Bio import Entrez
import sqlite3

con = sqlite3.connect("db_twinning.db")
cur = con.cursor()


def openen(file):
    """
    Opens a file, reads the contents, and fetches details for each ID list found in the file.

    Args:
        file (str): Path to the file to be opened.

    Returns:
        None
    """
    count = 0
    with open(file) as file:
        regex_id_list = r"\[.+]"
        regex_id_name = r"ID's.*"
        Id = ""
        for line in file:
            line = line.strip("\n")
            if re.search(regex_id_name, line):
                Id = line
            elif re.match(regex_id_list, line):
                count += 1
                print(count)
                fetch_details(line, Id)
    con.close()


def fetch_details(id_list, id_name):
    """
    Fetches details for a given ID list using Entrez and inserts the data into the database.

    Args:
        id_list (str): List of IDs.
        id_name (str): ID names containing keyword information.

    Returns:
        None
    """
    print(id_name)
    Entrez.email = 'rmh.engels@student.han.nl'
    handle = Entrez.efetch(db='pubmed', retmode='xml', id=id_list)
    results = Entrez.read(handle)

    no_author_check = True
    no_title_check = True
    no_date_check = True
    no_abstract_check = True

    ids = re.findall(r"\b\d+\b", id_list)

    for i, paper in enumerate(results['PubmedArticle']):
        print("\nScript one results:")
        
        no_author_check, names = check_authors(paper, i, no_author_check)
        no_title_check, title = check_titles(paper, i, no_title_check)
        no_date_check, date = check_dates(paper, i, no_date_check)
        no_abstract_check, abstract = check_abstracts(paper, i, no_abstract_check)

        if no_author_check == False:
            if no_title_check == False:
                if no_date_check == False:
                    if no_abstract_check == False:
                        fill_db(ids[i], title, abstract, names, date, id_name)
                        pass
                    else:
                        print("Test failed on abstract")
                else:
                    print("Test failed on date")
            else:
                print("Test failed on title")
        else:
            print("Test failed on author")


def check_authors(paper, i, noAuthorCheck):
    """
    Checks if authors are present in the paper details.

    Args:
        paper (dict): Paper details.
        i (int): Index of the paper.
        noAuthorCheck (bool): Flag indicating the presence of authors.

    Returns:
        tuple: A tuple containing the updated flag indicating the presence of authors and the authors' names.
    """
    noAuthorCheck = True
    try:
        authors = paper['MedlineCitation']['Article']['AuthorList']
        author_names = [
            author.get('LastName', '') + ' ' + author.get('ForeName', '')
            for author in authors]
        author_list = ', '.join(author_names)
        names = "{}".format(author_list)
        noAuthorCheck = False
    except KeyError:
        names = "{}) {}".format(i + 1, "No authors")

    return noAuthorCheck, names


def check_titles(paper, i, noTitleCheck):
    """
    Checks if a title is present in the paper details.

    Args:
        paper (dict): Paper details.
        i (int): Index of the paper.
        noTitleCheck (bool): Flag indicating the presence of a title.

    Returns:
        tuple: A tuple containing the updated flag indicating the presence of a title and the title itself.
    """
    noTitleCheck = True
    try:
        title = "{}".format(paper['MedlineCitation']['Article']['ArticleTitle'])
        noTitleCheck = False
    except KeyError:
        title = "{}) {}".format(i + 1, "No title")

    return noTitleCheck, title


def check_dates(paper, i, noDateCheck):
    """
    Checks if a publication date is present in the paper details.

    Args:
        paper (dict): Paper details.
        i (int): Index of the paper.
        noDateCheck (bool): Flag indicating the presence of a date.

    Returns:
        tuple: A tuple containing the updated flag indicating the presence of a date and the date itself.
    """
    noDateCheck = True
    try:
        pub_date = paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']
        year = pub_date.get('Year', '')
        month = pub_date.get('Month', '')
        day = pub_date.get('Day', '')
        if year and month and day:
            date_str = f"{year}-{month}-{day}"
        elif year and month:
            date_str = f"{year}-{month}"
        elif year:
            date_str = f"{year}"
        else:
            date_str = "No date"
        date = f"{date_str}"
        noDateCheck = False
    except KeyError:
        date = f"{i + 1}) No date"

    return noDateCheck, date


def check_abstracts(paper, i, noAbstractCheck):
    """
    Checks if an abstract is present in the paper details.

    Args:
        paper (dict): Paper details.
        i (int): Index of the paper.
        noAbstractCheck (bool): Flag indicating the presence of an abstract.

    Returns:
        tuple: A tuple containing the updated flag indicating the presence of an abstract and the abstract itself.
    """
    noAbstractCheck = True

    try:
        noAbstractCheck = False
        abstract = paper['MedlineCitation']['Article']['Abstract']['AbstractText']
    except KeyError:
        print("{}".format("No abstract"))
        abstract = "No abstract"

    return noAbstractCheck, abstract


def fill_db(id, title, abstract, names, date, id_names):
    """
    Inserts data into the database.

    Args:
        id (int): The PubMed ID of the article.
        title (str): The title of the article.
        abstract (str): The abstract of the article.
        names (str): The authors of the article.
        date (str): The publication date of the article.
        id_names (str): The ID names containing keyword information.

    Returns:
        None
    """
    link = "https://pubmed.ncbi.nlm.nih.gov/{}/".format(id)
    try:
        id_name = regex.search(r"\((.*)\)", id_names).group(1).replace("\'", "").split(", ")
        keys = tuple(id_name)
        query = "select keyword_ID from Keywords where keyword in {}".format(keys)
    except AttributeError:
        id_name = regex.search("ID's (.*):", id_names).group(1).replace("\'", "")
        query = "select keyword_ID from Keywords where keyword = '{}'".format(id_name)

    content = cur.execute(query).fetchall()

    cur.execute(
        "INSERT INTO Articles (title, abstract, links, pubmed_id, authors, dates) VALUES (?, ?, ?, ?, ?, ?)",
        (str(title), str(abstract), str(link), id, str(names), str(date)))

    cur.execute("SELECT MAX(article_ID) AS last_id FROM Articles")
    last_id = cur.fetchone()

    for j in content:
        cur.execute(
            "insert into Articles_Keywords (Articles_article_ID, Keywords_keyword_ID) values (?, ?)",
            (int(last_id[0]), int(j[0])))

    con.commit()


def create_db_tables():
    """
    Executes SQL statements to create the required database tables.

    Returns:
        None
    """
    cur.execute("""
        -- Table: Articles
        CREATE TABLE Articles (
            article_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            title varchar(100) NOT NULL,
            abstract varchar(10000) NOT NULL,
            links varchar(50) NOT NULL,
            pubmed_id varchar(20) NOT NULL,
            authors varchar(250) NOT NULL,
            dates varchar(20) NOT NULL
        );
    """)
    cur.execute("""
        -- Table: Articles_Keywords
        CREATE TABLE Articles_Keywords (
            Articles_article_ID integer NOT NULL,
            Keywords_keyword_ID integer NOT NULL,
            CONSTRAINT Articles_Keywords_pk PRIMARY KEY (Articles_article_ID,Keywords_keyword_ID),
            CONSTRAINT Articles_Keywords_Articles FOREIGN KEY (Articles_article_ID)
            REFERENCES Articles (article_ID),
            CONSTRAINT Articles_Keywords_Keywords FOREIGN KEY (Keywords_keyword_ID)
            REFERENCES Keywords (keyword_ID)
        );
    """)
    cur.execute("""
        -- Table: Keywords
        CREATE TABLE Keywords (
            keyword_ID integer NOT NULL CONSTRAINT Keywords_pk PRIMARY KEY,
            keyword varchar(50) NOT NULL
        );
    -- End of file.
    """)


def fill_keywords():
    """
    Fills the Keywords table in the database with keywords from input files.

    Returns:
        None
    """
    file = "gene_keywords"
    file2 = "key_words"
    count = 0

    with open(file) as data:
        for line in data:
            count += 1
            cur.execute("INSERT INTO Keywords (keyword_ID, keyword) VALUES (?, ?)",
                        (int(count), str(line.strip())))

    with open(file2) as data2:
        for line2 in data2:
            count += 1
            cur.execute("INSERT INTO Keywords (keyword_ID, keyword) VALUES (?, ?)",
                        (int(count), str(line2.strip())))

    con.commit()


if __name__ == '__main__':
    create_db_tables()
    fill_keywords()
    File = "output.txt"
    openen(File)
