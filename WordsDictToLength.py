# Given a list of words:
# words = ["apple", "banana", "kiwi", "cherry", "mango"]
# Create a dictionary that maps each word to its corresponding length.
# Example Output: ({"apple": 5, "banana": 6, "kiwi": 4, "cherry": 6, "mango": 5})

# define the list of fruits and an empty dictionary to store the results
fruits = ["apple", "banana", "kiwi", "cherry", "mango"]
fruits_length_dict = {}

# iterate through each fruit in the list and
# add an entry to the dictionary with the fruit as the key and its length as the value
for fruit in fruits:
    fruits_length_dict[fruit] = len(fruit)

# print the resulting dictionary
print(fruits_length_dict)
