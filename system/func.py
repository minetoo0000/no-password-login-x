import string;
import random;
from django.utils import timezone;

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