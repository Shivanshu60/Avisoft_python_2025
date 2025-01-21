# printing data
print("Hello")


# variable creation
name = "shivanshu"

# Concatenation of string
print(name+ " Good Morning")

# printing selected data
print(name[2])


# Input (to take data from user)
name = input('Input your name: ')
age = input("Enter your age: ")

print("Your name is ", name ,"and age is ", age)


# Simple Word replacement 

sentence = input("Enter your sentence: ")
print('Your sentence is : ',sentence)
word1 = input("Enter word to replace: ")
word2 = input("Enter the new word: ")
new_Sentence = sentence.replace(word1, word2)
print("New sentence is : ", new_Sentence)