import os
import unittest

from oslab.process_tools import process_info


class ProcessInfoTests(unittest.TestCase):
    def test_current_process_is_detected(self):
        info = process_info(os.getpid())
        self.assertEqual(info["PID"], str(os.getpid()))
        self.assertNotEqual(info["Status"], "Unavailable")
        self.assertNotEqual(info["Name"], "Unavailable")


if __name__ == "__main__":
    unittest.main()
