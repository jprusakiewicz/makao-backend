import os
import unittest

from app.room import Room


class MyTestCase(unittest.TestCase):
    def test_exporting_makao(self):
        os.environ[
            'EXPORT_RESULTS_URL'] = "https://backend-dev.capgemini.enl-projects.com"
        r = Room('61841128ed510a0007472145')
        r.export_makao_move('finish', '616ef6dabd5803000747bdaf')
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
