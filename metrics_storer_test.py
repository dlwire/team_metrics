import unittest
from metrics_storer import *
from json import loads

class SerialPosterTest(unittest.TestCase):
    def test_given_no_data_serialize_nothing(self):
        self.assertEqual(None, serialPoster({}))

    def test_given_one_element_serialize_it(self):
        testInput = {'team_name':'test team'}
        actual = loads(serialPoster(testInput))
        self.assertEqual(testInput, actual)

    def test_do_not_serialize_if_no_team_name(self):
        testInput = {'test_element':'test value'}
        self.assertEqual(None, serialPoster(testInput))

class JoinerTest(unittest.TestCase):
    def test_nothing_joined_with_nothing_is_nothing(self):
        self.assertEqual([], joiner([], {}))

    def test_nothing_joined_with_a_is_a(self):
        self.assertEqual([{'a':'b'}], joiner([], {'a':'b'}))

    def test_a_joined_with_b_is_ab(self):
        fileData = {'b':'c'}
        postData = {'a':'b'}
        self.assertEqual([fileData, postData], joiner([fileData], postData))

    def test_a_joined_with_nothing_is_a(self):
        fileData = [{'a':'b'}]
        postData = {}
        self.assertEqual(fileData, joiner(fileData, postData))

    def test_a_joined_with_a_is_a(self):
        fileData = {'a':'a'}
        postData = {'a':'a'}
        self.assertEqual([fileData], joiner([fileData], postData))


if __name__ == '__main__':
    unittest.main()
