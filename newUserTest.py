import unittest
import meeplib

# note:
#
# functions start within test_ are discovered and run
#       between setUp and tearDown;
# setUp and tearDown are run *once* for *each* test_ function.

class TestMeepLib(unittest.TestCase):
    def setUp(self):
        u = meeplib.User('foo', 'bar')

    def test_new_user_bad_version(self):
        x1 = meeplib._get_next_user_id_ORG()
        
    def test_new_user_good_version(self):
        x1 = meeplib._get_next_user_id()

    def tearDown(self):
        u = meeplib.get_all_users()[0]
        meeplib.delete_user(u)

        assert len(meeplib._users) == 0
        assert len(meeplib._user_ids) == 0

if __name__ == '__main__':
    unittest.main()
