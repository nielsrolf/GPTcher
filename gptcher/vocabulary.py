import os

import pandas as pd
from dotenv import load_dotenv

from gptcher.gpt_client import measure_time, supabase
from gptcher.translation import translate
from gptcher.settings import table_prefix


class Word:
    def __init__(
        self,
        word_en,
        target_language,
        word_translations,
        to_learn,
        score=0,
        showed=0,
        percentage=None,
    ):
        self.word_en = word_en.lower()
        if not isinstance(word_translations, list):
            word_translations = [word_translations]
        self.word_translations = word_translations
        self.score = score
        self.showed = showed
        self.to_learn = to_learn
        self.target_language = target_language

    @property
    def word_translated(self):
        return " / ".join(self.word_translations)

    @staticmethod
    def from_word(word_en, target_language, to_learn=False):
        word_translated = translate(target_language, word_en)
        return Word(word_en, target_language, word_translated, to_learn)

    @staticmethod
    def from_wordpair(word_en, word_translated, target_language, to_learn=False):
        return Word(word_en, target_language, word_translated, to_learn)

    def register_score(self, score, translation):
        self.score += score
        self.showed += 1
        if translation not in self.word_translations:
            self.word_translations.append(translation)

    @property
    def points(self):
        """
        Points are calculated as score / (showed + 3)
        Limit: points -> 2
        points = 1 if it was correctly answered 3 times and never incorrectly
        """
        return self.score / (self.showed + 3)

    def __str__(self):
        return f"{self.word_en} - {self.word_translated}"


# dictionary_en = pd.read_csv("data/words_en_small.csv")
# """
# > dictionary_en.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 333333 entries, 0 to 333332
# Data columns (total 5 columns):
#  #   Column  Non-Null Count   Dtype  
# ---  ------  --------------   -----  
#  0   word    333333 non-null  object 
#  1   count   333333 non-null  int64  
#  2   type    333333 non-null  object 
#  3   usage   333333 non-null  float64
#  4   cumsum  333333 non-null  float64
# dtypes: float64(2), int64(1), object(2)
# memory usage: 12.7+ MB
# """


class Vocabulary:
    def __init__(self, user, language):
        self.user = user
        self.language = language
        self.words = {}

    def __getitem__(self, word):
        if not self.words.get(word):
            self.words[word] = Word.from_word(word, self.language)
        return self.words[word]

    def __setitem__(self, word, value):
        self.words[word] = value

    def __contains__(self, word):
        return word in self.words

    @staticmethod
    def from_list(user, data):
        """Create a vocabulary from a dict"""
        words = [Word(**word) for word in data]
        vocabulary = Vocabulary(user, user.language)
        vocabulary.words = {word.word_en: word for word in words}
        return vocabulary

    def to_dict(self):
        """Convert the vocabulary to a dict"""
        return [word.__dict__ for word in self.words.values()]

    def to_db(self):
        """Save the db to supabase"""
        supabase.table(table_prefix + "users").update({"words": self.to_dict()}).eq(
            "user_id", self.user.user_id
        ).execute()

    def usage_percent_of_english_language(self):
        """Can tell you 'with this dataset, you understand 85% of the words used in the English language'"""
        return sum([word.percentage for word in self.words.values()])

    # def add_most_used_words(self, n, word_type=None):
    #     """Adds the n most used words from the english language to the passive vocabulary, with a count of 1
    #     If word_type is specified, only words of that type are added"""
    #     if word_type:
    #         words = dictionary_en[dictionary_en["type"] == word_type]
    #     else:
    #         words = dictionary_en
    #     # Sort the words by usage in descending order
    #     words = words.sort_values(by="usage", ascending=False)

    #     # Iterate through the top n most used words
    #     for i in range(n):
    #         # Get the word and usage from the DataFrame
    #         word = words.iloc[i]["word"]
    #         # Add the word to the passive vocabulary with a count of 1
    #         self[word].showed = max(1, self[word].showed)

    def add_wordpair(self, word_en, translation):
        """Add a word pair to the vocabulary"""
        self[word_en] = Word.from_wordpair(word_en, translation, self.language)

    def get_learn_list(self, n):
        """Returns a list of n words to learn - all words with their translation
        Words are the n words with the lowest score from the active vocabulary"""
        # Sort the words by score in ascending order
        words = sorted(self.words.values(), key=lambda word: word.score)
        # Select the n words with the lowest score
        words = words[:n]
        # Return the words and their translation
        vocab = Vocabulary(self.user, self.language)
        for word in words:
            vocab[word.word_en] = word
        return vocab

    def __str__(self):
        return "\n".join([str(word) for word in self.words.values()])

    @property
    def score(self):
        return round(sum([word.points for word in self.words.values()]) * 10) / 10
