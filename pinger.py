import ping3
import netaddr
import sqlite3
import threading
import queue
import time

target_cidr = "10.0.56.0/24"
ping_delay = 2

pingQueue = queue.Queue(maxsize=1024)


def pQinsert(dstip: str, delay: float, timeout=0):
    pingQueue.put((dstip, delay, timeout), block=True, timeout=None)


def pQdequeue():
    try:
        conn = sqlite3.connect("pinger.db")
    except sqlite3.Error:
        raise Exception("Failed to connect database")
    while True:
        dstip, delay, timeout = pingQueue.get(block=True, timeout=None)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO detail(DstIP, Delay, Timeout) "
                       "VALUES('%s', '%s', '%s')" % (dstip, str(delay), str(timeout)))
        conn.commit()
        cursor.close()


class ping_thread(object):
    def __init__(self):
        self.queue = queue.Queue(maxsize=1024)

    def enqueue(self):
        while True:
            for ip in netaddr.IPNetwork(target_cidr):
                self.queue.put(str(ip), block=True, timeout=None)

    def ping(self):
        while True:
            ip = self.queue.get(block=True, timeout=None)
            delay = ping3.ping(ip, unit="ms", timeout=3, ttl=64)
            if delay is None:
                pQinsert(ip, 0.0, timeout=1)
            else:
                pQinsert(ip, delay)
            time.sleep(ping_delay)

    def start_ping(self):
        queue_thread = threading.Thread(target=self.enqueue, args=())
        queue_thread.daemon = True
        queue_thread.start()

        for i in range(0, 10):
            t = threading.Thread(target=self.ping, args=())
            t.daemon = True
            t.start()

        wait = queue.Queue(maxsize=16)
        wait.get(block=True, timeout=None)


if __name__ == "__main__":
    dequeue_thread = threading.Thread(target=pQdequeue, args=())
    dequeue_thread.daemon = True
    dequeue_thread.start()

    Ping = ping_thread()
    Ping.start_ping()



