import os
import unittest
import ansible

from ansiblelint import Runner, RulesCollection
from pkg_resources import parse_version


class TestTaskIncludes(unittest.TestCase):

    def setUp(self):
        rulesdir = os.path.join('lib', 'ansiblelint', 'rules')
        self.rules = RulesCollection.create_from_directory(rulesdir)

    def test_block_included_tasks(self):
        filename = 'test/blockincludes.yml'
        runner = Runner(self.rules, filename, [], [], [])
        runner.run()
        self.assertEqual(len(runner.playbooks), 4)

    def test_block_included_tasks_with_rescue_and_always(self):
        filename = 'test/blockincludes2.yml'
        runner = Runner(self.rules, filename, [], [], [])
        runner.run()
        self.assertEqual(len(runner.playbooks), 4)

    def test_included_tasks(self):
        filename = 'test/taskincludes.yml'
        runner = Runner(self.rules, filename, [], [], [])
        runner.run()
        self.assertEqual(len(runner.playbooks), 4)
