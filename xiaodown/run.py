from xiaodown import dribbble
import time
import gc

x = 1
while(x<2):

    dribbble.run()
    gc.collect()
    time.sleep(10)