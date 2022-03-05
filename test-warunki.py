
s1 = "1"
s2 = "2"
s3 = "3"

n1 = 1
n2 = 2
n3 = 3

l1 = [1, 2, 3]
l2 = [1, 2, 3]
l3 = [3, 2, 1]

ls1 = ["a","b","c"]
ls2 = ["c","b","a"]
ls3 = ["d","e","f"]


print(n1,'==',n1,'True') if n1 == n1 else print(n1,'==',n1,'False') 
print(n1,'is',n1,'True') if n1 is n1 else print(n1,'is',n1,'False') 
print(n1,'==',n2,'True') if n1 == n2 else print(n1,'==',n2,'False') 
print(n1,'is',str(n1)+''+str(n2),'True') if n1 is 12 else print(n1,'is',str(n1)+''+str(n2),'False')
print(n1,'is [',str(n1)+','+str(n2),'] True') if n1 is [1,2] else print(n1,'is [',str(n1)+','+str(n2),'] False')

print(s1,'==',s1,'True') if s1 == s1 else print(s1,'==',s1,'False') 
print(s1,'is',s1,'True') if s1 is s1 else print(s1,'is',s1,'False') 
print(s1,'==',s2,'True') if s1 == s2 else print(s1,'==',s2,'False') 
print(s1,'is',str(s1)+''+str(s2),'True') if s1 is 12 else print(s1,'is',str(s1)+''+str(s2),'False')
print(s1,'is [',str(s1)+','+str(s2),'] True') if s1 is [1,2] else print(s1,'is [',str(s1)+','+str(n2),'] False')

#if n1 is n1: print(n1,'is',n1,'True') 
#if n1 == n1: print(n1,'==',n1,'True') 

