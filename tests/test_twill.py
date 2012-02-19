import twill

twill.execute_file("tests/create_user.twill", initial_url="http://localhost:8000")
twill.execute_file("tests/message_add.twill", initial_url="http://localhost:8000")
twill.execute_file("tests/message_delete.twill", initial_url="http://localhost:8000")
twill.execute_file("tests/message_reply.twill", initial_url="http://localhost:8000")
