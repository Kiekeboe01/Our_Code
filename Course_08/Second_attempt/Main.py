import Data_gathering


def hello_welcome():
    print("Welcome to the new and improved Course 08 application."
          "\nThis code consists out of 5 steps:"
          "\n1. Data gathering"
          "\n2. Pre-processing"
          "\n3. Processing"
          "\n4. Analysis"
          "\n5. Visualization")
    questionnaire()


def questionnaire():
    print("\n\nIf you have any questions about any of the steps,"
          " type the corresponding number."
          "\nIf you would like to continue to step 1, press enter")
    preform_next_step = input()
    next_step(preform_next_step)


def next_step(preform_next_step):
    if preform_next_step == '1':
        print('\nGathers all the ids of articles witch we might find '
              'interesting using the keywords in a already specified '
              'folder <NAME HERE>.And sends them to step 2.')
        another_question = input('Would you like to know more?\t(y/n)\n')
        if another_question.lower() == 'y':
            questionnaire()
        else:
            Data_gathering.gather_main()

    elif preform_next_step == '2':
        print('\nTakes all the ids and removes the stop words and stems '
              'all the words. From all the articles. And sends them to step 3')
        another_question = input('Would you like to know more?\t(y/n)\n')
        if another_question.lower() == 'y':
            questionnaire()
        else:
            Data_gathering.gather_main()

    elif preform_next_step == '3':
        print('\nTakes the stemmed articles and does a co-occurrence based '
              'type of textmineing. And sends them to step 4')
        another_question = input('Would you like to know more?\t(y/n)\n')
        if another_question.lower() == 'y':
            questionnaire()
        else:
            Data_gathering.gather_main()

    elif preform_next_step == '4':
        print('\nTO BE SPECIFIED')
        another_question = input('Would you like to know more?\t(y/n)\n')
        if another_question.lower() == 'y':
            questionnaire()
        else:
            Data_gathering.gather_main()

    elif preform_next_step == '5':
        print('\nRepresents the found results in the website.')
        another_question = input('Would you like to know more?\t(y/n)\n')
        if another_question.lower() == 'y':
            questionnaire()
        else:
            Data_gathering.gather_main()
    else:
        Data_gathering.gather_main()


if __name__ == '__main__':
    # Data Gathering
    # Gathers all the id's of articles witch we might find interesting.

    # Pre processing
    # Takes all the id's and removes stop words and stems all the words.

    # Processing
    # Takes the stemmed files and does a co-occurence based type of textmineing

    # Analasis
    # Website?

    # Visulization
    # Represent the found results in the website.

    hello_welcome()
