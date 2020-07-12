import time
import requests
def print_ts(message):
    print("[%s] %s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message))
def run(interval, command):
    while True:
        time.sleep(interval)
        req = requests.get('http://119.45.154.121:5000/index')
        print_ts(req.status_code)
if __name__=="__main__":
    interval = 450
    command = r"ls"
    run(interval, command)