import time
import re

# NOTE: The logic below has been updated to use simple string splitting 
# and counting based on the user's provided functions, which are less 
# robust than the original regex methods (e.g., they include punctuation 
# attached to words and only count three types of terminal punctuation).

def count_words(text: str) -> int:
    """Counts the total number of words in the text using simple splitting."""
    # This considers any whitespace-separated token a "word."
    words = text.split()
    return len(words)

def count_sentences(text: str) -> int:
    """Counts the total number of sentences based on terminal punctuation marks."""
    return text.count('.') + text.count('!') + text.count('?')

def find_longest_shortest_words(text: str) -> tuple[str, str]:
    """
    Finds the longest and shortest words using simple splitting.
    Punctuation remains attached to the words.
    """
    words = text.split()

    if not words:
        return "", ""

    # Longest word based on len()
    longest = max(words, key=len)

    # Shortest word based on len()
    shortest = min(words, key=len)

    return longest, shortest

def get_analysis_results(text: str) -> tuple[dict, float]:
    """
    Combines all updated analysis functions into a single result dictionary 
    and returns the server execution time for the analysis phase.
    """
    start_time = time.time()
    
    longest_word, shortest_word = find_longest_shortest_words(text)

    results = {
        "word_count": count_words(text),
        "sentence_count": count_sentences(text),
        "longest_word": longest_word,
        "shortest_word": shortest_word,
    }
    
    end_time = time.time()
    server_time = end_time - start_time
    
    return results, server_time