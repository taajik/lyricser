
import os
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


class FormatPathTest(unittest.TestCase):
    """test class for format_path function"""

    def test_basic_path(self):
        raw_p = "/fake_dir/for/test/2"
        p = str(utils.format_path(raw_p))
        self.assertEqual(raw_p, p)

    def test_basic_path_with_tilde(self):
        raw_p = "~/fake_dir/for/test/2"
        p = str(utils.format_path(raw_p))
        self.assertEqual(os.path.expanduser(raw_p), p)

    def test_empty_path(self):
        p = utils.format_path("")
        self.assertEqual(os.path.realpath(""), str(p))

    def test_dot_path(self):
        p = utils.format_path(".")
        self.assertEqual(os.path.realpath("."), str(p))

    def test_single_quoted_path(self):
        p = utils.format_path("'/fake/dir/for/test/2'")
        self.assertEqual("/fake/dir/for/test/2", str(p))

    def test_double_quoted_path(self):
        p = utils.format_path('"/fake/dir/for/test/2"')
        self.assertEqual('/fake/dir/for/test/2', str(p))

    def test_path_with_escaped_quote(self):
        p = utils.format_path("/Musics/Metallica/06 Don'\\''t Tread On Me_Metallica.mp3")
        self.assertEqual("/Musics/Metallica/06 Don't Tread On Me_Metallica.mp3", str(p))

    def test_complex_path(self):
        p = utils.format_path("   \"''~/songs 2/Mega'\\''deth/01 The Sick, The Dying… And The Dead!_Megadeth.mp3\"' ")
        self.assertEqual(os.path.expanduser("~/songs 2/Mega'deth/01 The Sick, The Dying… And The Dead!_Megadeth.mp3"), str(p))




if __name__ == "__main__":
    unittest.main()
