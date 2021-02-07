import os

file = 'test_schedule.inc'
if os.path.exists(file):
    with open(file,encoding="utf-8") as f:
        lines = f.readlines()
        print(lines)
        f.close()
