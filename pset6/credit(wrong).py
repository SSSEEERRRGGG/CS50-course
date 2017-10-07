while True:
    n = input("Number: ")
    if int(n) > 0:
        break
    
lenght = len(n)    
if lenght<13 or lenght>16 or lenght==14:
    print("INVALID")
    #exit(0)

num = []
for i in range(lenght):
    num.append(n[i])
print(num)
summ = 0
j = 1
i1=lenght-1
while i1 >= 0:
    if j % 2 ==0:
        summ += int(num[i1])*2 % 10
        if int(num[i1])*2 >= 10:
            summ += 1
    else:
        summ += int(num[i1])
    j+=1
    i1-=1
    
if num[0]==3 and (num[1]== 4 or num[1] == 7) and summ % 10 == 0:
    print("AMEX")
elif num[0] == 5 and num[1] > 0 and num[1] < 6 and summ % 10 == 0:
    print("MASTERCARD")
elif (num[0] == 4 and sum % 10 == 0):
    print("VISA")
else:
    print("INVALID")

    

        