#!/usr/bin/env python
import subprocess
import time
import threading
import os


def kill_child(pid):
    process_list = subprocess.check_output(['ps', 'a', '-o', 'ppid,pid'])
    for line in process_list.split('\n'):
        pids = line.split()
        if len(pids) > 0:
            if pids[0] == str(pid):
                #print "Killing", pids[1]
                os.kill(int(pids[1]), 9)


class ExecThread(threading.Thread):

    def __init__(self, commands):
        threading.Thread.__init__(self)
        self.commands = commands
        self.stopthread = threading.Event()

    def run(self):
        self.proc = subprocess.Popen(self.commands, stdout=open('/dev/null'))
        #print "Starting", self.proc.pid

    def stop(self):
        kill_child(self.proc.pid)


pipelines = ['gst-launch v4l2src ! xvimagesink',
    'gst-launch v4l2src ! tee name=tv ! queue ! xvimagesink sync=false tv. !'
    + ' theoraenc ! queue ! oggmux ! filesink location=/tmp/test.ogg',

    'gst-launch v4l2src ! tee name=tv ! queue ! xvimagesink sync=false tv. !'
    + ' theoraenc ! queue ! oggmux ! filesink location=/dev/null',

    'gst-launch v4l2src ! videoscale ! video/x-raw-yuv,width=160,height=120 !'
    + ' tee name=tv ! queue ! xvimagesink sync=false tv. ! theoraenc ! queue !'
    + ' oggmux ! filesink location=/dev/null',

    'gst-launch v4l2src ! videoscale ! video/x-raw-yuv,width=320,height=240 !'
    + ' tee name=tv ! queue ! xvimagesink sync=false tv. ! theoraenc ! queue !'
    + ' oggmux ! filesink location=/dev/null',

    'gst-launch v4l2src ! videoscale ! video/x-raw-yuv,width=400,height=300 !'
    + ' tee name=tv ! queue ! xvimagesink sync=false tv. ! theoraenc ! queue !'
    + ' oggmux ! filesink location=/dev/null',

    'gst-launch v4l2src ! videoscale ! video/x-raw-yuv,width=400,height=300 !'
    + ' tee name=tv ! queue ! xvimagesink sync=false tv. ! vp8enc speed=2 ! '
    + ' queue ! oggmux ! filesink location=/dev/null']

for pipeline in pipelines:
    commands = ['time']
    commands.extend(pipeline.split())
    print pipeline
    th = ExecThread(commands)
    th.run()
    time.sleep(30)
    th.stop()
    time.sleep(1)
    print
