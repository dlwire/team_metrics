import unittest
from metrics_storer import *
from json import loads, dumps
import os

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

class ReaderTest(unittest.TestCase):
    def tearDown(self):
        if os.path.isfile('this_file_should_exist'):
            os.remove('this_file_should_exist')

    def test_no_such_file_reads_as_empty_list(self):
        testPath = "this_file_should_never_exist"
        self.assertFalse(os.path.exists(testPath))
        self.assertEqual([], read(testPath))
        self.assertFalse(os.path.exists(testPath))

    def test_empty_file_reads_as_empty_list(self):
        testPath = "this_file_should_exist"
        with open(testPath, 'w') as f:
            f.write("")

        self.assertEqual([], read(testPath))

    def test_file_with_list_should_return_list(self):
        testPath = "this_file_should_exist"
        with open(testPath, 'w') as f:
            data = dumps([{"a":"a"},{'b':'b'}])
            f.write(data)
        
        self.assertEqual([{'a':'a'},{'b':'b'}], read(testPath))

    def test_file_with_hash_should_return_list(self):
        testPath = "this_file_should_exist"
        with open(testPath, 'w') as f:
            data = dumps({"a":"a"})
            f.write(data)
        
        self.assertEqual([{'a':'a'}], read(testPath))

class WriteTest(unittest.TestCase):
    def tearDown(self):
        if os.path.isfile('this_file_should_exist'):
            os.remove('this_file_should_exist')

    def test_does_not_write_no_data(self):
        write('this_file_should_not_exist', [])
        self.assertFalse(os.path.isfile('this_file_should_not_exist'))

    def test_writes_data_if_file_does_not_exist(self):
        write('this_file_should_exist', [{'a':'a'}])
        self.assertTrue(os.path.isfile('this_file_should_exist'))
        self.assertEqual([{'a':'a'}], read('this_file_should_exist'))
        
    def test_writes_data_if_file_does_exist(self):
        testPath = 'this_file_should_exist'
        with open(testPath, 'w') as f:
            f.write(dumps([{'b':'b'}]))

        write('this_file_should_exist', [{'a':'a'}])
        self.assertEqual([{'a':'a'}], read('this_file_should_exist'))

#    def test_writes_to_unique_file(self):
#        os.makedirs("_data_")
#        for i in range(1000):
#            write("data", {'a':'b'})


if __name__ == '__main__':
    unittest.main()
