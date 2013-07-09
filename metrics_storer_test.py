import unittest
from metrics_storer import *
from json import loads, dumps
import os
import shutil
import StringIO

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
    def setUp(self):
        self.dirName = '_data_'
    def tearDown(self):
        if os.path.isfile('this_file_should_exist'):
            os.remove('this_file_should_exist')
        if os.path.isdir(self.dirName):
            shutil.rmtree(self.dirName)

    def test_does_not_write_no_data(self):
        writeToDir('this_file_should_not_exist', [])
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

    def test_writes_to_unique_file(self):
        count = 1000
        os.makedirs(self.dirName)
        for i in range(count):
            writeToDir(self.dirName, {str(i) : (i%2)})

        actual = {}
        for fname in os.listdir(self.dirName):
            with open(os.path.join(self.dirName, fname)) as f:
                fileData = loads(f.read())
                for k,v in fileData.items():
                    actual[k] = v

        self.assertEqual(count, len(actual.keys()))

class NiceDataTest(unittest.TestCase):
    def test_value_arrays_are_mapped_to_values(self):
        self.assertEqual({'a':'a'}, mapValues({'a':['a']}))

    def test_values_which_are_integers_are_mapped_to_ints(self):
        self.assertEqual({'a':1}, mapValues({'a':'1'}))

    def test_values_which_are_floats_are_mapped_to_floats(self):
        self.assertEqual({'a':1.0}, mapValues({'a':'1.0'}))

    def test_removes_trailing_percents_from_value(self):
        self.assertEqual({'a':1}, mapValues({'a':'1 %'}))

    def test_removes_trailing_days_from_value(self):
        self.assertEqual({'a':1}, mapValues({'a':'1 days'}))

class DataDirTest(unittest.TestCase):
    def setUp(self):
        self.dirName = '_data_'
    def tearDown(self):
        if os.path.isdir(self.dirName):
            shutil.rmtree(self.dirName)
    def test_joins_data_from_all_files_in_dir(self):
        count = 1000
        os.makedirs(self.dirName)
        for i in range(count):
            writeToDir(self.dirName, {str(i) : (i%2)})

        data = readDirAsJson(self.dirName)
        self.assertEqual(count, len(data))
class CsvTest(unittest.TestCase):
    def test_creates_csv_with_headers_from_list(self):
        f = StringIO.StringIO()
        toCsv(f, [{'a':1, 'b':2, 'c':3}])
        self.assertEqual("""a,c,b\r
1,3,2\r
""", f.getvalue())

    def test_creates_csv_with_headers_for_list_of_several_items(self):
        f = StringIO.StringIO()
        toCsv(f, [{'a':1, 'b':2, 'c':3},{'a':4, 'b':5, 'c':6}, {'a':7, 'b':8, 'c':9}])
        self.assertEqual("""a,c,b\r
1,3,2\r
4,6,5\r
7,9,8\r
""", f.getvalue())

if __name__ == '__main__':
    unittest.main()
