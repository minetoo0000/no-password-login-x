import string;
import random;
from django.utils import timezone;
import threading, time;

def random_str(
  length:int,
  letters:str=string.punctuation+string.digits+string.ascii_letters
)->str:
  result:str = "";
  for _ in range(length):
    result += random.choice(letters);
  return( result );

def token()->str:
  return( random_str(128) );
def id()->str:
  return random_str(128, string.ascii_letters+string.digits);
def lifetime():
  return( timezone.now()+timezone.timedelta(minutes=5) );

## 출처 : https://stackoverflow.com/a/48709380
class setInterval():
    def __init__(self,interval:float,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()