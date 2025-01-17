def binary(arr, low, high, x):
    if high > low:
        mid = (low + high) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binary(arr, low, mid -1, x)
        else:
            return binary(arr, mid+1, high, x)
    else:
        return -1
        
arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
x = 60
result = binary(arr, 0, len(arr)-1,x)
if(result != -1):
    print("Element is present at index %d" % result)
else:
    print("Element is not present in array")