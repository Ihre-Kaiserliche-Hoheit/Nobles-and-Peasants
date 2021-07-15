from datetime import datetime as d
import hashlib as hash

def get_time():
    """
    Gives the time in the following format:
        YEAR.MONTH.DAY HOUR:MINUTE:SECOND
    """
    time = d.now()
    t = str(time.strftime("%Y-%m-%d-%H:%M:%S"))
    return(t)

def convert_to_hash(_input, _length=None):
    _input = str(_input)
    if _length != None:
        output = int(hash.sha256(_input.encode('utf-8')).hexdigest(), 16) % 10**_length
    else:
        output = int(hash.sha256(_input.encode('utf-8')).hexdigest(), 16)
    return(output)

def pseudo_random_seed():
    seed = get_time()
    seed = convert_to_hash(seed)
    return(seed)
