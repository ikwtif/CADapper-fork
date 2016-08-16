#import time



from datetime import datetime


#print(time.strftime("%Y%m%d"))



now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
print(now)


#print(datetime.date(1999,11,4))


print(datetime.now())
