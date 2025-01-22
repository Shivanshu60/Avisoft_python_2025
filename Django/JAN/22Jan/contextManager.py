with open('sample.txt', 'r') as file:
    content = file.read()
    print(file.closed)

print(file.closed)  #outside with file is automatically closed

# other usage of context manager:
# - file handling
# - db conn.
# - thread lock
# - network conn 

