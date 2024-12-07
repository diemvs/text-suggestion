from typing import List, Tuple
from collections import Counter

class NGramLanguageModel:
    def __init__(self, corpus, n):
        # максимальная длинна N-граммы
        self.n = n 
        # Счётчик частот N-грамм
        self.ngram_counts = Counter()
        # Счётчик частот контекстов (первых n-1 слов)
        self.context_counts = Counter()
        
        # Построение N-грамм из корпуса
        for sentence in corpus:
            sentence_length = len(sentence)
            
            for word_index in range(sentence_length):
                for ngram_length in range(1, sentence_length - word_index + 1):  
                    ngram = tuple(sentence[word_index : word_index + ngram_length])
                    self.ngram_counts[ngram] += 1
                    # Контексты существуют только для n-грамм длиной > 1
                    if len(ngram) > 1:  
                        context = ngram[:-1]
                        self.context_counts[context] += 1
                
    def get_next_words_and_probs(self, prefix: list) -> (List[str], List[float]):
        """
        Возвращает список слов, которые могут идти после prefix,
        а так же список вероятностей этих слов
        """
        
        # Возможные следующие слова
        next_words = []  
        # Вероятности этих слов
        probs = []  
        # Преобразуем prefix в кортеж для сопоставления с n-граммами
        context = tuple(prefix)  
        # Найти все n-граммы, начинающиеся с данного контекста
        for ngram, count in self.ngram_counts.items():

            if ngram[:-1] == context:  # Проверка, соответствует ли n-грамма данному контексту
                next_word = ngram[-1]
                next_words.append(next_word)
                
                # Вычисляем вероятность слова как P(next_word | context)
                context_count = self.context_counts[context]
                probs.append(count / context_count)

        return next_words, probs