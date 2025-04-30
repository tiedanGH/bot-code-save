from random import*
string="🀇🀈🀉🀊🀋🀌🀍🀎🀏🀐🀑🀒🀓🀔🀕🀖🀗🀘🀙🀚🀛🀜🀝🀞🀟🀠🀡🀀🀁🀂🀃🀆🀅🀄"
str=''.join([char*4 for char in string])
print(''.join(str[i] for i in sorted(sample(range(len(str)), 13))))
