import time

def thetime():
    return str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+': '