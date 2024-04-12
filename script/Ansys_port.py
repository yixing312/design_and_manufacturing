import time
import os

if __name__ == "__main__":
    while 1:
        if os.path.exists("../data/task_queue.txt"):
            with open("../data/task_queue.txt", "r", encoding="utf8") as f:
                flines = f.readlines()
                task_queue = []
                for line in flines:
                    task = line[0:-1].split(",")
                    print(task)
                    task = [float(i) for i in task]
                    task_queue.append(task)
                # delay 10s
                time.sleep(1)
            os.remove("../data/task_queue.txt")
        else:
            print("任务队列文件不存在！")
            time.sleep(1)
