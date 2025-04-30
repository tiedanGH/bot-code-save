from random import *
num,c=0,0
while c<5:
  if num==0: print('#新游戏 HP杀')
  num+=1 if randint(1,5)<=3 or num==0 else -1
  print(num,end='')
  if randint(1,10)==1 and num>5:
    num=0; print('\n房主不在，炸房吧', end='')
  if num==0: c+=1; print()
  if num==8: break
print('HP杀已经凉了' if c==5 else '\nHP杀启动！',end='')
