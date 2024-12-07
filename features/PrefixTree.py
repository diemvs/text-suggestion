from typing import List

class PrefixTreeNode:
    def __init__(self):
        # словарь с буквами, которые могут идти после данной вершины
        self.children: dict[str, PrefixTreeNode] = {}
        self.is_end_of_word = False

class PrefixTree:
    def __init__(self, vocabulary: List[str]):
        """
        vocabulary: список всех уникальных токенов в корпусе
        """
        self.root = PrefixTreeNode()
        
        for word in vocabulary:
            current_node = self.root
            for char in word:
                if char not in current_node.children:
                    current_node.children[char] = PrefixTreeNode()
                current_node = current_node.children[char]
            current_node.is_end_of_word = True

    def search_prefix(self, prefix: str) -> List[str]:
        """
        Возвращает все слова, начинающиеся на prefix
        prefix: str – префикс слова
        """
        current_node = self.root
        
        for char in prefix:
            if char in current_node.children:
                current_node = current_node.children[char]
            else:
                return []

        def get_bottom_prefixes(node: PrefixTreeNode, path: str) -> List[str]:
            results = []
            if node.is_end_of_word:
                results.append(path)
            for char, child in node.children.items():
                results.extend(get_bottom_prefixes(child, path + char))
            return results

        return get_bottom_prefixes(current_node, prefix)