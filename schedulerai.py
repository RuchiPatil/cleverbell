
from ai_func import *
from comm_func import *
#scheduler ai
#from apscheduler.scheduler.background import BackgroundScheduler as s

def worker():
    i = 0
    while (True):
        print(f'{i}. do something ... ' + str(time.time()))
        time.sleep(5)
        i += 1
        if i > 5: break

#try get image and user in known encodings pool


#try looking for image to add

#try looking for image to detect

#----------------------------------------                       detect



t = threading.Thread(target=askforimage)
print(time.time())
t.start()
print(time.time())
