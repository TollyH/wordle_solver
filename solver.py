import random
import string


def get_word_list(path: str = "wordlist.txt") -> list[str]:
    with open(path, encoding="utf8") as word_file:
        return word_file.read().strip().splitlines()


def get_letter_counts(word_list: list[str]) -> dict[str, list[int]]:
    """
    Get the number of times each letter of the alphabet appears in each
    position of every word in the word list.
    """
    counts = {c: [0, 0, 0, 0, 0] for c in string.ascii_lowercase}
    for word in word_list:
        for i, c in enumerate(word):
            counts[c][i] += 1
    return counts


def score_word(word: str, letter_counts: dict[str, list[int]]):
    score = 0
    for i, c in enumerate(word):
        score += letter_counts[c][i]
    return score


def get_possible_words(word_list: list[str], possible_letters: list[set[str]],
                       min_letter_count: dict[str, int],
                       max_letter_count: dict[str, int]) -> list[str]:
    """
    Get a list of all possible words based on the current state of the game.

    possible_letters is a list of possible characters for each character in the
    word.

    min_letter_count and max_letter_count are the minimum and maximum number of
    times each letter in the alphabet must appear.
    """
    if len(possible_letters) != 5:
        raise ValueError("possible_letters must contain 5 items.")
    possible_words: list[str] = []
    for word in word_list:
        possible = True
        for i, c in enumerate(word):
            if c not in possible_letters[i]:
                possible = False
                break
        for letter in string.ascii_lowercase:
            letter_count = word.count(letter)
            if letter_count < min_letter_count[letter]:
                possible = False
                break
            if letter_count > max_letter_count[letter]:
                possible = False
                break
        if possible:
            possible_words.append(word)
    return possible_words


def main() -> None:
    word_list = get_word_list()
    # Shuffle the word list so that words with the same score will be decided
    # randomly
    random.shuffle(word_list)
    letter_counts = get_letter_counts(word_list)
    possible_letters = [set(string.ascii_lowercase) for _ in range(5)]
    min_letter_count = {c: 0 for c in string.ascii_lowercase}
    max_letter_count = {c: 5 for c in string.ascii_lowercase}
    while True:
        possible_words = get_possible_words(
            word_list, possible_letters, min_letter_count, max_letter_count
        )
        if len(possible_words) == 0:
            print(
                "\nThere are no possible words. "
                "Are you sure you entered the results correctly and used the "
                "recommended words?"
            )
            break
        best_word = max(
            possible_words, key=lambda w: score_word(w, letter_counts)
        )
        if len(possible_words) == 1:
            print(f"\nThe word must be: {best_word.upper()}")
            break
        print(
            f"\nTry this word: {best_word.upper()}\n"
            f"({len(possible_words)} possible words remaining)"
        )
        result = input(
            "Enter result (Y = green, ? = amber, or N = grey, e.g. YYN?N) > "
        )
        success = True
        if len(result) != 5:
            print("Incorrect length. Try again.")
            success = False
        else:
            if not set(result).issubset({'Y', 'N', '?'}):
                print("Invalid character. Try again.")
                success = False
            else:
                min_letter_count = {c: 0 for c in string.ascii_lowercase}
                max_letter_count = {c: 5 for c in string.ascii_lowercase}
                for i, c in enumerate(result.upper()):
                    word_c = best_word[i]
                    if c == 'Y':
                        # Character must be this letter
                        possible_letters[i] = {word_c}
                        min_letter_count[word_c] += 1
                    elif c == '?':
                        # Character cannot be this letter,
                        # but it is in the word
                        possible_letters[i].discard(word_c)
                        min_letter_count[word_c] += 1
                    elif c == 'N':
                        # Character cannot be this letter
                        # and it cannot appear any more times than it has
                        # been accepted
                        possible_letters[i].discard(word_c)
                        # Use -1 to flag that the value needs to be filled
                        max_letter_count[word_c] = -1
        if success:
            for letter, max_count in max_letter_count.items():
                if max_count != -1:
                    continue
                max_letter_count[letter] = min_letter_count[letter]


if __name__ == "__main__":
    main()
