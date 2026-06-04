"""Finds all sub-anagrams of a given word from a word list.

Word list: https://github.com/dwyl/english-words/blob/master/words.txt

Problem: Given file containing words. User enters a target word. Goal is to return CLI output of all words that are either full or sub-anagrams of target word.

Example:
    $ python3 jumble_solver.py word_list.txt dog
    god
    go
    do

Idea:
    - Create a freq array of size 26 for the target word. Each index in array corresponds to ch (a–z).
    - For every word read from the word list file (once it's been normalized), build its freq counter and compare against the target freq counter.
    - If count of any letter in the word array exceeds the target, skip it.
    - Otherwise, print the word.
    - Optimization: skip any word longer than target word.

Time and Space Complexity:
    N = number of words in the text file
    L = word length
    TC: O(N * L): Every word is read, a freq counter of L chs is
        built and compared against the freq input counter.
    SC: O(1) only 2 fixed-size freq arrays (of size 26 chs) are kept in
        memory. The word list is streamed line-by-line. No
        additional storage needed.
"""

import sys


def build_word_freq(word: str) -> list[int]:
    """Build a character frequency arr for the parameter word.

    Args:
        word: A lowercase alpha str.

    Returns:
        A list of 26 ints. Index 0 = 'a', index 25 = 'z'.
    """
    freqs = [0] * 26
    for c in word:
        freqs[ord(c) - ord('a')] += 1
    return freqs


def is_sub_anagram(word_freq: list[int], input_freq: list[int]) -> bool:
    """Determine if word_freq is a sub-anagram of input_freq.

    A sub-anagram uses some or all of the available letters. Each letter
    in the word can't appear more times than it does in the input.

    Args:
        word_freq: Frequency array of the read word.
        input_freq: Frequency array of the user's input word.

    Returns:
        True if the word is a sub-anagram of the input word.
    """
    for i in range(26):
        if word_freq[i] > input_freq[i]:
            return False
    return True


def find_words(file_path: str, input_word: str, input_freq: list[int]) -> None:
    """Stream every word from the text file and print every valid sub-anagram.

    Args:
        file_path: Path to a text file. Has one word per line.
        input_word: The normalized input word given by the user.
        input_freq: Frequency array of the input word.
    """
    with open(file_path) as f:
        for line in f:
            comparison_word = line.strip().lower()

            if not comparison_word or not comparison_word.isalpha():
                continue

            if len(comparison_word) > len(input_word):
                continue

            word_freq = build_word_freq(comparison_word)

            if is_sub_anagram(word_freq, input_freq):
                print(comparison_word)


def main() -> None:
    """Validate input arguments and run the algorithm."""
    if len(sys.argv) != 3:
        print("Format must be: python3 jumble_solver.py <word_list_path> <jumbled_word>")
        sys.exit(1)

    file_path = sys.argv[1]
    input_word = sys.argv[2].lower()

    if not file_path:
        print("Missing file path")
        sys.exit(1)

    if not input_word.isalpha():
        print("Word must contain only letters")
        sys.exit(1)

    input_freq = build_word_freq(input_word)
    find_words(file_path, input_word, input_freq)


if __name__ == "__main__":
    main()
