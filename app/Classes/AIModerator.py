import string
import re
import aiohttp

from typing import List, Any
from transformers import pipeline
from .base_moderator import Moderator
import asyncio


class AIModerator(Moderator):
    moderator_pipeline = pipeline("text-classification", model="cointegrated/rubert-tiny-toxicity")

    async def handle(self, request: Any, results: List[str]) -> List[str]:
        if isinstance(request, str):
            try:
                correct_text = await self.correct_text(request)
                text = await self.preprocess_text(correct_text)
                segments = self.split_text_into_segments(text)
                for segment in segments:
                    moderation_result = await asyncio.to_thread(self.moderate_text, segment)
                    interpretation = self.interpret_result(moderation_result)
                    if interpretation:
                        results.extend(interpretation)
            except Exception as e:
                raise RuntimeError(f"Error during moderation: {e}")
        return await super().handle(request, results)

    @staticmethod
    def split_text_into_segments(text: str, max_length: int = 500) -> List[str]:
        words = text.split()
        segments = []
        current_segment = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 > max_length:
                segments.append(' '.join(current_segment))
                current_segment = [word]
                current_length = len(word) + 1
            else:
                current_segment.append(word)
                current_length += len(word) + 1

        if current_segment:
            segments.append(' '.join(current_segment))

        return segments

    @staticmethod
    async def correct_text(text: str) -> str:
        YANDEX_SPELLER_API_URL = "https://speller.yandex.net/services/spellservice.json/checkText"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(YANDEX_SPELLER_API_URL, data={"text": text}) as response:
                    if response.status == 200:
                        corrections = await response.json()
                        corrected_text = text

                        for correction in corrections:
                            word = correction['word']
                            suggestions = correction['s']
                            if suggestions:
                                corrected_text = corrected_text.replace(word, suggestions[0])

                        print(f"Input text: {text}")
                        print(f"Corrected text: {corrected_text}")
                        return corrected_text
                    else:
                        return text  # Вернуть исходный текст, если сервис не вернул статус 200
        except Exception as e:
            print(f"ERROR: {e}")
            return text

    @staticmethod
    async def preprocess_text(text: str) -> str:
        # Преобразование в нижний регистр
        text = text.lower()
        # Удаление знаков препинания
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Удаление эмодзи и специальных символов
        text = re.sub(r'[^\w\s]', '', text)  # Оставляет только буквы, цифры и пробелы
        return text

    @staticmethod
    def moderate_text(text: str) -> List[dict]:
        try:
            return AIModerator.moderator_pipeline(text)
        except Exception as e:
            raise RuntimeError(f"Error in pipeline execution: {e}")

    @staticmethod
    def interpret_result(result: List[dict]) -> List[str]:
        try:
            interpretation = []
            for res in result:
                label = res['label']
                score = res['score']
                print(f"Score - {score} = {label}")
                if score > 0.7 and label != 'neutral' and label != 'non-toxic':
                    interpretation.append(f"✨ AI - {label}")
            return interpretation
        except Exception as e:
            raise RuntimeError(f"Error in result interpretation: {e}")
