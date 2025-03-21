import os
import signal
import time
from threading import Thread

log_file = 'all_log.log'


# https://www.geeksforgeeks.org/how-to-detect-file-changes-using-python/
def detect_file_changes(file_path, interval=1.):
    last_modified = os.path.getmtime(file_path)
    while True:
        current_modified = os.path.getmtime(file_path)
        if current_modified != last_modified:
            return True
        time.sleep(interval)


def run_cpp(start):
    new = f'./yes_output.sh "./../cluster/SVS-CPP/ndn-svs/build/examples/core {separate_state(start)}"'
    process = os.popen(new)
    return int(process.read())


def separate_state(state):
    s = ''
    for char in state:
        s += ' '
        s += char
    return s


def run_prober(probe):
    cmd = f'node ../cluster/SVS-TS/build/main.js {separate_state(probe)}'
    return run_cmd_prober(cmd)


# start background process with no output
# returns pid
def run_cmd_prober(cmd):
    # for prober
    new = f'./no_output.sh "{cmd}"'
    process = os.popen(new)
    return int(process.read())


def run_fetcher(starting, probing):
    process = os.popen(f'./fetch_data.sh {starting} {probing}')
    # basically a thread.join
    process.read()
    return


def run_test(start, probe):
    # clear cache
    os.popen("nfdc cs erase /").read()
    # os.popen("systemctl restart nfd").read()

    # start output monitor for file updates (background)
    thread = Thread(target=detect_file_changes, args=[log_file, 0.01])
    thread.start()

    # run implementation, save output to file
    cpp_pid = run_cpp(start)
    print(f'ran cpp\t{cpp_pid}')
    # time.sleep(0.01)

    # run ts prober, save pid
    prober_pid = run_prober(probe)
    print(f'ran prober\t{prober_pid}')

    # on file update,
    thread.join(timeout=3)
    print('got file update')

    #   run data fetcher, sending output to file
    print('run fetcher')
    run_fetcher(start, probe)

    #   kill implementation and prober
    print('kill cpp and prober')
    os.kill(cpp_pid, signal.SIGTERM)
    os.kill(prober_pid, signal.SIGTERM)
    print('finished')


if __name__ == '__main__':
    # global settings
    os.popen("nfdc strategy set /ndn/svs /localhost/nfd/strategy/multicast").read()
    os.popen("echo '' > saving.csv").read()
    for line in open('tests.all'):
        start, probe = line.split(' ')
        start = start.strip()
        # 12345 12346
        probe = probe.strip()
        print(f'running test: {start} {probe}')
        run_test(start, probe)
        time.sleep(0.5)
