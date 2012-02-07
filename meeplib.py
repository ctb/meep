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

def _get_next_user_id():
    if _users:
        return max(_user_ids.keys()) + 1
    return 0
    
# a dictionary, storing all topics by a (unique, int) ID -> Topic object.
_topics = {}

def _get_next_topic_id():
    if _topics:
        return max(_topics.keys()) + 1
    return 0

def _reset():
    """
    Clean out all persistent data structures, for testing purposes.
    """
    global _messages, _users, _user_ids, _topics
    _messages = {}
    _users = {}
    _user_ids = {}
    _topics = {}
    
def save_data():

    obj = (_users, _user_ids, _topics, _messages)
    
    filename = 'save.meep.pickle'
    fp = open(filename, 'w')
    pickle.dump(obj, fp)
    fp.close()

def load_data():
    fp = open('save.meep.pickle')
    obj = pickle.load(fp)
    (users, user_ids, topics, messages) = obj
    
    for u in users:
        _users[u] = users[u]
        
    for i in user_ids:
        _user_ids[i] = user_ids[i]
        
    for t in topics:
        _topics[t] = topics[t]
        
    for m in messages:
        _messages[m] = messages[m]
        
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

def get_all_messages(sort_by='id'):
    return _messages.values()

def get_message(id):
    return _messages[id]

def delete_message(msg):
    assert isinstance(msg, Message)
    del _messages[msg.id]

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
        self.messages = {0 : message}
        
        assert isinstance(author, User)
        self.author = author
        
        self._save_topic()
        
    def _save_topic(self):
        self.id = _get_next_topic_id()
        
        _topics[self.id] = self
    
    def _add_message(self, message):
        print self._get_next_msg_id()
        self.messages[self._get_next_msg_id()] = message
        
    def _get_next_msg_id(self):
        if self.messages:
            return max(self.messages.keys()) + 1
        return 0
        
    def get_messages(self):
        return self.messages.values()
        
    def add_message(self, message):
        assert isinstance(message, Message)
        self.messages[self._get_next_msg_id()] = message
        
    def delete_message_from_topic(self, msg):
        assert isinstance(msg, Message)
        del self.messages[msg.id]
        
def get_all_topics():
    return _topics.values()

def get_topic(id):
    return _topics[id]
        
def delete_topic(topic):
    del _topics[topic.id]
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

def get_user(username):
    return _users.get(username)         # return None if no such user

def get_all_users():
    return _users.values()

def delete_user(user):
    del _users[user.username]
    del _user_ids[user.id]
