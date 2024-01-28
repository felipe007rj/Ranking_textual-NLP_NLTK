import unittest
from src.preprocess import split_except_quotes

class TestPreprocess(unittest.TestCase):

    def test_split_except_quotes(self):
        # Caso de teste 1: String sem aspas duplas
        result = split_except_quotes("apple,orange,banana")
        self.assertEqual(result, ['apple', 'orange', 'banana'])

        # Caso de teste 2: String com aspas duplas
        result = split_except_quotes('apple,"orange,banana",grape')
        self.assertEqual(result, ['apple', '"orange,banana"', 'grape'])

        # Caso de teste 3: String com aspas duplas aninhadas
        result = split_except_quotes('apple,"orange,banana,pear","grape,kiwi"')
        self.assertEqual(result, ['apple', '"orange,banana,pear"', '"grape,kiwi"'])

if __name__ == '__main__':
    unittest.main()
