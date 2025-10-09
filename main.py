import datetime

s1 = input()
s2 = input()
date1 = datetime.datetime.strptime(s1, "%Y %m %d")
date2 = datetime.datetime.strptime(s2, "%Y %m %d")
delta = abs((date2 - date1).days)
print(delta)