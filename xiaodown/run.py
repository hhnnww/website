import sys
import dribbble
import time
import gc

while True:
    # 开始采集dribbble
    dribbble.run()
    gc.collect()
    time.sleep(60*60*4) 