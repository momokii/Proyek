import datetime
from models import *

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print(type(get_now_time()))