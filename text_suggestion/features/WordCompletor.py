from typing import List

class WordCompletor:
    def __init__(self, corpus: List[str]):
        """
        corpus: list – корпус текстов
        """
        self.word_count_dict = {}
        
        self.words_count = 0
        
        for corpus_item in corpus:
            self.words_count += len(corpus_item)
            for word in corpus_item:
                if word in self.word_count_dict.keys():
                    self.word_count_dict[word] += 1
                else:
                    self.word_count_dict[word] = 1

        self.word_count_dict = {key: value / self.words_count for key, value in self.word_count_dict.items()}
        
        self.prefix_tree = PrefixTree(self.word_count_dict.keys())
        

    def get_words_and_probs(self, prefix: str) -> (List[str], List[float]):
        """
        Возвращает список слов, начинающихся на prefix,
        с их вероятностями (нормировать ничего не нужно)
        """
        words = self.prefix_tree.search_prefix(prefix)
        
        probs = [self.word_count_dict[word] for word in words]
        
        return words, probs