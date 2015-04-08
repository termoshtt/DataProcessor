import os
import unittest
import tempfile

from .. import utility
from ..exception import DataProcessorError


class TestUtility(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tempdir)

    def test_check_file(self):
        tempfile = os.path.join(self.tempdir, "foo")
        relative_path = os.path.relpath(tempfile)
        with self.assertRaises(DataProcessorError):
            utility.check_file(tempfile)
        open(tempfile, "a").close()
        self.assertEqual(utility.check_file(tempfile), tempfile)
        self.assertEqual(utility.check_file(relative_path), tempfile)

        dir_path = os.path.join(self.tempdir, "bar")
        relative_path = os.path.relpath(dir_path)
        with self.assertRaises(DataProcessorError):
            utility.check_file(dir_path)
        os.mkdir(dir_path)
        with self.assertRaises(DataProcessorError):
            utility.check_file(dir_path)
        with self.assertRaises(DataProcessorError):
            utility.check_file(relative_path)

    def test_check_directory(self):
        tempfile = os.path.join(self.tempdir, "foo")
        with self.assertRaises(DataProcessorError):
            utility.check_directory(tempfile)
        open(tempfile, "a").close()
        with self.assertRaises(DataProcessorError):
            utility.check_directory(tempfile)
        relative_path = os.path.relpath(tempfile)
        with self.assertRaises(DataProcessorError):
            utility.check_directory(relative_path)

        dir_path = os.path.join(self.tempdir, "bar")
        relative_path = os.path.relpath(dir_path)
        with self.assertRaises(DataProcessorError):
            utility.check_directory(dir_path)
        os.mkdir(dir_path)
        self.assertEqual(utility.check_directory(dir_path), dir_path)
        self.assertEqual(utility.check_directory(relative_path), dir_path)

    def test_get_directory1(self):
        tempfile = os.path.join(self.tempdir, "foo")
        open(tempfile, "a").close()
        with self.assertRaises(DataProcessorError):
            utility.get_directory(tempfile)

        temp_dir = os.path.join(self.tempdir, "bar")
        os.mkdir(temp_dir)
        self.assertEqual(utility.get_directory(temp_dir), temp_dir)

    def test_get_directory2(self):
        temp_dir = os.path.join(self.tempdir, "bar")
        self.assertEqual(utility.get_directory(temp_dir, True), temp_dir)

    def test_get_directory3(self):
        temp_dir = os.path.join(self.tempdir, "bar")
        relative_path = os.path.relpath(temp_dir)
        os.mkdir(temp_dir)
        self.assertEqual(utility.get_directory(relative_path, temp_dir),
                         temp_dir)

    def test_read_configure1(self):
        configure_path = os.path.join(self.tempdir, "conf")
        contents = """hgoe=1\nhoge=2\ndafo=ds\n#hoge=ds"""
        self.create_file(configure_path, contents)
        conf = utility.read_configure(configure_path)
        self.assertEqual(conf, {"hgoe": "1", "hoge": "2", "dafo": "ds"})

    def test_read_configure2(self):
        configure_path = os.path.join(self.tempdir, "conf")
        # does not comment.
        contents = """hgoe=1\nhoge=2\ndafo=ds\n #hoge=ds"""
        self.create_file(configure_path, contents)
        conf = utility.read_configure(configure_path)
        self.assertEqual(conf, {"hgoe": "1", "hoge": "2",
                                "dafo": "ds", "#hoge": "ds"})

    def test_read_configure3(self):
        configure_path = os.path.join(self.tempdir, "conf")
        contents = """hgoe:1\nhoge   :   2\ndafo : ds\n!hoge=ds"""
        self.create_file(configure_path, contents)
        conf = utility.read_configure(configure_path, ":", "!")
        self.assertEqual(conf, {"hgoe": "1", "hoge": "2", "dafo": "ds"})

    def create_file(self, path, contents):
        f = open(path, "w")
        f.write(contents)
        f.close()
