import unittest
import os
from ontology_engine import OntologyEngine, ChangeLog, OntologyNode

class TestOntologyEngine(unittest.TestCase):
    def setUp(self):
        self.db_file = "test_ontology.db"
        if os.path.exists(self.db_file):
            os.remove(self.db_file)
        self.engine = OntologyEngine(f"sqlite:///{self.db_file}")

    def tearDown(self):
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_version_creation(self):
        v1 = self.engine.set_version("v1.0", "Initial version")
        self.assertEqual(v1['tag'], "v1.0")

        # Test re-setting same version
        v1_again = self.engine.set_version("v1.0")
        self.assertEqual(v1['id'], v1_again['id'])

    def test_node_creation(self):
        self.engine.set_version("v1.0")
        node_id = self.engine.create_node("Test Node", {"attr": "value"})

        node = self.engine.get_node(node_id)
        self.assertEqual(node['name'], "Test Node")
        self.assertEqual(node['metadata']["attr"], "value")

    def test_relationship_creation(self):
        self.engine.set_version("v1.0")
        p_id = self.engine.create_node("Parent")
        c_id = self.engine.create_node("Child")

        edge_id = self.engine.create_relationship(p_id, c_id, "hierarchy", weight=0.8)
        self.assertIsNotNone(edge_id)

    def test_changelog(self):
        self.engine.set_version("v1.0")
        self.engine.create_node("Logged Node")

        logs = self.engine.get_logs()
        self.assertGreaterEqual(len(logs), 2) # Version creation + Node creation

        actions = [log['action'] for log in logs]
        self.assertIn("INSERT", actions)

    def test_no_version_error(self):
        with self.assertRaises(ValueError):
            self.engine.create_node("Floating Node")

if __name__ == "__main__":
    unittest.main()
