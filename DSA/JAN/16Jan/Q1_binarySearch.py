# Question1

''' 
Anchit is working on a project and he wants a getIndex() function. getIndex() function should return the index number of a value present inside a list of numbers and remove that value as well. He told his friend Juned to create this function.
Note: Use binary search algorithm to search the element in the list.


arr = [1, 3, 5, 6, 7, 8, 9]
Input = 6
Result = get_index(arr, Input)
Result = [1, 3, 5,  7, 8, 9]
'''

# Solution

def get_index(arr, target):

    #var declaration
    low, high = 0, len(arr) - 1
    
    # binary search 
    while (low <= high):
        mid = (low + high) // 2
        if (arr[mid] == target):
            arr.pop(mid)
            print("Index is:", mid)
            print("Array after removing element is: ", end=" ")
            return arr
        elif (arr[mid] < target):
            low = mid + 1
        else:
            high = mid - 1
    print("Target", target, "not found!!!")
    return arr

# Test case 
arr = [1, 3, 5, 6, 7, 8, 9]
input = 7
result = get_index(arr, input)
print(result)  




