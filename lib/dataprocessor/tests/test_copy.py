# -*- coding: utf-8 -*-

from . import helper
from .. import copy
from ..exception import DataProcessorError

import os


class TestUtility(helper.TestEnvironment):

    def test_copy_file1(self):
        from_path = os.path.join(self.tempdir_path, "fromfile")
        to_path = os.path.join(self.tempdir_path, "to_file")
        open(from_path, "a").close()

        copy.copy_file(from_path, to_path)
        self.assertTrue(os.path.exists(to_path))

    def test_copy_file2(self):
        from_path = os.path.join(self.tempdir_path, "fromfile")
        to_path = os.path.join(self.tempdir_path, "to_file")
        open(from_path, "a").close()
        open(to_path, "a").close()

        copy.copy_file(from_path, to_path)
        self.assertTrue(os.path.exists(to_path))

    def test_copy_file3(self):
        from_path = os.path.join(self.tempdir_path, "fromfile")
        to_path = os.path.join(self.tempdir_path, "foo/hogedir/to_file")
        open(from_path, "a").close()

        copy.copy_file(from_path, to_path)
        self.assertTrue(os.path.exists(to_path))

    def test_copy_file4(self):
        from_path = os.path.join(self.tempdir_path, "fromfile")
        to_path = os.path.join(self.tempdir_path, "to_file")

        with self.assertRaises(DataProcessorError):
            copy.copy_file(from_path, to_path)

    def test_copy_file5(self):
        from_path = os.path.join(self.tempdir_path, "fromfile")
        to_path = os.path.join(self.tempdir_path, "to_file")
        open(from_path, "a").close()
        f = open(to_path, "a")
        f.write("hoge")
        f.close()

        with self.assertRaises(DataProcessorError):
            copy.copy_file(from_path, to_path, "error")
        copy.copy_file(from_path, to_path, "skip")
        self.assertTrue(os.path.exists(to_path))
        copy.copy_file(from_path, to_path, "replace")
        self.assertTrue(os.path.exists(to_path))
