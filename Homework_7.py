import csv
import os
import string

# Paths to input and output files
input_file_path = r'C:\SwissRE\DynamicSeries\Pandas_Select\Homework_5.txt'
word_count_csv_path = r'C:\SwissRE\DynamicSeries\Pandas_Select\word-count.csv'
letter_count_csv_path = r'C:\SwissRE\DynamicSeries\Pandas_Select\letter-count.csv'


def preprocess_text(text):
    """Convert text to lowercase and remove punctuation."""
    return text.lower().translate(str.maketrans("", "", string.punctuation)).strip()


def calculate_word_count(file_path):
    """Calculate the count of each word in the file."""
    word_count = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            words = preprocess_text(line).split()
            for word in words:
                word_count[word] = word_count.get(word, 0) + 1
    return word_count


def calculate_letter_statistics(file_path):
    """Calculate letter statistics for the file."""
    letter_stats = {}
    total_letters = 0
    total_uppercase_letters = 0

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            for char in line:
                if char.isalpha():  # Check if the character is alphabetic
                    total_letters += 1
                    if char.isupper():
                        total_uppercase_letters += 1

                    char_lower = char.lower()
                    letter_stats[char_lower] = letter_stats.get(char_lower, 0) + 1

    # Calculate the percentage of uppercase letters
    return {
        'letter_stats': letter_stats,
        'total_letters': total_letters,
        'total_uppercase_letters': total_uppercase_letters,
        'uppercase_percentage': (total_uppercase_letters / total_letters * 100) if total_letters else 0
    }


def write_word_count_to_csv(word_count, csv_path):
    """Write word count to a CSV file."""
    with open(csv_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Word', 'Count'])
        for word, count in sorted(word_count.items()):
            writer.writerow([word, count])


def write_letter_statistics_to_csv(stats, csv_path):
    """Write letter statistics to a CSV file."""
    with open(csv_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Letter', 'Count_All', 'Count_Uppercase', 'Percentage_Uppercase'])
        for letter, count in sorted(stats['letter_stats'].items()):
            count_uppercase = stats['letter_stats'].get(letter.upper(), 0)
            percentage_uppercase = (count_uppercase / count * 100) if count else 0
            writer.writerow([letter, count, count_uppercase, percentage_uppercase])


def recreate_csv_files(input_file, word_count_csv, letter_count_csv):
    """Main function to process the input file and write results to CSV files."""
    if not os.path.exists(input_file):
        print(f"Error: The input file '{input_file}' does not exist. Please check the file path.")
        return

    # Ensure output directory exists
    output_dir = os.path.dirname(word_count_csv)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Processing file: {input_file}")

    word_count = calculate_word_count(input_file)
    write_word_count_to_csv(word_count, word_count_csv)

    letter_statistics = calculate_letter_statistics(input_file)
    write_letter_statistics_to_csv(letter_statistics, letter_count_csv)

    print(f"Files created:\n - {word_count_csv}\n - {letter_count_csv}")


if __name__ == "__main__":
    # Recreate the CSV files
    recreate_csv_files(input_file_path, word_count_csv_path, letter_count_csv_path)

    print(f"Execution completed. Check the folder: 'C:\\SwissRE\\DynamicSeries\\Pandas_Select'.")
