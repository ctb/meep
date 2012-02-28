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
           'User', 'get_user',
           'get_all_users', 'delete_user', 'is_user']

###
# internal data structures & functions; please don't access these
# directly from outside the module.  Note, I'm not responsible for
# what happens to you if you do access them directly.  CTB

# a dictionary, storing all messages by a (unique, int) ID -> Message object.
_messages = {}

# a dictionary, storing all users by a (unique, int) ID -> User object.
_user_ids = {}

# a dictionary, storing all users by username
_users = {}

def _getFileName():
    return 'meepBackup.txt'

def _backup_meep():
    meepBackup = open(_getFileName(), 'w')
    pickle.dump(_users, meepBackup)
    pickle.dump(_user_ids, meepBackup)
    pickle.dump(_messages, meepBackup)
    meepBackup.close()
      
def _load_backup():
    global _messages, _users, _user_ids
    meepBackup = open(_getFileName(), 'r')
    _users = pickle.load(meepBackup)
    _user_ids = pickle.load(meepBackup)
    _messages = pickle.load(meepBackup)
    meepBackup.close()

def _get_root_messages():
    rootMessages = []
    for m in _messages.values():
        if m.parentPostID == -1:
            rootMessages.append(m)
    return rootMessages

def _get_next_message_id():
    if _messages:
        return max(_messages.keys()) + 1
    return 0

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
    def __init__(self, title, post, author, parentPostID):
        self.title = title
        self.post = post
        assert isinstance(author, User)
        self.author = author
        self.parentPostID = parentPostID
        self.children = {}
        if parentPostID == -1:
            self._save_message()
        else:
            self.id = _get_next_message_id()
            _messages.get(parentPostID).children[self.id] = self
            _messages[self.id] = self    
        _backup_meep()
        
    def __cmp__(self, other):
        if (other.title != self.title or
            other.post != self.post or
            other.author != self.author or
            other.parentPostID != self.parentPostID):
            return -1
        else:
            return 0

    def _save_message(self):
        self.id = _get_next_message_id()
        
        # register this new message with the messages list:
        _messages[self.id] = self  
        

def build_tree(children):
    tree = []
    for c in children:
        tree.append(c)
        tree += build_tree(c.children.values())
 
    return tree

def get_all_messages():
    return build_tree(_get_root_messages())
    
def get_message(id):
    return _messages[id]

def delete_message(msg):
    assert isinstance(msg, Message)
    for c in msg.children.values():
        delete_message(c)
    
    if msg.parentPostID == -1:
        del _messages[msg.id]
    else:
        del _messages[msg.parentPostID].children[msg.id]
        del _messages[msg.id]
    _backup_meep()

###

class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password    
        self._save_user()
        
    def __cmp__(self, other):
        if (other.username != self.username or other.password != self.password):
            return -1
        else:
            return 0

    def _save_user(self):
        self.id = _get_next_user_id()
        _user_ids[self.id] = self
        _users[self.username] = self
        _backup_meep()

def get_user(username):
    return _users.get(username)         # return None if no such user

def get_all_users():
    return _users.values()

def delete_user(user):
    del _users[user.username]
    del _user_ids[user.id]
    
