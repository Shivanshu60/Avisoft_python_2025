# Reading files 
coun_file = open('countries.txt', 'r')
print(coun_file.readable())

coun_file.close()

# Writing file 
coun_file = open('countries.txt', 'a')
coun_file.write('\n This is a new line')
print(coun_file.readable())

coun_file.close()