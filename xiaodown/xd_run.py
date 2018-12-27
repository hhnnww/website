import sys
import dribbble
import time
import gc

while True:
    # 采集dribbble
    dribbble.run()
    gc.collect()
    time.sleep(10)
