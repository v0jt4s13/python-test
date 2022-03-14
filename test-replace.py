
a = str(input(''))
b = ''
for x in a:
  if x.isupper():
    b+= '_'
  else:
    b+= x
print(b)