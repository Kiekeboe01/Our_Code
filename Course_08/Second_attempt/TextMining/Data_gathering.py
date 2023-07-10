import time

from Bio import Entrez


def gather_main():
    gene_list, term_list = read_file()
    print("\nGene List:")
    print(gene_list)
    print("\nTerm List:")
    print(term_list)

    keyword_id_list = send_to_search(gene_list, term_list)
    for i in keyword_id_list:
        print('Keyword used for the list of ids: ' + str(i))
        print('List of ids', keyword_id_list[i])
        print('Lenght of the list of ids: ', len(keyword_id_list[i]), '\n')


def read_file():
    print('Reading file containing keywords...')

    gene_list = []
    term_list = []

    with open('KeyWords', 'r') as file:
        read_genes = False
        read_terms = False

        for line in file:
            line = line.strip()

            if line == ">GENES":
                read_genes = True
                read_terms = False
                continue
            elif line == ">TERMS":
                read_genes = False
                read_terms = True
                continue

            if read_genes:
                gene_list.append(line)
            elif read_terms:
                term_list.append(line)

    return gene_list, term_list


def send_to_search(gene_list, term_list):
    print()
    keyword_id_list = {}

    total_hits_single = 0
    for i in gene_list:
        id_list, hits = entrez_search(i)
        keyword_id_list[i] = id_list
        total_hits_single += hits

    total_hits_multiple = 0
    for x in gene_list:
        for y in term_list:
            id_list, hits = double_entrez_search(x, y)
            keyword_id_list[x, ' plus ', y] = id_list
            total_hits_single += hits

    print("Total number of hits for single search: ", total_hits_single)
    print("Total number of hits for multiple search: ", total_hits_multiple)
    print("Total hits for all searches: ",
          total_hits_single + total_hits_multiple, '\n')

    return keyword_id_list


def entrez_search(keyword):
    Entrez.email = "xander.te.winkel@hotmail.com"
    print("Searching hits for: " + keyword)

    term = f"{keyword}[KYWD]"
    start_time = time.time()

    handle = Entrez.esearch(db="pubmed", term=term, retmax=999999999)
    record = Entrez.read(handle)

    end_time = time.time()
    total_time = end_time - start_time

    print("Execution time: {:.2f} seconds\n".format(total_time))
    hits = len(record["IdList"])
    return record["IdList"], hits


def double_entrez_search(keyword_01, keyword_02):
    if keyword_01 != keyword_02:
        Entrez.email = "xander.te.winkel@hotmail.com"
        print("Searching hits for: " + keyword_01 + " and " + keyword_02)

        term = f"{keyword_01}[KYWD] AND {keyword_02}[KYWD]"
        start_time = time.time()

        handle = Entrez.esearch(db="pubmed", term=term, retmax=999999999)
        record = Entrez.read(handle)

        end_time = time.time()
        total_time = end_time - start_time

        print("Execution time: {:.2f} seconds\n".format(total_time))
        hits = len(record["IdList"])
        return record["IdList"], hits

