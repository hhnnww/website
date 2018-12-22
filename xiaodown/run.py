import sys
sys.path.append('../xiaodown/')
import dribbble
import time
import gc

x = 1
while True:
    # 采集dribbble
    dribbble.run()
    gc.collect()
    time.sleep(10)

    #