import socketserver, os


def parse_first_line(first_line):
    '''
    1. Split first line into verb, resource and protocol
    return as a dictionary
    e.g.: GET / HTTP/1.1
    {
        'verb': 'GET',
        'resource': '/',
        'protocol', 'HTTP/1.1'   
    }
    '''
    first_line.split()[0]
    dict = {'verb':first_line.split()[0],
            'resource': first_line.split()[1],
            'protocol': first_line.split()[2]}
    print(dict)

# parse_first_line()



def parse_headers(request_str):
    '''
    Read all headers (multiline) and parse them into dict.
    E.g.:
    Host: localhost:8080
    User-Agent: HTTPie/2.6.0
    Accept-Encoding: gzip, deflate
    returns 
    {
        'Host': 'localhost:8080',
        'User-Agent': 'HTTPie/2.6.0',
        'Accept-Encoding': 'gzip, deflate'
    }
    '''
    # split given request to single lines
    lst = request_str.split("\n")

    request_dict = {}
    i = 0

    # for every line split it into header and it's value
    while i != len(lst):

        # split into two
        temp = lst[i].split(" ", 1)

        # append to dict
        request_dict[temp[0]] = temp[1]

        i += 1


    print(request_dict)
# parse_headers()



def identify_resource(public_html, resource):
    '''
    Return path to file at specific resource. eg:
    '/index.html' -> public_html/index.html
    '/' -> public_html/index.html
    '/blog' -> public_html/blog/index.html
    '/blog/index.html' -> public_html/blog/index.html
    '/nonexisting' -> raise exception        
    '''

    # given that resource starts with /
    if "index.html" in resource:
        resource_path = f"{public_html}{resource}"

    elif "index.html" not in resource:
        resource_path = f"{public_html}{resource}\index.html"


    # does given path even lead to any existing object?
    try:
        # get path to main directory and the requested file/dir
        dir_path = os.path.dirname(os.path.realpath(__file__))+"\\"+public_html
        full_path = dir_path+resource

        if os.path.exists(full_path):
            print(resource_path)
            
        else:
            print (f"Error with {resource_path}")
        

    except: #find specific error!
        print("Path could not be found")

# identify_resource()



def read_resource(path):
    '''
    Read content of the resource (path) and return it
    '''
    # clean path from 'http' and host
    path = path.split(" ", 2)[2]

    print(path)
    
# read_resource()



def build_status_line(status_code):
    '''
    For supported status codes build proper http status line
    eg:
    200 -> HTTP/1.1 200 OK
    404 -> HTTP/1.1 404 Not Found
    500 -> HTTP/1.1 500 Internal Server Error
    '''

    if status_code == "200":
        print("HTTP/1.1 200 OK")

    elif status_code == "404":
        print("HTTP/1.1 404 Not Found")

    elif status_code == "500":
        print("HTTP/1.1 500 Internal Server Error")

    else:
        print(f"Error code '{status_code}' not found.")

# status()



def build_resposne_headers(resource_len):
    '''
    Always include Keep-alive: Close
    Alawys include Server: http_serv
    Include Content-Length header
    '''
    
    print (f"Keep-alive: Close",
    "Server: http_serv",    #?change to name of the dir instead of hardcode
    "Content-Length: {resource_len}")
    
#build_resposne_headers(res)



class HttpServer(socketserver.BaseRequestHandler):
    def handle(self):
        print('Handling request...')

        data = self.request.recv(4096)
        print('Receive data')
        print(data.decode())

        response = 'HTTP/1.1 204 No Content\r\n' # CRLF \r\n \n LF

        self.request.sendall(response.encode())

with socketserver.TCPServer(('localhost', 8080), HttpServer) as server:
    server.serve_forever()