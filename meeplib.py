import pickle
"""
meeplib - A simple message board back-end implementation.

Functions and classes:

 * u = User(username, password) - creates & saves a User object.  u.id
     is a guaranteed unique integer reference.

 * m = Message(title, post, author) - creates & saves a Message object.
     'author' must be a User object.  'm.id' guaranteed unique integer.

 * get_all_messages() - returns a list of all Message objects.

 * get_all_users() - returns a list of all User objects.

 * delete_message(m) - deletes Message object 'm' from internal lists.

 * delete_user(u) - deletes User object 'u' from internal lists.

 * get_user(username) - retrieves User object for user 'username'.

 * get_message(msg_id) - retrieves Message object for message with id msg_id.

"""

__all__ = ['Message', 'get_all_messages', 'get_message', 'delete_message',
           'User', 'get_user', 'get_all_users', 'delete_user']


###
# internal data structures & functions; please don't access these
# directly from outside the module.  Note, I'm not responsible for
# what happens to you if you do access them directly.  CTB

# a dictionary, storing all messages by a (unique, int) ID -> Message object.
_messages = {}

def _get_next_message_id():
    if _messages:
        return max(_messages.keys()) + 1
    return 0

# a dictionary, storing all users by a (unique, int) ID -> User object.
_user_ids = {}

# a dictionary, storing all users by username
_users = {}

_filename = 'save.pickle'

def initialize():
    try:
        print 'loading'
        print _filename
        fp = open(_filename)
        # load data
        obj = pickle.load(fp)
        fp.close()
        print 'file retrieved'
        global _users, _user_ids, _messages
        _users = obj[0]
        _user_ids = obj[1]
        _messages = obj[2]
        print "number of users: %d" %(len(_users),)
        print "most current user: %s" %(_users[max(_users.keys())].username,)
        print 'successfully loaded data'
    except:  # file does not exist/cannot be opened
        print 'error loading. loading defaults'
        # create a default user
        u = User('foo', 'bar')
        # create a single message
        Message('my title', 'This is my message!', u)

def _save():
    obj = []
    obj.append(_users)
    obj.append(_user_ids)
    obj.append(_messages)
    try:
        print 'saving'
        fp = open(_filename, 'w')
        pickle.dump(obj, fp)
        fp.close()
        print 'successful'
    except IOError:
        pass

def _get_next_user_id():
    if _users:
        return max(_user_ids.keys()) + 1
    return 0

def _reset():
    """
    Clean out all persistent data structures, for testing purposes.
    """
    global _messages, _users, _user_ids
    _messages = {}
    _users = {}
    _user_ids = {}

###  

class Message(object):
    """
    Simple "Message" object, containing title/post/author.

    'author' must be an object of type 'User'.

    """
    def __init__(self, title, post, author):
        self.title = title
        self.post = post

        assert isinstance(author, User)
        self.author = author
        #adding another property to the Message object for replies
        self.replies = []
        self._save_message()

    def _save_message(self):
        self.id = _get_next_message_id()


        # register this new message with the messages list:
        _messages[self.id] = self
        _save()
        
    #addReply will add the reply paramter to the self.replies string array
    def add_reply(self, reply):
        self.replies.append(str(reply))
        _save()

def get_all_messages(sort_by='id'):
    return _messages.values()

def get_message(id):
    return _messages[id]

def delete_message(msg):
    assert isinstance(msg, Message)
    del _messages[msg.id]
    _save()

###

class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self._save_user()

    def _save_user(self):
        self.id = _get_next_user_id()

        # register new user ID with the users list:
        _user_ids[self.id] = self
        _users[self.username] = self
        _save()

def get_user(username):
    return _users.get(username)         # return None if no such user

def get_all_users():
    return _users.values()

def delete_user(user):
    del _users[user.username]
    del _user_ids[user.id]
    _save()


#edited meeplib for reply functionality 11/23/12



