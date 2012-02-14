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

def cookie_expiration_date(numdays):
    # FROM http://python.6.n6.nabble.com/How-to-Delete-a-Cookie-td1528033.html 
    """
    Returns a cookie expiration date in the required format.
    `expires` should be a string in the format "Wdy, DD-Mon-YY HH:MM:SS GMT" 
    NOTE!  Must use [expires] because earlier IE versions don't support [max-age].
    A negative input value will delete the cookie 
    """ 
    from datetime import date, timedelta 
    new = date.today() + timedelta(days = numdays) 
    return new.strftime("%a, %d-%b-%Y 23:59:59 GMT") 