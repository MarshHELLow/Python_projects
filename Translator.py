from bs4 import BeautifulSoup
import os
import requests


def translate(translate_from, translate_to, word):
    url = f"https://context.reverso.net/translation/{translate_from.lower()}-{translate_to.lower()}/{word.lower()}"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    main_soup = BeautifulSoup(response.content, 'html.parser')
    sentences_soup = main_soup.find("section", {"id": "examples-content"})
    words = [i.text for i in main_soup.find_all("span", {"class": "display-term"})]
    sentences = [i.text.strip() for i in sentences_soup.find_all("span", {"class": "text"})]
    with open(word + ".txt", "a", encoding="utf-8") as word_file:
        print(f"{translate_to} Translations:", words[0], f"\n{translate_to} Examples:", sep="\n", file=word_file)
        print(sentences[0], sentences[1], "\n", sep="\n", file=word_file)


def main():
    print('The current working directory is', os.getcwd())
    languages = {"1": "Arabic", "2": "German", "3": "English", "4": "Spanish", "5": "French",
                 "6": "Hebrew", "7": "Japanese", "8": "Dutch", "9": "Polish", "10": "Portuguese",
                 "11": "Romanian", "12": "Russian", "13": "Turkish"}
    print("Hello, welcome to the translator. Translator supports:")
    for n, language in languages.items():
        print(f"{n}. {language}")
    translate_from = languages[input("Type the number of your language:\n")]
    user_number = input("Type the number of language you want to translate to:\n")
    word = input('Type the word you want to translate:\n')
    translate(translate_from, languages[user_number], word)
    with open(word + ".txt", encoding="utf-8") as word_file:
        print(word_file.read())


if __name__ == "__main__":
    main()
