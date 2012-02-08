from Cookie import SimpleCookie

def make_set_cookie_header(name, value, path='/'):
    """
    Makes a 'Set-Cookie' header.
    
    """
    c = SimpleCookie()
    c[name] = value
    c[name]['path'] = path
    
    # can also set expires and other stuff.  See
    # Examples under http://docs.python.org/library/cookie.html.

    s = c.output()
    (key, value) = s.split(': ')
    return (key, value)
