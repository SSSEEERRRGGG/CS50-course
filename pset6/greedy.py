while True:
    try:
        n = float(input('How much change is owed? '))
        if n >= 0.00:
            break
    except ValueError:
        exit(1)

counter = 0
n *= 100
amount = round(n)
    
while amount >= 25:
    counter+=1
    amount-=25
while amount >= 10:
    counter+=1
    amount-= 10
while amount >= 5:
    counter+=1
    amount-= 5
while amount >= 1:
    counter+=1
    amount-= 1
    
print(counter)
exit(0)

    