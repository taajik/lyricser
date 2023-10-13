
import unittest
from unittest.mock import patch

import utils


class ReportTest(unittest.TestCase):
    """test class for report functions."""

    def tearDown(self):
        utils.successful = 0
        utils.unsuccessful = 0

    def test_report_counters_default(self):
        self.assertEqual(0, utils.successful)
        self.assertEqual(0, utils.unsuccessful)

    def test_one_report_true(self):
        utils.report(True)
        self.assertEqual(1, utils.successful)
        self.assertEqual(0, utils.unsuccessful)

    def test_one_report_false(self):
        utils.report(False)
        self.assertEqual(0, utils.successful)
        self.assertEqual(1, utils.unsuccessful)

    def test_multiple_report_true(self):
        utils.report(True)
        utils.report(True)
        utils.report(True)
        self.assertEqual(3, utils.successful)
        self.assertEqual(0, utils.unsuccessful)

    def test_multiple_report_false(self):
        utils.report(False)
        utils.report(False)
        utils.report(False)
        self.assertEqual(0, utils.successful)
        self.assertEqual(3, utils.unsuccessful)

    def test_report_mixed(self):
        utils.report(False)
        utils.report(True)
        utils.report(True)
        utils.report(False)
        utils.report(True)
        self.assertEqual(3, utils.successful)
        self.assertEqual(2, utils.unsuccessful)

    def test_report_message(self):
        with patch("builtins.print") as mocked_print:
            message = " X Test error!"
            utils.report(False, message)
            mocked_print.assert_called_with(message)
            self.assertEqual(0, utils.successful)
            self.assertEqual(1, utils.unsuccessful)

    def test_report_no_message(self):
        with patch("builtins.print") as mocked_print:
            utils.report(True)
            mocked_print.assert_not_called()

    def test_print_report(self):
        utils.report(True)
        utils.report(True)
        utils.report(False)
        with patch("builtins.print") as mocked_print:
            suc_title, unsuc_title = "test suc title", "test unsuc title"
            utils.print_report(suc_title, unsuc_title)
            mocked_print.assert_called_with(
                f"\n\n\n {suc_title}: 2\n {unsuc_title}: 1"
            )




if __name__ == "__main__":
    unittest.main()
