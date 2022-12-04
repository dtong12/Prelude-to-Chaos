



#testing everything else afterwards....






#take all of these live games....
#cross compare them against each other 


#we end up just storing the entire string behind it....




#may be one profile per sport.
    #draftkings has 

#sport
#still have to match the event_name/tournament name at least 




#average out the lines that have a very high match rate

#only show feeds for 4 same line matches or more




import spacy
from itertools import combinations


# Set globals
nlp = spacy.load("en_core_web_md")

def pre_process(titles):
    """
    Pre-processes titles by removing stopwords and lemmatizing text.
    :param titles: list of strings, contains target titles,.
    :return: preprocessed_title_docs, list containing pre-processed titles.
    """

    # Preprocess all the titles
    title_docs = [nlp(x) for x in titles]
    preprocessed_title_docs = []
    lemmatized_tokens = []
    for title_doc in title_docs:
        for token in title_doc:
            if not token.is_stop:
                lemmatized_tokens.append(token.lemma_)
        preprocessed_title_docs.append(" ".join(lemmatized_tokens))
        del lemmatized_tokens[
            :
            ]  # empty the lemmatized tokens list as the code moves onto a new title

    return preprocessed_title_docs

def similarity_filter(titles):
    """
    Recursively check if titles pass a similarity filter.
    :param titles: list of strings, contains titles.
    If the function finds titles that fail the similarity test, the above param will be the function output.
    :return: this method upon itself unless there are no similar titles; in that case the feed that was passed
    in is returned.
    """

    # Preprocess titles
    preprocessed_title_docs = pre_process(titles)

    # Remove similar titles
    all_summary_pairs = list(combinations(preprocessed_title_docs, 2))
    similar_titles = []
    for pair in all_summary_pairs:
        title1 = nlp(pair[0])
        title2 = nlp(pair[1])
        similarity = title1.similarity(title2)
        if similarity > 0.8:
            similar_titles.append(pair)

    titles_to_remove = []
    for a_title in similar_titles:
        # Get the index of the first title in the pair
        index_for_removal = preprocessed_title_docs.index(a_title[0])
        titles_to_remove.append(index_for_removal)

    # Get indices of similar titles and remove them
    similar_title_counts = set(titles_to_remove)
    similar_titles = [
        x[1] for x in enumerate(titles) if x[0] in similar_title_counts
    ]

    # Exit the recursion if there are no longer any similar titles
    if len(similar_title_counts) == 0:
        return titles

    # Continue the recursion if there are still titles to remove
    else:
        # Remove similar titles from the next input
        for title in similar_titles:
            idx = titles.index(title)
            titles.pop(idx)
            
        return similarity_filter(titles)

if __name__ == "__main__":
    your_title_list = ['title1', 'title2']
    similarty_filter(your_title_list)


