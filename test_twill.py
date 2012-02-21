import twill

twill.execute_file("twill/test_1_login.twill", initial_url="http://localhost:8000")
twill.execute_file("twill/test_2_add_message.twill", initial_url="http://localhost:8000")
twill.execute_file("twill/test_3_message_ranks.twill", initial_url="http://localhost:8000")
twill.execute_file("twill/test_4_reply.twill", initial_url="http://localhost:8000")
twill.execute_file("twill/test_5_delete.twill", initial_url="http://localhost:8000")
