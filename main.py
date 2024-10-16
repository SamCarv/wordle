from rich.console import Console
from random import randint
import os
import re
import unicodedata

console = Console()

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()

new_letters = [f"[bold white]{x}" for x in letters]


def remove_accent(string: str):
    normalized = unicodedata.normalize("NFD", string)
    return re.sub(r"[\u0300-\u036f]", "", normalized).casefold()


def guess_word():
    list_words = [""]

    with open("words.txt", "r") as file:
        for line in file:
            list_words.append(line)

    return list_words[randint(0, len(list_words) - 1)].strip()


def check_word(word: str, word_guessed: str):
    new_word = ""

    word_guessed_without_accent = remove_accent(word_guessed)

    for idx, i in enumerate(word):
        if (
            word[idx] == word_guessed[idx]
            or word[idx] == word_guessed_without_accent[idx]
        ):
            new_word += f"[bold green]{word_guessed[idx]}"
            change_letter(f"[bold green]{i}")
        elif i in word_guessed or i in word_guessed_without_accent:
            new_word += f"[bold yellow]{i}"
            change_letter(f"[bold yellow]{i}")
        elif i not in word_guessed or i not in word_guessed_without_accent:
            new_word += f"[bold red]{i}"
            change_letter(f"[bold red]{i}")

    return new_word


def change_letter(letter: str, list_letters: list[str] = new_letters):
    only_letter = letter.split("]")[1]

    for idx, i in enumerate(list_letters):
        if only_letter == i.split("]")[1]:
            new_letters[idx] = letter


def check_win(word: str, word_guessed: str):
    if word == word_guessed or word == remove_accent(word_guessed):
        return True
    else:
        return False


def game():
    word_guessed = guess_word()

    _ = os.system("clear")
    attempts = 6
    guess = 1
    words: list[str] = []

    while guess <= attempts:

        console.rule(f"✨ Guess {guess} ✨")

        for i in range(0, attempts):
            if i < len(words):
                console.print(words[i], justify="center")
            else:
                console.print("_____", justify="center")

        print()

        new_abc = " ".join(x for x in new_letters)
        console.print(new_abc, justify="center")

        print()

        while True:
            word_temp = input("Adivinhe a palavra: ").lower()

            if len(word_temp) == 5 and word_temp.isalpha():
                break

            console.print("Use palavras de 5 letras.")

        words.append(check_word(word_temp, word_guessed))

        if check_win(word_temp, word_guessed):
            console.print(
                f"Correto, a palavra era {word_guessed}",
                style="bold green",
            )
            break

        guess += 1

    if guess >= attempts:
        print(f"A palavra era {word_guessed}")


if __name__ == "__main__":
    game()
