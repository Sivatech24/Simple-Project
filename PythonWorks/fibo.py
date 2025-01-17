def fibo(n):
    n1 = 0
    n2 = 1
    count = 0
    if n == 1:
        print(n1)
    else:
        while count < n:
            print(n1)
            n3 = n1 + n2
            n1 = n2
            n2 = n3
            count += 1

n = int(input("Enter a number: "))
fibo(n)
