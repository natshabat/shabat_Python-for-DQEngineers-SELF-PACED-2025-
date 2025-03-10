import re

# The text provided for the task
text = """ homEwork: 
tHis iz your homeWork, copy these Text to variable. You NEED TO normalize it fROM letter CASEs point oF View. 


also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph. 


it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.


last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

# Step 1: Normalize letter cases
# Split text into sentences
sentences = re.split(r'(?<=[.\n])\s+', text.strip())  # Split at newlines and periods

normalized_sentences = []
for sentence in sentences:
    sentence = sentence.strip()  # Remove extra whitespace around the sentence
    if sentence:
        normalized_sentence = sentence[0].upper() + sentence[1:].lower()
        normalized_sentences.append(normalized_sentence)

normalized_text = " ".join(normalized_sentences)

# Step 2: Fix 'iz' to 'is' (when it's a mistake)
normalized_text = re.sub(r'\b[Ii][Zz]\b', 'is', normalized_text)

# Step 3: Fix spacing issue between "Fix" and "is"
normalized_text = re.sub(r'Fix“', 'Fix “', normalized_text)

# Step 4: Add one more sentence with the last words of each existing sentence
all_sentences = re.split(r'(?<=[\.\!\?])\s+', normalized_text)  # Split into sentences
last_words = [sentence.strip().split()[-1].strip(".").capitalize() for sentence in all_sentences if sentence.strip()]
additional_sentence = " ".join(last_words) + "."
normalized_text += " " + additional_sentence

# Step 5: Fix the 3rd sentence explicitly (capitalizing "Also")
final_sentences = re.split(r'(?<=[\.\!\?])\s+', normalized_text)
for i in range(len(final_sentences)):
    final_sentences[i] = final_sentences[i].strip()
    if i == 2:  # 3rd sentence (index 2 in 0-based indexing)
        final_sentences[i] = final_sentences[i][0].upper() + final_sentences[i][1:]

normalized_text = " ".join(final_sentences)

# Step 6: Calculate the number of whitespace characters
whitespace_count = sum(c.isspace() for c in text)

# Print the outputs
print("Normalized Text:\n")
print(normalized_text)
print("\nNumber of Whitespace Characters:", whitespace_count)