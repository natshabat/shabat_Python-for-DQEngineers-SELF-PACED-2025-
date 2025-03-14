import csv
import os
import string
import sqlite3  # For database-related functionalities


# Paths to input and output files
DEFAULT_FOLDER = r'C:\SwissRE\DynamicSeries\Pandas_Select'
input_file_path = os.path.join(DEFAULT_FOLDER, 'Homework_5.txt')
word_count_csv_path = os.path.join(DEFAULT_FOLDER, 'word-count.csv')
letter_count_csv_path = os.path.join(DEFAULT_FOLDER, 'letter-count.csv')
database_path = os.path.join(DEFAULT_FOLDER, 'records.db')  # SQLite database file


class DatabaseHandler:
    """A class to manage database operations."""

    def __init__(self, db_path):
        """
        Initialize the database handler and set up the required tables.
        :param db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self.connection = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Establish a connection to the SQLite database."""
        self.connection = sqlite3.connect(self.db_path)
        print(f"Connected to database: {self.db_path}")

    def disconnect(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Disconnected from the database.")

    def create_tables(self):
        """Create tables for storing word and letter statistics, if they don't already exist."""
        cursor = self.connection.cursor()

        # Table for word statistics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_count (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                count INTEGER NOT NULL,
                UNIQUE(word)  -- Ensure no duplicate entries for words
            )
        ''')

        # Table for letter statistics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS letter_statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                letter TEXT NOT NULL,
                count_all INTEGER NOT NULL,
                count_uppercase INTEGER NOT NULL,
                percentage_uppercase REAL NOT NULL,
                UNIQUE(letter)  -- Ensure no duplicate entries for letters
            )
        ''')

        self.connection.commit()
        print("Tables created (or already exist).")

    def insert_word_count(self, word, count):
        """
        Insert a word count record into the database.
        :param word: The word to insert.
        :param count: The count of the word to insert.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                'INSERT OR IGNORE INTO word_count (word, count) VALUES (?, ?)',
                (word, count)
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            print(f"Record for word '{word}' already exists, ignoring duplicate.")

    def insert_letter_statistics(self, letter, count_all, count_uppercase, percentage_uppercase):
        """
        Insert a letter statistics record into the database.
        :param letter: The letter to insert.
        :param count_all: Total occurrences of the letter.
        :param count_uppercase: Total uppercase occurrences of the letter.
        :param percentage_uppercase: Percentage of uppercase occurrences.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                'INSERT OR IGNORE INTO letter_statistics (letter, count_all, count_uppercase, percentage)
                 VALUES (?, ?, ?, ?)',
                (letter, count_all, count_uppercase, percentage_uppercase)
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            print(f"Record for letter '{letter}' already exists, ignoring duplicate.")


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


def recreate_csv_files(input_file, word_count_csv, letter_count_csv, db_handler):
    """Main function to process the input file, write results to CSV files, and save to the database."""
    if not os.path.exists(input_file):
        print(f"Error: The input file '{input_file}' does not exist. Please check the file path.")
        return

    # Ensure output directory exists
    output_dir = os.path.dirname(word_count_csv)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Processing file: {input_file}")

    # Process word count
    word_count = calculate_word_count(input_file)
    write_word_count_to_csv(word_count, word_count_csv)

    for word, count in word_count.items():
        db_handler.insert_word_count(word, count)

    # Process letter statistics
    letter_statistics = calculate_letter_statistics(input_file)
    write_letter_statistics_to_csv(letter_statistics, letter_count_csv)

    for letter, count in letter_statistics['letter_stats'].items():
        db_handler.insert_letter_statistics(
            letter,
            count,
            letter_statistics['total_uppercase_letters'],
            letter_statistics['uppercase_percentage']
        )

    print(f"Files created:\n - {word_count_csv}\n - {letter_count_csv}")


if __name__ == "__main__":
    # Initialize the database handler
    db_handler = DatabaseHandler(database_path)

    # Recreate CSV files and save records into the database
    recreate_csv_files(input_file_path, word_count_csv_path, letter_count_csv_path, db_handler)

    # Disconnect from the database
    db_handler.disconnect()

    print(f"Execution completed. Check the folder: '{DEFAULT_FOLDER}' and the database: {database_path}.")
    