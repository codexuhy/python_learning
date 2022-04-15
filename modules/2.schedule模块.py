import schedule
import time
import threading
import queue
def job():
    import os

    def fun():
        os.system("python3  /data/hongyuan/work/docker_dir/dev_car_jira_tool/test/aa.py")
    fun()

def job1():
    print("I'm working... in job1  start")
    time.sleep(15)
    print("I'm working... in job1  end")
def job2():
    print("I'm working... in job2")
# 1、schedule方法是串行的,会先执行完job1，再执行job2  
# schedule.every(2).seconds.do(job1)
# schedule.every(2).seconds.do(job2)

# 2、将上述方法改成多线程,但是会起很多个线程
# def run_threaded(job_func):
#      job_thread = threading.Thread(target=job_func)
#      job_thread.start()
# schedule.every(10).seconds.do(run_threaded,job1)
# schedule.every(10).seconds.do(run_threaded,job2)

# 3、为了对线程数量进行控制，可以采用如下方法
def worker_main():
    while 1:
        job_func = jobqueue.get()
        job_func()
jobqueue = queue.Queue()
# 5个线程
schedule.every(10).seconds.do(jobqueue.put, job2)
schedule.every(10).seconds.do(jobqueue.put, job2)
schedule.every(10).seconds.do(jobqueue.put, job2)
schedule.every(10).seconds.do(jobqueue.put, job2)
schedule.every(10).seconds.do(jobqueue.put, job2)

worker_thread = threading.Thread(target=worker_main)
worker_thread.start()


# 原文链接：https://blog.csdn.net/kamendula/article/details/51452352?spm=1001.2101.3001.6650.15&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-15.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-15.pc_relevant_default&utm_relevant_index=21
# schedule.every(2).seconds.do(job)# 每隔2s执行一次
# schedule.every(5).minutes.do(job)# 每隔5min执行一次
# schedule.every().hour.do(job) # 每隔1小时执行函数job
# schedule.every(2).hours.do(job)  #  每隔2h执行一次
# schedule.every().day.at("10:30").do(job)#每天的10点30执行函数job
# schedule.every().monday.do(job) #每周一执行函数job
# schedule.every().wednesday.at("14:15").do(job) #每周三下午2点15分执行函数job

if __name__ == '__main__':
    while True:
        schedule.run_pending()

# 按日期输出日志，如 nohup2022-04-15.out
# nohup python3 -u timed_task.py >> ./log/nohup`date +%Y-%m-%d`.out 2>&1