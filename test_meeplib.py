import unittest
import meeplib
import os

# note:
#
# functions start within test_ are discovered and run
#       between setUp and tearDown;
# setUp and tearDown are run *once* for *each* test_ function.

class TestMeepLib(unittest.TestCase):
    def setUp(self):
        u = meeplib.User('foo', 'bar')
        m = meeplib.Message('the title', 'the content', u, -1)
        try:
            os.remove(meeplib._getFileName())
        except:
            pass    #the file does not exist
        
    def test_backup_and_load_meep(self):        
        #create a user, and message, then backup, reset data in app
        meeplib.User('admin', 'admin')
        author = meeplib.get_user('admin')
        message = meeplib.Message('title', 'message', author, -1)
        
        meeplib._backup_meep()
        meeplib._reset()
        
        #check that the file exists and contains information about the message and user
        try:
            meeplib._load_backup()
            assert author in meeplib._users.values()
            assert message in meeplib._messages.values()
        except:
            assert False    #the test failed
            
    def test_get_next_message_id(self):
        #there should be 1 message initially created
        assert meeplib._get_next_message_id() == 1
        meeplib.User('admin', 'admin')
        author = meeplib.get_user('admin')
        message = meeplib.Message('title', 'message', author, -1)
        
        #there should not be two messages
        assert meeplib._get_next_message_id() == 2
        
    def test_get_next_user_id(self):
        #there should be 1 user initially
        assert meeplib._get_next_user_id() == 1
        meeplib.User('admin', 'admin')
        #there should be 2 users now
        assert meeplib._get_next_user_id() == 2
        
    def test_reset(self):
        #there should be 1 user and 1 message initially
        assert meeplib._get_next_message_id() == 1
        assert meeplib._get_next_user_id() == 1
        meeplib._reset()
        assert meeplib._get_next_message_id() == 0
        assert meeplib._get_next_user_id() == 0
        
    def test_get_root_messages(self):
        meeplib.User('admin', 'admin')
        author = meeplib.get_user('admin')
        message1 = meeplib.Message('title1', 'message1', author, -1)
        message2 = meeplib.Message('title2', 'message2', author, -1)
        message3 = meeplib.Message('title3', 'message3', author, 0)
        
        root_messages = meeplib._get_root_messages()
        assert message1 in root_messages
        assert message2 in root_messages
        assert message3 not in root_messages

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
        
    def test_get_message(self):
        user = meeplib._users['foo']
        assert meeplib.Message('the title', 'the content', user, -1) == meeplib._messages[0]
        
    def test_get_user(self):
        assert meeplib._users['foo'] == meeplib.get_user('foo')
        
    def test_get_all_users(self):
        #create one more user, so there are 2 users in total
        meeplib.User('foo2', 'bar2')
        assert len(meeplib.get_all_users()) == 2
        
    def test_delete_user(self):
        #check that there is 1 user
        assert len(meeplib.get_all_users()) == 1
        assert len(meeplib._user_ids) == 1
        meeplib.delete_user(meeplib.get_user('foo'))
        
        #check that there are no users
        assert len(meeplib.get_all_users()) == 0
        assert len(meeplib._user_ids) == 0


    def tearDown(self):
        meeplib._reset()
        assert len(meeplib._messages) == 0
        assert len(meeplib._users) == 0
        assert len(meeplib._user_ids) == 0

if __name__ == '__main__':
    unittest.main()
