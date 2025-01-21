# LIST => Mutable, Different datatype possible
countries = ['shivanshu', 'sawan']
print(countries[0:])
print(len(countries))

# two ways of creating a list 

list(('shivanshu', 'sawan'))
['shivanshu', 'sawan']

#inserting new item
list.insert(1, 'cherry')


# TUPLE
three_number = (1, 2, 3, 4, 5, True)
print(type(three_number))

#################################################
# function 

def greetings_function(*name):
    print("welcome " + name[1] )

greetings_function('John', 'Tim', 'Tom')

#addition function
def add(num1, num2):
    return num1+num2

print(add(2,4))


#################################################
# DICTIONARY 
my_dict = {
    'name': 'African',
    'name2': 'African',
    'age': 21,
    'friends': ['A', 'B'],
    'Qualification': 'College'
}

print(my_dict)

for letter in "Hello":
    print(letter)

mylist = ['ji','jo', 'ju']

for values in mylist:
    print(values)

    
