from Bio import Entrez
import time


def read_file():
    """
    Reads the file 'main_keywords' and 'Combi_keywords' to retrieve keywords and performs Entrez searches for each keyword.

    Returns:
        dict: Dictionary containing keywords as keys and their corresponding ID lists.
    """
    with open('main_keywords', 'r') as file1:
        list_one = set(line.strip() for line in file1)

    with open('Combi_keywords', 'r') as file2:
        list_two = set(line.strip() for line in file2)

    total_single = 0
    for i in list_one:
        id_list, hits = single_entrez_search(i)
        keywords[i] = id_list
        total_single += hits

    total_multiple = 0
    for x in list_one:
        for y in list_two:
            id_list, hits = multiple_entrez_search(x, y)
            keywords[x, y] = id_list
            total_multiple += hits

    print("Total number of hits for single search: ", total_single)
    print("Total number of hits for multiple search: ", total_multiple)
    print("Total hits for all searches: ", total_single + total_multiple)
    return keywords


def single_entrez_search(keyword):
    """
    Performs a single Entrez search for a keyword.

    Args:
        keyword (str): Keyword to search.

    Returns:
        tuple: A tuple containing the filtered ID list and the number of hits.
    """
    Entrez.email = "xander.te.winkel@hotmail.com"
    print("Searching hits for: " + keyword)
    term = f"{keyword}[KYWD]"
    start_time = time.time()
    handle = Entrez.esearch(db="pubmed", term=term, retmax=999999999)
    record = Entrez.read(handle)
    end_time = time.time()
    total_time = end_time - start_time
    hits = len(record["IdList"])
    print("Number of hits:", hits)
    print("Execution time: {:.2f} seconds\n".format(total_time))
    return filterIDs(record["IdList"]), hits


def multiple_entrez_search(keyword_01, keyword_02):
    """
    Performs a multiple Entrez search for a combination of keywords.

    Args:
        keyword_01 (str): First keyword to search.
        keyword_02 (str): Second keyword to search.

    Returns:
        tuple: A tuple containing the filtered ID list and the number of hits.
    """
    if keyword_01 != keyword_02:
        Entrez.email = "xander.te.winkel@hotmail.com"
        print("Searching hits for: " + keyword_01 + " and " + keyword_02)
        term = f"{keyword_01}[KYWD] AND {keyword_02}[KYWD]"
        start_time = time.time()
        handle = Entrez.esearch(db="pubmed", term=term, retmax=999999999)
        record = Entrez.read(handle)
        end_time = time.time()
        total_time = end_time - start_time
        hits = len(record["IdList"])
        print("Number of hits:", hits)
        print("Execution time: {:.2f} seconds\n".format(total_time))
        return filterIDs(record["IdList"]), hits


def filterIDs(idlist):
    """
    Filters the list of IDs to remove duplicates.

    Args:
        idlist (list): List of IDs.

    Returns:
        list: List of unique IDs.
    """
    unique_ids = []
    for i in idlist:
        if i not in unique_ids:
            unique_ids.append(i)
    return unique_ids


def write_file(keywords):
    """
    Writes the keywords and their corresponding ID lists to a file.

    Args:
        keywords (dict): Dictionary containing keywords as keys and their corresponding ID lists.
    """
    with open('output.txt', 'w') as file:
        for keyword, id_list in keywords.items():
            file.write(f"\n<ID's {keyword}:\n")
            file.write(f"{id_list}\n")
            file.write(f"Lenght list: {len(id_list)}\n")


if __name__ == '__main__':
    keywords = {}
    keywords = read_file()
    write_file(keywords)
    print("End of code")
