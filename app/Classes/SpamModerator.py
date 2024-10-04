import os
import pickle
import string
from typing import Any, List
from .base_moderator import Moderator


class SpamModerator(Moderator):
    def __init__(self):
        filepath = os.path.join(os.path.dirname(__file__), 'resource', 'spam_classifier_model.pkl')
        with open(filepath, 'rb') as file:
            self.word_freq, self.ham_count, self.spam_count, self.total_count = pickle.load(file)

        self.stop_words = {'и', 'в', 'на', 'с', 'о', 'по', 'к', 'из', 'у', 'за', 'от', 'до', 'не', 'что', 'он', 'она',
                           'мы', 'вы'}

    async def handle(self, request: Any, results: List[str]) -> List[str]:
        if isinstance(request, str):
            if await self.classify(request) == 'spam':
                results.append('spam')
        return await super().handle(request, results)

    async def preprocess_text(self, text: str) -> str:
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text

    async def tokenize(self, text: str) -> List[str]:
        return [word for word in text.split() if word not in self.stop_words]

    async def classify(self, message: str) -> str:
        if not message.strip():  # Проверка на пустую строку
            return 'ham'

        words = await self.tokenize(await self.preprocess_text(message))
        p_ham = self.ham_count / self.total_count
        p_spam = self.spam_count / self.total_count
        p_word_given_ham = p_word_given_spam = 1.0

        for word in words:
            if word in self.word_freq:
                p_word_given_ham *= (self.word_freq[word][0] + 1) / (self.ham_count + len(self.word_freq))
                p_word_given_spam *= (self.word_freq[word][1] + 1) / (self.spam_count + len(self.word_freq))
            else:
                p_word_given_ham *= 1 / (self.ham_count + len(self.word_freq))
                p_word_given_spam *= 1 / (self.spam_count + len(self.word_freq))

        p_ham_given_message = p_word_given_ham * p_ham
        p_spam_given_message = p_word_given_spam * p_spam

        return 'spam' if p_spam_given_message > p_ham_given_message else 'ham'
