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

# a string, stores the current user that is logged on
_curr_user = []

# a dictionary, storing all messages by a (unique, int) ID -> Message object.
_messages = {}

# a dictionary, storing all users by a (unique, int) ID -> User object.
_user_ids = {}

# a dictionary, storing all users by username
_users = {}

# a dictionary, storing all topics by a (unique, int) ID -> Topic object.
_topics = {}

def _get_next_message_id():
    if _messages:
        return max(_messages.keys()) + 1
    return 0

def _get_next_user_id():
    if _users:
        return int(max(_user_ids.keys())) + 1
    return 0
    
def _get_next_topic_id():
    if _topics:
        return max(_topics.keys()) + 1
    return 0

def _reset():
    """
    Clean out all persistent data structures, for testing purposes.
    """
    global _messages, _users, _user_ids, _topics, _curr_user
    _messages = {}
    _users = {}
    _user_ids = {}
    _topics = {}
    _curr_user = []

###

###
# Pickle implentation
###

# Filename for topics
_topics_filename = 'topics.pickle'

# Filename for messages
_messages_filename = 'messages.pickle'

# Filename for users
_users_filename = 'users.pickle'

def _load_data():
    global _topics, _messages, _users, _user_ids

    #Load topics data
    fp = open(_topics_filename, 'r')
    _topics = pickle.load(fp)
    #_print_topics()
    fp.close()
    
    #Load messages data
    fp1 = open(_messages_filename, 'r')
    _messages = pickle.load(fp1)
    #_print_messages()
    fp1.close()
    
    #Load users data
    fp2 = open(_users_filename, 'r')
    _users = pickle.load(fp2)
    #_print_users()
    _user_ids = pickle.load(fp2)
    fp2.close()

def _save_topic_data():
    fp = open(_topics_filename, 'w')
    pickle.dump(_topics, fp)
    fp.close()

def _save_message_data():
    fp = open(_messages_filename, 'w')
    pickle.dump(_messages, fp)
    fp.close()

def _save_user_data():
    fp = open(_users_filename, 'w')
    pickle.dump(_users, fp)
    pickle.dump(_user_ids, fp)
    fp.close()

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

        self._save_message()

    def _save_message(self):
        self.id = _get_next_message_id()
        
        # register this new message with the messages list:
        _messages[self.id] = self
        
        _save_message_data()

def get_all_messages(sort_by='id'):
    return _messages.values()

def get_message(id):
    return _messages[id]

def delete_message(msg):
    assert isinstance(msg, Message)
    del _messages[msg.id]
    _save_message_data()

###

class Topic(object):
    """
    Simple "Topic" object, containing a title, author, and messages.
    
    author must be an object of type 'User', and messages contains objects of type 'Message'
    """
    def __init__(self, title, message, author):
        self.title = title
        
        assert isinstance(message, Message)
        #self.messages = {self._get_next_msg_id() : message}
        self.messages = {message.id : message}
        
        assert isinstance(author, User)
        self.author = author
        
        self._save_topic()
        
    def _save_topic(self):
        self.id = _get_next_topic_id()
        
        _topics[self.id] = self
        
        _save_topic_data()
        
    def _get_next_msg_id(self):
        if self.messages:
            return max(self.messages.keys()) + 1
        return 0
        
    def get_messages(self):
        return self.messages.values()
        
    def add_message(self, message):
        assert isinstance(message, Message)
        self.messages[self._get_next_msg_id()] = message
        _save_topic_data()
        
    def delete_message_from_topic(self, msg):
        assert isinstance(msg, Message)
        del self.messages[msg.id]
        _save_topic_data()
        
def get_all_topics():
    return _topics.values()

def get_topic(id):
    return _topics[id]
        
def delete_topic(topic):
    del _topics[topic.id]
    _save_topic_data()

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
        
        _save_user_data()

def set_curr_user(username):
    _curr_user.insert(0, username)

def get_curr_user():
    if(len(_curr_user) > 0):
        return _curr_user[0]
    else:
        return null

def delete_curr_user(username):
    _curr_user.remove(_curr_user.index(0))

def get_user(username):
    try:
        return _users.pop(username)
    except KeyError:
        raise KeyError
    

def get_all_users():
    return _users.values()

def delete_user(user):
    del _users[user.username]
    del _user_ids[user.id]
    _save_user_data()

def check_user(username, password):
    try:
        aUser = get_user(username)
    except KeyError:
        aUser = None
        return False

    if aUser.password == password:
        return True
    else:
        return False

###

###
# Debugging functions
###

def _print_topics():
    for x in _topics.values():
        print 'Topic ID: ', x.id, 'Title: ', x.title

def _print_messages():
    for x in _messages.values():
        print 'Message ID: ', x.id, 'Title: ', x.title, 'Message: ', x.post

def _print_users():
    for x in _users.values():
        print 'Username: ', x.username, 'Password: ', x.password
    
def _print_user_ids():
    pass
