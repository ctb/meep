from meep_example_app import MeepExampleApp, initialize
import datetime
from collections import deque


def main():
    initialize()
    app = MeepExampleApp()
    environ = {}

    # CTB: interesting choice to hardcode this stuff -- works, I guess!
    # bigger complaint is that this code isn't reusable for serve2!
    def custom_start_response(status, headers):
        print "HTTP/1.0", status
        print "Date:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        print "Server: CustomServer/0.1 Python/2.7"
        for header in headers:
            print header[0] + ":", header[1]
    
    file_name = raw_input("Please enter the request file's name: ")
    print
    f = open(file_name)

    response = ''
    queue = deque()
    for line in f:
        queue.append(line)
    f.close()

    new_line = queue.popleft()

    #Handle the first line
    line_array = new_line.split(" ")
    request_method = line_array[0]
    path_info_raw = line_array[1]
    server_protocol = line_array[2].strip("\n")
    
    #Get the query from the url_path
    path_list = path_info_raw.split("?")
    path_info = path_list[0]
    try:
        query_string = path_list[1]
        environ['QUERY_STRING'] = query_string
    except IndexError:
        #No query, do nothing
        print
    
    environ['REQUEST_METHOD'] = request_method
    environ['PATH_INFO'] = path_info
    environ['SERVER_PROTOCOL'] = server_protocol
    
    while(True):
        try:
            new_line = queue.popleft().split(":")
            if new_line[0] == 'cookie':
                environ['HTTP_COOKIE'] = new_line[1]
        except IndexError:
            break
    

    data = app(environ, custom_start_response)
    print data
    
main()
