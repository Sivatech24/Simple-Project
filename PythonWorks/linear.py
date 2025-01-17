def leanier(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1

arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
print("Enter a number to search: ")
x = int(input())
res = leanier(arr, x)
if(res != -1):
    print("element is present at index ",res)
else:   
    print("Element is not present in array")