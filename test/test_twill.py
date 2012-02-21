import os

filedir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
testdir = os.path.dirname(__file__)+"\\twill\\"

def run_server(PORT=None):
    import time, tempfile, sys, subprocess
    global _server_url
    global filedir

    if PORT is None:
        PORT = 8000

    print "Using port", PORT
        
    outfd = open('log.txt', 'w')
    #outfd = tempfile.mkstemp('meeptest')[0]
    print 'STARTING:', sys.executable, filedir+'/serve.py', os.getcwd()
    process = subprocess.Popen([sys.executable, '-u', filedir+'/serve.py'],
                               stderr=subprocess.STDOUT,
                               stdout=outfd)
   
    time.sleep(2)

    _server_url = 'http://localhost:%d/' % (PORT,)
    
#I know I need to add this, but right now it won't do anything.
"""
def kill_server():
    global _server_url
    if _server_url != None:
       try:
          fp = urllib.urlopen('%sexit' % (_server_url,))
       except:
          pass

    _server_url = None
"""

def test():
    import twill
    global _server_url
    global testdir
    run_server(8000)
    twill.execute_file(testdir+"test_create_account.twill", initial_url=_server_url)
    twill.execute_file(testdir+"test_logout.twill", initial_url=_server_url)
    twill.execute_file(testdir+"test_login.twill", initial_url=_server_url)
    twill.execute_file(testdir+"test_add_topic.twill", initial_url=_server_url)
    twill.execute_file(testdir+"test_add_message.twill", initial_url=_server_url)
    twill.execute_file(testdir+"test_delete_message.twill", initial_url=_server_url)
    twill.execute_file(testdir+"test_delete_topic.twill", initial_url=_server_url)
    ###
    #   TODO: kill server somehow
    ###

    