import re


# Function to normalize letter cases for the text
def normalize_cases(text):
    sentences = re.split(r'(?<=[.\n])\s+', text.strip())  # Split by newlines and periods
    normalized_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()  # Remove extra whitespace
        if sentence:
            normalized_sentence = sentence[0].upper() + sentence[1:].lower()
            normalized_sentences.append(normalized_sentence)
    return " ".join(normalized_sentences)


# Function to fix 'iz' to 'is' when it is a mistake
def fix_iz_errors(text):
    return re.sub(r'\b[Ii][Zz]\b', 'is', text)


# Function to fix spacing issue between "Fix" and "is"
def fix_spacing(text):
    return re.sub(r'Fix“', 'Fix “', text)


# Function to add a sentence with the last words of each existing sentence
def add_last_words_sentence(text):
    sentences = re.split(r'(?<=[\.\!\?])\s+', text)  # Split into sentences
    last_words = [sentence.strip().split()[-1].strip(".").capitalize() for sentence in sentences if sentence.strip()]
    additional_sentence = " ".join(last_words) + "."
    return text + " " + additional_sentence


# Function to explicitly fix the 3rd sentence to ensure it starts with "Also"
def fix_third_sentence(text):
    sentences = re.split(r'(?<=[\.\!\?])\s+', text)  # Split into sentences
    for i in range(len(sentences)):
        sentences[i] = sentences[i].strip()
        if i == 2:  # Fix the 3rd sentence (index 2 in 0-based indexing)
            sentences[i] = sentences[i][0].upper() + sentences[i][1:]
    return " ".join(sentences)


# Function to calculate the number of whitespace characters
def count_whitespace_characters(text):
    return sum(1 for c in text if c.isspace())


# Main function to process the text and execute all steps
def process_text(text):
    print("\n--- Processing Text ---")

    # Step 1: Normalize letter cases
    normalized_text = normalize_cases(text)

    # Step 2: Fix 'iz' to 'is'
    normalized_text = fix_iz_errors(normalized_text)

    # Step 3: Fix spacing between "Fix" and "is"
    normalized_text = fix_spacing(normalized_text)

    # Step 4: Add a new sentence with the last words of all existing sentences
    normalized_text = add_last_words_sentence(normalized_text)

    # Step 5: Fix capitalization of the 3rd sentence explicitly
    normalized_text = fix_third_sentence(normalized_text)

    # Step 6: Calculate the number of whitespace characters
    whitespace_count = count_whitespace_characters(text)

    # Print results
    print("\nNormalized Text:\n")
    print(normalized_text)
    print("\nNumber of Whitespace Characters:", whitespace_count)


# The text provided for the task
text = """ homEwork: 
tHis iz your homeWork, copy these Text to variable. You NEED TO normalize it fROM letter CASEs point oF View. 


also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph. 


it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.


last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

# Run the main processing function
process_text(text)


"======================================"
import re


def merge_dicts_with_index(dicts_list):
    """
    Merges a list of dictionaries and keeps the maximum value for each key,
    along with the index of the dictionary from which the value was taken.

    :param dicts_list: A list of dictionaries to merge
    :return: A dictionary storing the maximum value for each key and the origin index
    """
    merged_dict = {}
    for dict_index, current_dict in enumerate(dicts_list, start=1):
        for key, value in current_dict.items():
            if key not in merged_dict:
                # If the key is not yet in the merged dictionary, add it with its value and dictionary index
                merged_dict[key] = (value, dict_index)
            else:
                # If the key already exists, compare its value with the current one
                existing_value, existing_dict_index = merged_dict[key]
                if value > existing_value:
                    # Update the dictionary with the new maximum value and its origin index
                    merged_dict[key] = (value, dict_index)
    return merged_dict


def rename_duplicate_keys(merged_dict, dicts_list):
    """
    Renames duplicate keys by appending the index of the dictionary
    where the maximum value originates, ensuring all keys are unique.

    :param merged_dict: A dictionary containing values and their origin indices
    :param dicts_list: The original list of dictionaries to check for duplicates
    :return: A final dictionary with unique keys and their respective values
    """
    final_dict = {}
    for key, (value, dict_index) in merged_dict.items():
        # Check if the key exists in multiple dictionaries
        is_duplicate = sum(key in dct for dct in dicts_list) > 1
        if is_duplicate:
            # Append the dictionary index to the key if it is duplicated
            final_dict[f"{key}_{dict_index}"] = value
        else:
            # Keep the original key if it is unique
            final_dict[key] = value
    return final_dict


def process_dicts_list(dicts_list):
    """
    Processes a list of dictionaries:
    - Merges dictionaries and stores the maximum value for each key
    - Renames duplicate keys to ensure uniqueness

    :param dicts_list: A list of dictionaries to process
    :return: A final dictionary with merged and renamed keys
    """
    # Step 1: Merge dictionaries with maximum values and origin indices
    merged_dict = merge_dicts_with_index(dicts_list)

    # Step 2: Rename duplicate keys for uniqueness
    final_dict = rename_duplicate_keys(merged_dict, dicts_list)

    return final_dict


# ====== Example Usage ======
random_dicts_list = [
    {'a': 5, 'b': 7},
    {'a': 3, 'c': 35, 'g': 42},
    {'a': 10, 'b': 2, 'x': 50}
]

# Process the dictionaries
result_dict = process_dicts_list(random_dicts_list)

# Print the result
print(result_dict)