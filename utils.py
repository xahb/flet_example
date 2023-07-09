def list_to_string(lst):
    string = ''
    for element in lst:
        string += str(element)
    return string


def hash_id(lst):
    from hashlib import sha224 
    string = list_to_string(lst)
    string = string.encode()
    return sha224(string).hexdigest()


def list_to_string2(lst):
    return str(lst).replace('[','{').replace(']','}')
