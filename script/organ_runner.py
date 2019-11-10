import subprocess
import time
import urllib.request
import threading
import pyudev

#https://eli.thegreenplace.net/2017/interacting-with-a-long-running-child-process-in-python/

# jackd -d alsa -d hw:0 -p 256
# setBfreeUi
# a2jmidi_bridge
# git/hammond_on_electrix_tweaker/cpp/main
# /dev usb Tweaker hot plug
# connection router

#TODO: what is jack is already running?

class Process:
    def __init__(self, name, cmd):
        print("INIT:", name)
        self.cmd = cmd
        self.name = name
        self.running = False

    # STATIC
    def output_reader(self):
        for line in iter(self.proc.stdout.readline, b''):
            decoded_line = '{0}'.format(line.decode('utf-8'))
            print("  " + self.name + ":", decoded_line, end='')
            try:
                if (self.line_running in decoded_line):
                    print("  " + self.name + ":", "LINE RUNNING")
                    self.running = True
            except:
                pass

    def start_process(self):
        self.proc = subprocess.Popen(self.cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def stop_process(self):
        self.proc.terminate()
        try:
            self.proc.wait(timeout=0.2)
            print(self.name, '== subprocess exited with rc =', self.proc.returncode)
        except subprocess.TimeoutExpired:
            print(self.name, 'subprocess did not terminate in time')

    def start_process_output(self):
        self.proc_output = threading.Thread(target=self.output_reader)
        self.proc_output.start()

    def stop_process_output(self):
        self.proc_output.join()

    # DYNAMIC
    def start(self):
        print("STARTING:", self.name)
        self.running = False
        self.start_process()
        self.start_process_output()

    def stop(self):
        print("STOPING:", self.name)
        self.running = False
        self.stop_process()
        self.stop_process_output()

    def registerRunning(self, line):
        self.line_running = line

    def isRunning(self):
        return self.running

    def waitRunning(self):
        print("WAITING:", self.name)
        try:
            while (not self.isRunning()):
                pass
        except:
            print("Keyboard interrupt")

    def sendLine(self, line):
        lineout = line + "\n"
        self.proc.stdin.write(lineout.encode('utf-8'))
        self.proc.stdin.flush()


def detectTweaker():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    for device in monitor:
        print(repr(device))
    # For USB devices
    # monitor.filter_by(subsystem='usb')
    # OR specifically for most USB serial devices
    # monitor.filter_by(susbystem='tty')
    # for action, device in monitor:
        # vendor_id = device.get('ID_VENDOR_ID')
        # I know the devices I am looking for have a vendor ID of '22fa'
        # if vendor_id in ['200c']:
            # print('Detected {} for device with vendor ID {}'.format(action, vendor_id))

def setConnections():
    subprocess.Popen('jack_connect "a2j:tweaker [131] (capture): output" "setBfree DSP Tonewheel Organ:control"', shell=True)
    time.sleep(0.2)
    subprocess.Popen('jack_disconnect "a2j:Midi Through [14] (capture): Midi Through Port-0" "setBfree DSP Tonewheel Organ:control"', shell=True)
    time.sleep(0.2)
    subprocess.Popen('jack_disconnect "setBfree DSP Tonewheel Organ:notify" "a2j:Midi Through [14] (playback): Midi Through Port-0"', shell=True)
    time.sleep(0.2)

def killJack():
    subprocess.Popen('killall jackd', shell=True)
    time.sleep(0.2)

if __name__ == "__main__":
    # detectTweaker()

    killJack()

    jack = Process("jack", "jackd -d alsa -d hw:0 -p 256")
    jack.registerRunning("ALSA: use 2 periods for playback")

    a2j = Process("a2j", "a2jmidid")
    a2j.registerRunning("Bridge started")

    tweaker = Process("tweaker", "tweaker")
    tweaker.registerRunning("Press any key to exit")

    setbfree = Process("setbfree", "setBfreeUI")

    jack.start()
    jack.waitRunning()
    a2j.start()
    a2j.waitRunning()
    tweaker.start()
    tweaker.waitRunning()
    setbfree.start()
    time.sleep(0.5)
    setConnections()

    try:
        while True:
            pass
    except:
        pass

    setbfree.stop()
    tweaker.stop()
    a2j.stop()
    jack.stop()
