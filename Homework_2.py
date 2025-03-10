#Task 1
import random  # Import the random module to generate random numbers

# Create an empty list to hold the random dictionaries
random_dicts_list = []

# Determine the random number of dictionaries (between 2 to 10)
num_dicts = random.randint(2, 10)

for _ in range(num_dicts):
    # Create a single dictionary
    random_dict = {
        # Randomly select a letter (from 'a' to 'z') as a key
        random.choice('abcdefghijklmnopqrstuvwxyz'): random.randint(0, 100)
        # Repeat this process for a random number of key-value pairs (between 1 and 26)
        for _ in range(random.randint(1, 26))
    }
    # Append the generated dictionary to the list
    random_dicts_list.append(random_dict)

# Print the final list of random dictionaries
print(random_dicts_list)

#Task 2
# Example of a previously generated list of dictionaries
random_dicts_list = [
    {'a': 5, 'b': 7},
    {'a': 3, 'c': 35, 'g': 42},
    {'a': 10, 'b': 2, 'x': 50}
]

# Initialize a new dictionary to keep track of the merged results
merged_dict = {}

# Iterate through each dictionary in the list with its index (1-based for renaming)
for dict_index, current_dict in enumerate(random_dicts_list, start=1):
    # Iterate through the key-value pairs in the current dictionary
    for key, value in current_dict.items():
        if key not in merged_dict:
            # If the key is not in the merged dictionary, add it with its corresponding value and origin index
            merged_dict[key] = (value, dict_index)
        else:
            # If the key is already in the merged dictionary, compare the values
            existing_value, existing_dict_index = merged_dict[key]
            if value > existing_value:
                # Update the merged dictionary with the new maximum value and the corresponding dictionary index
                merged_dict[key] = (value, dict_index)

# Prepare the final dictionary with renamed keys where necessary
final_dict = {}

for key, (value, dict_index) in merged_dict.items():
    # Check if the key exists in multiple dictionaries and needs renaming
    is_duplicate = sum(key in dct for dct in random_dicts_list) > 1
    if is_duplicate:
        # Rename the key by appending the dictionary index where the maximum value was found
        final_dict[f"{key}_{dict_index}"] = value
    else:
        # If the key is unique, add it as is
        final_dict[key] = value

# Print the final merged dictionary
print(final_dict)
