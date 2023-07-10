import json

def get_highest_count_term(terms):
    """
    Finds the highest count term and its count in a dictionary of terms.

    Args:
        terms (dict): Dictionary of terms with their respective counts.

    Returns:
        tuple: A tuple containing the highest count and corresponding term.
    """
    highest_count = 0
    highest_count_term = None
    # Initialize variables to keep track of the highest count and corresponding term.

    for term, count in terms.items():
        if count > highest_count:
            highest_count = count
            highest_count_term = term
        # Iterate through the terms dictionary and update the highest count
        # and term if a higher count is found.

    return highest_count, highest_count_term
    # Return the highest count and corresponding term as a tuple.

if __name__ == '__main__':
    highest_count_terms = {}
    # Initialize an empty dictionary to store the highest count terms for each category.

    for category, terms in data.items():
        highest_count, highest_count_term = get_highest_count_term(terms)
        # Call the get_highest_count_term() function to find the highest count
        # term and its count for the current category.

        highest_count_terms[category] = (highest_count, highest_count_term)
        # Store the highest count and term as a tuple in the
        # highest_count_terms dictionary with the category as the key.

    sorted_terms = sorted(highest_count_terms.items(), key=lambda x: x[1][0],
                          reverse=True)
    # Sort the items in the highest_count_terms dictionary based on the
    # count in descending order.

    for category, (count, term) in sorted_terms:
        print(
            f"Category: '{category}', Highest count term: '{term}', Count: {count}")
        # Iterate through the sorted terms and print the category, highest
        # count term, and count in a formatted manner.
