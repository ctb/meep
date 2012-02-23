import twill
import unittest
import meep_example_app
import meeplib
import meepcookie


def run_twill_tests(filename):
    fp = open(filename)
    twill.execute_string(fp.read(), initial_url='http://localhost:8000/')
    meeplib._reset()

class TestTwill(unittest.TestCase):
    def test_create_user(self):
        run_twill_tests('01test_create_user.twill')
        meeplib._reset()

##    def test_login_message(self):
##        run_twill_tests('02test_login.twill')
##
##    def test_add_message(self):
##        run_twill_tests('03test_add_message.twill')
##
##    def test_reply_message(self):
##        run_twill_tests('04test_reply_message.twill')
##
##    def test_delete_message(self):
##        run_twill_tests('05test_delete_message.twill')
##
##    def test_logout_message(self):
##        run_twill_tests('06test_logout.twill')

if __name__ == '__main__':
    unittest.main()
