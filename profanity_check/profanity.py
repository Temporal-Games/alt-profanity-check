import string
import pkg_resources
from collections import OrderedDict

class Profanity:
    from typing import Set
    profanity: Set[str] = set(
        open(pkg_resources.resource_filename("profanity_check", "data/profanity.txt")).read().splitlines()
    )


    def __init__(self, censor_char: str = '*'):
        self.censor_char = censor_char
    @staticmethod
    def check_word(word: str):
        while len(word) > 0 and word[-1] in (string.punctuation + string.digits):
            word = word[:-1]
        while len(word) > 0 and  word[0] in (string.punctuation + string.digits):
            word = word[1:]

        return word.lower()


    def censor(self, text: str) -> str:
        words = text.split(' ')

        for i, word in enumerate(words):
            checked_word = self.check_word(word)
            variants = {
                word,
                checked_word,
                ''.join(OrderedDict.fromkeys(checked_word).keys()),
                word.translate(str.maketrans('', '', string.digits)),
                word.translate(str.maketrans('', '', string.punctuation)),
            }
            if len(
                variants & self.profanity
            ):
                words[i] = ''.join([char if not char.isalpha() else self.censor_char for char in word])

        return ' '.join(words)
