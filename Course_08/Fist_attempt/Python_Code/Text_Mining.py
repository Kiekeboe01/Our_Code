import sqlite3
import re
import json

from collections import defaultdict
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


def keyword_retrieval():
    """
    Retrieves keywords from the 'textmine_keywords' file.

    Returns:
        set: A set of keywords.
    """
    print("Opening keyword file")
    # Opens the file textmine_keywords and reads it line by line
    with open('textmine_keywords', 'r') as file1:
        keywords = set(line.strip() for line in file1)

    return keywords


def open_database():
    """
    Retrieves abstracts from the 'db_twinning.db' database.

    Retrieves abstracts from the 'Articles' table in the 'db_twinning.db' database.
    Processes the retrieved abstracts by stemming and printing them.

    Returns:
        None
    """
    print("\nRetrieving abstracts from database")
    # Connect to the database
    conn = sqlite3.connect('db_twinning.db')
    cursor = conn.cursor()

    cursor.execute('SELECT abstract FROM Articles')

    # Fetch all the results as a list of tuples
    results = cursor.fetchall()

    limit = 0
    # Process the results
    for row in results:
        column_data = row[0]
        if limit < 50:
            limit += 1
            print("\nArticle nr: ", limit)
            print(str(column_data))
            stemming(str(column_data))

    # Close the cursor and the database connection
    cursor.close()
    conn.close()
    return


def stemming(abstract):
    """
    Performs stemming on the given abstract.

    Args:
        abstract (str): The abstract to be stemmed.

    Returns:
        None
    """
    print("Stemming the abstract")

    # Convert the abstract to lowercase
    abstract = abstract.lower()

    # Removing all non-word-like symbols
    abstract = re.sub(r'[^\w\s]', '', abstract)

    # Tokenization
    tokens = word_tokenize(abstract)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in tokens]

    keyword_in_abstract(stemmed_tokens, keywords)
    return


def keyword_in_abstract(stemmed_tokens, regex):
    """
    Retrieves keywords from the stemmed tokens in the abstract.

    Args:
        stemmed_tokens (list): List of stemmed tokens from the abstract.
        regex (set): Set of relevant keyword regular expressions.

    Returns:
        None
    """
    print("Retrieving keywords from abstract...")
    # Define relevant keywords using regular expressions
    relevant_keywords_regex = regex

    # Search for papers containing the keywords
    papers_containing_keywords = []

    # Convert the relevant keywords into regular expression patterns
    patterns = [re.compile(regex) for regex in relevant_keywords_regex]

    # Iterate over the tokens
    for i in range(len(stemmed_tokens)):
        for pattern in patterns:
            if pattern.match(stemmed_tokens[i]):
                # If the current token matches the pattern
                # Add the corresponding paper or document to the list
                papers_containing_keywords.append(stemmed_tokens[i])

    window_size = 10
    co_occurrence(stemmed_tokens, window_size, papers_containing_keywords)
    return


def co_occurrence(words, window_size, keywords_in_abstract):
    """
    Creates a co-occurrence matrix based on the given words and window size.

    Args:
        words (list): List of words in the abstract.
        window_size (int): Size of the co-occurrence window.
        keywords_in_abstract (list): List of keywords present in the abstract.

    Returns:
        None
    """
    print("Making co-occurrence matrix...")
    co_occurrence_matrix = defaultdict(lambda: defaultdict(int))

    # Iterate over each word in the sentence
    for i in range(len(words)):
        target_word = words[i]
        # Iterate over the words within the specified window size
        for j in range(i - window_size, i + window_size + 1):
            if j != i and j >= 0 and j < len(words):
                context_word = words[j]
                co_occurrence_matrix[target_word][context_word] += 1

    print("Done")
    for key in keywords_in_abstract:
        matrix_making(key, co_occurrence_matrix)
    return


def matrix_making(target_word, co_occurrence_matrix):
    """
    Fills the matrix dictionary based on the target word and co-occurrence matrix.

    Args:
        target_word (str): Target word from the co-occurrence matrix.
        co_occurrence_matrix (defaultdict): Co-occurrence matrix containing word counts.

    Returns:
        None
    """
    for context_word, count in co_occurrence_matrix[target_word].items():
        matrix_dictionary[target_word][context_word] += count
    return


def file_filling(matrix_dictionary):
    """
    Fills the JSON and text files with the matrix dictionary.

    Args:
        matrix_dictionary (defaultdict): Co-occurrence matrix dictionary.

    Returns:
        None
    """
    print("\nFilling the JSON file")
    # Define the path to the file where you want to save the dictionary
    json_file_path = 'Text_Mining_Test.json'
    text_file_path = 'Text_Mining_Test.txt'

    # Save the dictionary to a file
    with open(json_file_path, 'w') as file:
        json.dump(matrix_dictionary, file)

    with open(text_file_path, 'w') as file:
        for key, value in matrix_dictionary.items():
            data = {key: value}
            json.dump(data, file)
            file.write('\n')
    return


if __name__ == '__main__':
    # Opens keyword_retrieval for all the keywords
    keywords = keyword_retrieval()
    print(keywords)

    # Opens the open_database function and makes a matrix for the next function
    matrix_dictionary = defaultdict(lambda: defaultdict(int))
    open_database()

    # A function for writing the matrix to a JSON file
    file_filling(matrix_dictionary)
