import unittest

from fds.classification import BagOfWords

class TestBagOfWords(unittest.TestCase):
    def test_bagofwords(self):
        bow = BagOfWords('abc', ('cat', 'dog'), tuple(), smoothing=1)
        print(bow)

