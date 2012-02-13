import unittest
import sys
import os.path
cwd = os.path.dirname(__file__)
importdir = os.path.abspath(os.path.join(cwd, '../'))
if importdir not in sys.path:
    sys.path.append(importdir)
import meeplib

# note:
#
# functions start within test_ are discovered and run
#       between setUp and tearDown;
# setUp and tearDown are run *once* for *each* test_ function.

class TestMeepLib(unittest.TestCase):
    def setUp(self):
        u = meeplib.User('foo', 'bar')
        t = meeplib.Thread('the title')
        m = meeplib.Message('the content', u)
        t.add_post(m)

    def test_for_message_existence(self):
        x = meeplib.get_all_threads()[0]
        y = x.get_all_posts()
        assert len(y) == 1
        assert x.title == 'the title'
        assert y[0].post == 'the content'

    def test_message_ownership(self):
        x = meeplib.get_all_users()
        assert len(x) == 1
        u = x[0]

        t = meeplib.get_all_threads()[0]
        x = t.get_all_posts()
        assert len(x) == 1
        m = x[0]

        assert m.author == u

    def test_get_next_user(self):
        x = meeplib._get_next_user_id()
        assert x != None

    def tearDown(self):
        t = meeplib.get_all_threads()[0]
        m = t.get_all_posts()[0]
        t.delete_post(m)

        u = meeplib.get_all_users()[0]
        meeplib.delete_user(u)

        assert len(meeplib._threads) == 0
        assert len(meeplib._users) == 0
        assert len(meeplib._user_ids) == 0

if __name__ == '__main__':
    unittest.main()
