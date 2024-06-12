import re
import json
import time
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

# Load data from JSON file


def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)['successful_tracks']


data = load_data('data.json')


def preprocess(text):
    # Original text for exact matching
    original_text = text.lower()

    # Cleaned text
    cleaned_text = text.lower()
    cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # remove punctuation
    original_text = re.sub(r'[^\w\s]', '', cleaned_text)
    cleaned_text = re.sub(r'\d+', '', cleaned_text)  # remove numbers
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(cleaned_text)  # tokenize
    tokens = [word for word in tokens if word not in stopwords.words(
        'english')]  # remove stopwords
    cleaned_text = ' '.join(tokens)

    return original_text, cleaned_text


# Adjust the preprocess call in your main implementation as well
for track in data:
    original, cleaned = preprocess(track['lyrics'])
    track['original_lyrics'] = original
    track['cleaned_lyrics'] = cleaned


# Function to get user input


def get_user_input():
    return input("Enter the lyrics fragment to search for: ").lower()

# Knuth-Morris-Pratt (KMP) Algorithm


def computeLPSArray(pattern):
    M = len(pattern)
    lps = [0] * M
    length = 0
    i = 1
    while i < M:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def KMP_search(pattern, text):
    M = len(pattern)
    N = len(text)
    lps = computeLPSArray(pattern)
    i = j = 0
    results = []
    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == M:
            results.append(i - j)
            j = lps[j - 1]
        elif i < N and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return results

# Brute Force Algorithm


def brute_force_search(pattern, text):
    M = len(pattern)
    N = len(text)
    results = []
    for i in range(N - M + 1):
        j = 0
        while j < M and text[i + j] == pattern[j]:
            j += 1
        if j == M:
            results.append(i)
    return results

# Boyer-Moore Algorithm


def bad_character_table(pattern):
    table = {}
    for i in range(len(pattern) - 1):
        table[pattern[i]] = len(pattern) - i - 1
    return table


def boyer_moore_search(pattern, text):
    M = len(pattern)
    N = len(text)
    if M > N:
        return []

    bad_char_table = bad_character_table(pattern)
    s = 0
    results = []
    while s <= N - M:
        j = M - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            results.append(s)
            s += M
        else:
            s += max(1, bad_char_table.get(text[s + j], M))
    return results

# Regex Search Function


def regex_search(pattern, text):
    return bool(re.search(pattern, text, re.IGNORECASE))


def find_songs(fragment, data, search_function):
    results = []
    start_time = time.time()
    for track in data:
        if search_function(fragment, track['original_lyrics']):
            results.append(track)
    end_time = time.time()
    return results, end_time - start_time


def display_results(results, algorithm_name, search_time):
    print(f"Algorithm: {algorithm_name}")
    print(f"Search Time: {search_time:.4f} seconds")
    if not results:
        print(f"No matches found using {algorithm_name}.")
    else:
        for track in results:
            print(
                f"Track: {track['track_name']}, Artist: {track['artist_name']}, "
                f"Album: {track['album_name']}, Release Date: {track['release_date']}, "
                f"Genres: {', '.join(track['genres'])}, Spotify URL: {track['spotify_url']}"
            )
    print("\n")


# Main Execution
if __name__ == "__main__":
    fragment = get_user_input()

    kmp_results, kmp_time = find_songs(fragment, data, KMP_search)
    brute_force_results, brute_force_time = find_songs(
        fragment, data, brute_force_search)
    boyer_moore_results, boyer_moore_time = find_songs(
        fragment, data, boyer_moore_search)
    regex_results, regex_time = find_songs(fragment, data, regex_search)

    # Display results from any one algorithm (they should be the same)
    display_results(kmp_results, "KMP Algorithm", kmp_time)

    # Show efficiency of all algorithms
    print("Efficiency Comparison:")
    print(f"KMP Algorithm: {kmp_time:.4f} seconds")
    print(f"Brute Force Algorithm: {brute_force_time:.4f} seconds")
    print(f"Boyer-Moore Algorithm: {boyer_moore_time:.4f} seconds")
    print(f"Regex Search: {regex_time:.4f} seconds")
