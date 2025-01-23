def divide(x, y): 
    try: 
        result = x // y 
    except ZeroDivisionError: 
        print(" You are dividing by zero ") 
    finally:
        print("completed")
  

divide(3, 2) 
divide(3, 0)