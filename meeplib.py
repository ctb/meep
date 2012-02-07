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
import pickle
###
# internal data structures & functions; please don't access these
# directly from outside the module.  Note, I'm not responsible for
# what happens to you if you do access them directly.  CTB

# a dictionary, storing all messages by a (unique, int) ID -> Message object.
_messages = {}
_replies = {}
_words={}
_search=True
_searchIDs={}
        
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
        return int(max(_user_ids.keys())) + 1
    return 0

def _reset():
    """
    Clean out all persistent data structures, for testing purposes.
    """
    global _messages, _users, _user_ids, _replies
    _messages = {}
    _users = {}
    _user_ids = {}
    _replies = {}
    

###

class Message(object):
    """
    Simple "Message" object, containing title/post/author.

    'author' must be an object of type 'User'.
    
    """
    def __init__(self, title, post, author):
        self.title = title
        self.post = post
        #self.parent = parent

       # assert isinstance(author, User)
        self.author = author

        self._save_message()
        add_message_to_dict(self)

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
    remove_message_from_dict(msg)
    del _messages[msg.id]
    
def add_reply(message_id, reply):
    if _replies.has_key(message_id):
        _replies[message_id].append(reply)        
    else:
        _replies[message_id] = [reply]

def get_replies(message_id):
    if _replies.has_key(message_id):
        print _replies
        return _replies[message_id]
    else:
        return -1
def add_message_to_dict(msg):
    print "add_message_to_dict"

    print "My message id"+ str(msg.id)
    print type(msg.id)
    message=_messages[msg.id]
    wordset=set()
    thePost=message.post.split()
    theReply = get_replies(msg.id)
    print theReply
    if theReply!=-1:
        theReply = message.post.split()
        for word in theReply:
            wordset.add(word)
    for word in thePost:
        wordset.add(word)
    theTitle=message.title.split()
    for word in theTitle:
        wordset.add(word)
    
    print "THE WORDSET"
    print wordset
    for word in wordset:
        if word not in _words:
            temp=list()
            temp.append(msg.id)
            _words[word]=temp
        else:
            currentValue=_words[word]
            currentValue.append(msg.id)
            print "CURRENT VALUE"
            
            _words[word]=currentValue
            print _words[word]

    return True

def remove_message_from_dict(msg):
    print "remove_message_from_dict"

    message=_messages[msg.id]
    wordset=set()
    thePost=message.post.split()
    for word in thePost:
        wordset.add(word)
    theTitle=message.title.split()
    for word in theTitle:
        wordset.add(word)
    for word in wordset:
        currentValue=_words[word]
        currentValue.remove(msg.id)
        _words[word]=currentValue
    return True

def search_message_dict(text):
    print "search_message_dict"
    print text
    text=text.split()
    searchSet=set()
    resultIDSet=set()
    for word in text:
        searchSet.add(word)
    for word in searchSet:
        if word in _words:
            for msgID in _words[word]:
                resultIDSet.add(msgID)

    print "THE SEARCH RESULTS"
    for msgID in resultIDSet:
        print msgID
    _searchIDs["test"]=resultIDSet
    print _searchIDs
    return resultIDSet

def get_search_results():
    print "get_search_results"
    return _searchIDs["test"]
def save_message():
    filename = 'posts.pickle'
    fp = open(filename, 'w')
    obj=[]
    for m in _messages:
        m=get_message(m)
        try:
            obj.append(("Message",m.title, m.post, m.author.username, m.id))
        except:
            obj.append(("Message",m.title, m.post, m.author, m.id))
    pickle.dump(obj, fp)
    fp.close()
    
    
def save_reply():
    filename = "replies.pickle"
    obj=[]
    fp = open(filename, 'w')
    for r in _replies:
        obj.append((r,_replies[r]))
    pickle.dump(obj, fp)
    fp.close()
    
def load():
    filename = 'posts.pickle'
    fp = open(filename)
    obj = pickle.load(fp)
    for i in obj:
        if i[0]=="Message":
            Message(i[1], i[2], i[3])
    fp2=open("replies.pickle")
    obj=pickle.load(fp2)
    print "REPLY OBJ", obj
    h=0
    for reply in obj:
        print "REPLY", reply
        i=0
        for msg in reply[1]:
            add_reply(reply[0],reply[1][i])
            i+=1
        h+=1
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
