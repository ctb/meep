import os
import twill


#need to remove backup file before twill tests
try:
    os.remove('meepBackup.txt')
except:
    pass



twill.execute_file("test_add_message.twill", initial_url="http://localhost:8000")
twill.execute_file("test_create_response.twill", initial_url="http://localhost:8000")
twill.execute_file("test_create_user.twill", initial_url="http://localhost:8000")
twill.execute_file("test_delete_response.twill", initial_url="http://localhost:8000")
twill.execute_file("test_initial_login.twill", initial_url="http://localhost:8000")
twill.execute_file("test_initial_logout.twill", initial_url="http://localhost:8000")
twill.execute_file("test_logged_in_postings.twill", initial_url="http://localhost:8000")
twill.execute_file("test_not_logged_in_postings.twill", initial_url="http://localhost:8000")