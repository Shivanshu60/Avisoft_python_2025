a = input("Enter the number: ")
print(f"Multiplaication table of {a} is : ")

try:
    for i in range(1, 11):
        print(f"{int(a)} X {i} = {int(a)*i}")
except Exception as e:
    print("Invalid input!!!")
finally:
    print("Execution completed")