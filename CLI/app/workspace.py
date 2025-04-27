namespace = {}

def set_variable(name, value):
    namespace[name] = value

def get_variable(name):
    return namespace.get(name)

def get_all_variables():
    return namespace
