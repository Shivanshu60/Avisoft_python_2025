# def div(a,b):
#     if a<b:
#         a,b = b,a
    
#     print(a/b)

# div(4,2)
# div(2,4)

# decorators : when we don't have access to the var/function &  wants do some condition based task in our func then we use decorators.
# or 
# It is a function that takes another function as argument and returns a function


def div(a,b):
    print(a/b)

def decorator(func):
    print("Execution started...")

    def wrapper(a,b):
        if a<b:
            a,b = b,a
    
        return func(a,b)
    
    print("Execution completed...")
    return wrapper

div1 = decorator(div)

div1(2,4)
