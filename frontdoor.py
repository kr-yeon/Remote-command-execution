import socket
from threading import Thread
import time

class Server:
    def __init__(self):
        self.sock=socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.selected=None
        self.clients=[]

    def setbind(self, ip="0.0.0.0", port=3000):
        self.sock.bind((ip, port))
        self.sock.listen()
        return True

    def client_receiver(self):
        while True:
            conn, addr = self.sock.accept()
            self.clients.append({"sock":conn, "addr":addr})

    def startloop(self):
        t=Thread(target=self.client_receiver)
        t.daemon=True
        t.start()

    def recvline(self, conn):
        buf=b""
        while True:
            t = conn.recv(1)
            if t == b"\n":
                return buf
            buf+=t

    def clientlist(self):
        arr=[]
        if len(self.clients)==0:
            return "No clinet"
        else:
            for i, v in enumerate(self.clients):
                arr.append("{} {}".format(i, v["addr"]))
            return arr

    def select(self, number=0):
        self.selected = self.clients[number]
        print("selected ", self.selected["addr"])

    def shutdown(self):
        if self.isselect():
            print("shutdown {}".format(self.selected["addr"]))
            print("shutdown")
            self.selected["sock"].send(b"shutdown\n")
            self.selected = None
        else:
            print("select frist")

    def isselect(self):
        if not self.selected:
            return False
        else:
            return True

    def send(self, msg):
        if self.isselect():
            self.selected["sock"].send("{}\n".format(msg).encode("utf-8"))
            print(self.recvline(self.selected["sock"]).decode())
        else:
            print("select frist")

    def check(self):
        for i in self.clients:
            try:
                i["sock"].send(b"ping\n")
            except:
                if self.selected == i:
                    self.selected = None
                self.clients.remove(i)

class Client:
    def __init__(self):
        self.sock = None
        self.ono=False

    def setconnect(self, ip="127.0.0.1", port=3000):
        self.ip=ip
        self.port=port

    def recvline(self, conn):
        buf=b""
        while True:
            t = conn.recv(1)
            if not t:
                raise Exception("disconnect")
            if t == b"\n":
                return buf
            buf+=t

    def recv(self):
        while True:
            time.sleep(0.8)
            print("connect try")
            try:
                self.sock = socket.socket()
                self.sock.connect((self.ip, self.port))
                print("connected")
                self.ono=True
                break
            except:
                print("connect error")
                pass
        while True:
            print("read..")
            recv = self.recvline(self.sock).decode("utf-8")
            yield recv

    def send(self, msg):
        try:
            self.sock.send("{}\n".format(msg).encode("utf-8"))
        except Exception as e:
            self.sock.send("{}\n".format(False).encode("utf-8"))
            print(e)

    def check(self):
        return self.ono
