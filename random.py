import threading

global x
x = 0
def foo(threadNum):
    global x
    for i in range(10):
        x += 1
        print("{}: {}".format(threadNum, x))

for i in range(10):
    thread = threading.Thread(target=foo, args=[i+1])
    thread.start()

# http://pythontutor.com/visualize.html#mode=edit 