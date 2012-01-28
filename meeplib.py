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
           'User', 'get_user', 'get_all_users', 'delete_user', 'Thread']

###
# internal data structures & functions; please don't access these
# directly from outside the module.  Note, I'm not responsible for
# what happens to you if you do access them directly.  CTB

# a dictionary, storing all threads by a (unique, int) ID -> Thread object.
_threads = {}

def _get_next_thread_id():
    if _threads:
        return max(_threads.keys()) + 1
    return 0

# a dictionary, storing all users by a (unique, int) ID -> User object.
_user_ids = {}

# a dictionary, storing all users by username
_users = {}

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
    def __init__(self, post, author):
        self.post = post
        # is later reassigned by Thread
        self.id = 0

        assert isinstance(author, User)
        self.author = author

def get_all_threads(sort_by='id'):
    return _threads.values()

def get_thread(id):
    return _threads[id]

def delete_message(msg):
    assert isinstance(msg, Message)
    del _messages[msg.id]

###

class Thread(object):
    """
    Thread object, consisting of a simple dictionary of Message objects.
    Allows users to add posts to the dictionary.
    New messages must be of an object of type "Message".
    """

    def __init__(self, title):
        # a dictionary, storing all messages by a (unique, int) ID -> Message object.
        self.posts = {}
        self.save_thread()
        self.title = title

    def save_thread(self):
        self.id = _get_next_thread_id()
        _threads[self.id] = self

    def add_post(self, post):
        assert isinstance(post, Message)
        post.id = self.get_next_post_id()
        self.posts[post.id] = post
        
    def delete_post(self, post):
        assert isinstance(post, Message)
        del self.posts[post.id]
        # if there are no more posts in self.posts, delete the self Thread object and the reference to the thread in _threads
        if not self.posts:
            del _threads[self.id]
            del self
            
    def get_post(self, id):
        return self.posts[id]

    def get_next_post_id(self):
        if self.posts:
            return max(self.posts.keys()) + 1
        return 0

    def get_all_posts(self, sort_by = 'id'):
        return self.posts.values()

        

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
