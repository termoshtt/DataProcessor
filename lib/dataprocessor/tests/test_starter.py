# -*- coding: utf-8 -*-

from . import helper
from .. import starter, basket, nodes

import os.path as op


class TestStarter(helper.TestEnvironment):

    def test_start(self):
        N = len(self.node_list)
        starter.start(self.node_list, ["touch", "homhom"], [])
        self.assertEqual(len(self.node_list), N + 1)
        node = self.node_list[-1]
        path = node["path"]
        self.assertTrue(op.exists(op.join(path, "homhom")))

    def test_start_projects(self):
        N = len(self.node_list)
        node = starter.start(self.node_list, ["touch", "homhom"], [],
                             projects=["mado_magi"])
        self.assertEqual(len(self.node_list), N + 2)
        project_path = basket.get_tag_abspath("mado_magi")
        self.assertTrue(op.exists(project_path))
        self.assertTrue(project_path in node["parents"])

        project_node = nodes.get(self.node_list, project_path)
        self.assertTrue(node["path"] in project_node["children"])
