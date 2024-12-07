from typing import List, Union

class TextSuggestion:
    def __init__(self, word_completor, n_gram_model):
        self.word_completor = word_completor
        self.n_gram_model = n_gram_model

    def suggest_text(self, text: Union[str, list], n_words=3, n_texts=1) -> list[list[str]]:
        """
        Возвращает возможные варианты продолжения текста (по умолчанию только один)
        
        text: строка или список слов – написанный пользователем текст
        n_words: число слов, которые дописывает n-граммная модель
        n_texts: число возвращаемых продолжений (пока что только одно)
        
        return: list[list[srt]] – список из n_texts списков слов, по 1 + n_words слов в каждом
        Первое слово – это то, которое WordCompletor дополнил до целого.
        """
        
        suggestions = []
        
        suggestion = []
        
        if(isinstance(text, str)):
            words = text.strip().split()
        elif(isinstance(text, list)):
            words = text
        else:
            raise ValueError('Недопустимый тип text')
        
        if(len(words) == 0):
            return []
        # получим последнее слово
        last_word = words[-1]
        # получаем варианты дополнения последнего слова до целого
        completor_words, completor_probs = self.word_completor.get_words_and_probs(last_word)
        # если completor_words вернул дополненные слова, то берем слово с наибольшей вероятностью
        last_word = completor_words[completor_probs.index(max(completor_probs))] if len(completor_words) > 0 else last_word
        # заменяем последнее слово
        words[-1] = last_word
        
        suggestion.append(last_word)
        
        n = self.n_gram_model.n
        # получаем контекст (n - 1) слов
        context = words[-(n - 1):]  if n > 1 else []
        
        for _ in range(n_words):
            # получаем предсказания следующих n_word слов
            n_gram_words, n_gram_probs = self.n_gram_model.get_next_words_and_probs(context)
            
            if len(n_gram_words) == 0:
                break
            # берем слово с макс вероятностью
            next_word = n_gram_words[n_gram_probs.index(max(n_gram_probs))]
            
            suggestion.append(next_word)
            # добавляем в контекст
            context = context[1:] + [next_word] if n > 1 else [next_word]
            
        suggestions.append(suggestion)
            
        return suggestions