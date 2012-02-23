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
        m = meeplib.Message('the title', 'the content', u)

    def test_for_message_existence(self):
        x = meeplib.get_all_messages()
        assert len(x) == 1
        assert x[0].title == 'the title'
        assert x[0].post == 'the content'

    def test_message_ownership(self):
        x = meeplib.get_all_users()
        assert len(x) == 1
        u = x[0]

        x = meeplib.get_all_messages()
        assert len(x) == 1
        m = x[0]

        assert m.author == u
    
    def test_add_reply(self):
        msg = meeplib.get_all_messages()[0]
        reply = "I'm a reply."
        msg.add_reply(reply)

        myreply = msg.replies
        assert len(myreply) == 1
        
    def test_delete_message(self):
        temp = meeplib.get_all_messages()
        msg = meeplib.get_all_messages()[0]
        meeplib.delete_message(msg)
        
        assert len(meeplib.get_all_messages()) < len(temp)

    def test_get_next_user(self):
        x = meeplib._get_next_user_id()
        print x
        assert x!=None

    def tearDown(self):
##        if len(meeplib.get_all_messages()) > 0:
##            m = meeplib.get_all_messages()[0]
##            meeplib.delete_message(m)
##
##        u = meeplib.get_all_users()[0]
##        meeplib.delete_user(u)
        meeplib._reset()

        assert len(meeplib._messages) == 0
        assert len(meeplib._users) == 0
        assert len(meeplib._user_ids) == 0

if __name__ == '__main__':
    unittest.main()
