# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/10/9 9:47 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_12_12.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

'''
def countdown(n):
    while n>0:
        print("befor,t_minus",n)
        yield
        print("after,t_minus",n)
        n -= 1
    print("blasoff")

def countup(n):
    x=0
    while x < n:
        print("count up",x)
        yield
        x += 1

x=countdown(10)  #生成器可以赋值
next(x)
next(x)  #next还是一样的遇到yield就暂停。下一个next继续执行
'''


from collections import deque
'''
class ActorScheduler:
    def __init__(self):
        self._actors={}
        self._msg_queue=deque()

    def new_actor(self,name,actor):
        self._msg_queue.append((actor,None))
        self._actors["name"]=actor


    def send(self,name,msg):
        actor=self._actors.get(name)
        if actor:
            self._msg_queue.append((actor,msg))

    def run(self):
        while self._msg_queue:
            actor,msg=self._msg_queue.popleft()
            try:
                actor.send(msg)
            except StopIteration: pass

if __name__ == "__main__":
    def printer():
        while True:
            print("before,printer")
            msg=yield
            print("after,printer")
            print("Got:",msg)

    def counter(sched):
        while True:
            print("before,counter")
            n=yield
            print("after,counter",n)
            if n==0:break
            sched.send("printer",n)
            sched.send("counter",n-1)

    sched=ActorScheduler()
    sched.new_actor("printer",printer())
    sched.new_actor("counter",counter(sched))
    sched.send("counter",10)
    sched.run()




class ActorScheduler:
    def __init__(self):
        self._actors = { }          # Mapping of names to actors
        self._msg_queue = deque()   # Message queue

    def new_actor(self, name, actor):
        '''
        Admit a newly started actor to the scheduler and give it a name
        '''
        self._msg_queue.append((actor,None))
        self._actors[name] = actor

    def send(self, name, msg):
        '''
        Send a message to a named actor
        '''
        actor = self._actors.get(name)
        if actor:
            self._msg_queue.append((actor,msg))

    def run(self):
        '''
        Run as long as there are pending messages.
        '''
        while self._msg_queue:
            actor, msg = self._msg_queue.popleft()
            try:
                 actor.send(msg)
            except StopIteration:
                 pass

# Example use
if __name__ == '__main__':
    def printer():
        while True:
            print("before,printer")
            msg = yield
            print("after,printer")
            print('Got:', msg)

    def counter(sched):
        while True:
            # Receive the current count
            print("before,counter")
            n = yield
            print("after,counter", n)
            if n == 0:
                break
            # Send to the printer task
            sched.send('printer', n)
            # Send the next count to the counter task (recursive)

            sched.send('counter', n-1)

    sched = ActorScheduler()
    # Create the initial actors
    sched.new_actor('printer', printer())
    sched.new_actor('counter', counter(sched))

    # Send an initial message to the counter to initiate
    sched.send('counter', 10)
    sched.run()
'''
    #666

from collections import deque
from select import  select
from socket import socket,AF_INET,SOCK_STREAM
import time


#  image  task  a  generator func
class Scheduler:
    def __init__(self):
        self._numtasks=0
        self._ready=deque()
        self._read_waiting={}
        self._write_waiting={}

    def new(self,task):
        self._ready.append((task,None))
        self._numtasks += 1

    def add_ready(self,task,msg=None):
        self._ready.append((task,msg))

    def _read_wait(self,fileno,evt,task):
        self._read_waiting[fileno] = (evt,task)

    def _write_wait(self,fileno,evt,task):
        self._write_waiting[fileno] = (evt,task)

    def _iopoll(self):
        rset,wset,eset=select(self._read_waiting,self._write_waiting,[])
        for r in rset:
            evt,task=self._read_waiting.pop(r)
            evt.handle_resume(self,task)

        for w in wset:
            evt,task=self._write_waiting.pop(w)
            evt.handle_resume(self,task)

    def run(self):
        while self._numtasks:
            if not self._ready:
                self._iopoll()
            task,msg=self._ready.popleft()

            try:
                r=task.send(msg)
                if isinstance(r,YieldEvent):
                    r.handle_yield(self,task)
                else:
                    raise RuntimeError("unrecognized yield event")
            except StopIteration:
                self._numtasks -= 1

class YieldEvent:
    def handle_yield(self,sched,task): ...
    def handle_resume(self,sched,task): ...


class ReadSocket(YieldEvent):
    def __init__(self,sock,nbytes):
        self.sock=sock
        self.nbytes=nbytes

    def handle_yield(self,sched,task):
        sched._read_wait(self.sock.fileno(),self,task)

    def handle_resume(self,sched,task):
        data=self.sock.recv(self.nbytes)
        sched.add_ready(task,data)


class WriteSocket(YieldEvent):
    def __init__(self,sock,data):
        self.sock=sock
        self.data=data

    def handle_yield(self,sched,task):
        sched._read_wait(self.sock.fileno(),self,task)

    def handle_resume(self,sched,task):
        nsent=self.sock.send(self.data)
        sched.add_ready(task,nsent)

class AcceptSocket(YieldEvent):
    def __init__(self,sock):
        self.sock=sock

    def handle_yield(self,sched,task):
        sched._read_wait(self.sock.fileno(),self,task)

    def handle_resume(self,sched,task):
        r=self.sock.accept()
        sched.add_ready(task,r)



class Socket(object):
    def __init__(self,sock):
        self._sock=sock

    def recv(self,maxbytes):
        return ReadSocket(self._sock,maxbytes)

    def send(self,data):
        return WriteSocket(self._sock)

    def accept(self):
        return AcceptSocket(self._sock)

    def __getattr__(self, item):
        return getattr(self._sock,name)

if __name__=="__main__":
    def readline(sock):
        chars=[]
        while True:
            c=yield sock.recv(1)
            if not c:
                break
            chars.append(c)
            if c == b'\n':
                break
        return b''.join(chars)

    class EchoServer:
        def __init__(self,addr,sched):
            self.sched=sched
            sched.new(self.server_loop(addr))

        def server_loop(self,addr):
            s=Socket(socket(AF_INET,SOCK_STREAM))
            s.bind(addr)
            s.listen(5)
            while True:
                c,a=yield  s.accept()
                print("got connection from",a)
                self.sched.new(self.client_handler(Socket(c)))

        def client_handler(self,client):
            while True:
                line=yield  from readline(client)
                if not line:
                    break
                line = b'GOT:' + line
                while line:
                    nsent=yield client.send(line)
                    line=line[nsent:]

            client.close()
            print("client closed")


