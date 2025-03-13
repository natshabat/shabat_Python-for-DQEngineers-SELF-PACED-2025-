import datetime
import os


class NewsFeed:
    # File path for storing records
    FILE_PATH = r'C:\SwissRE\DynamicSeries\Pandas_Select\Homework_5.txt'

    def __init__(self):
        self.records = []

    def add_record(self, record):
        # Add a record to the feed
        self.records.append(record)

    def save_to_file(self):
        # Save all records to the text file
        with open(self.FILE_PATH, 'a', encoding='utf-8') as file:
            for record in self.records:
                file.write(record.publish() + '\n')
        # Clear processed records to avoid duplication
        self.records.clear()


class Record:
    # Base class for all record types
    def __init__(self, text):
        self.text = text

    def publish(self):
        # Publish must be implemented in derived classes
        raise NotImplementedError("Publish method must be implemented in subclasses")


class News(Record):
    # News class with text, city, and a calculated publish date
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city
        self.publish_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def publish(self):
        return f"News:\n{self.text}\nCity: {self.city}\nPublished at: {self.publish_date}\n{'-'*50}"


class PrivateAd(Record):
    # Private Ad class with text, expiration date, and days left
    def __init__(self, text, expiration_date):
        super().__init__(text)
        self.expiration_date = expiration_date
        self.days_left = (self.expiration_date - datetime.datetime.now()).days

    def publish(self):
        return (f"Private Ad:\n{self.text}\nExpiration date: {self.expiration_date.strftime('%Y-%m-%d')}\n"
                f"Days left: {self.days_left}\n{'-'*50}")


class MotivationalQuote(Record):
    # Motivational Quote with a quote and author
    def __init__(self, text, author):
        super().__init__(text)
        self.author = author
        self.publish_time = datetime.datetime.now().strftime('%H:%M:%S')

    def publish(self):
        return f"Motivational Quote:\n\"{self.text}\" - {self.author}\nPublished at: {self.publish_time}\n{'-'*50}'"


class FileProcessor:
    # Class to process records from a text file
    DEFAULT_FOLDER = r'C:\SwissRE\DynamicSeries\Pandas_Select\InputFiles'

    def __init__(self, file_path=None):
        self.file_path = file_path or self.DEFAULT_FOLDER

    def process_file(self, feed):
        # Check if the file exists
        if not os.path.exists(self.file_path):
            print(f"File '{self.file_path}' not found.")
            return

        try:
            # Read records from the file
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # Split the line into components based on the predefined format
                    record_data = line.strip().split(';')
                    record_type = record_data[0].lower()

                    # Create records based on their type
                    if record_type == 'news':
                        feed.add_record(News(record_data[1], record_data[2]))
                    elif record_type == 'privatead':
                        expiration_date = datetime.datetime.strptime(record_data[2], '%Y-%m-%d')
                        feed.add_record(PrivateAd(record_data[1], expiration_date))
                    elif record_type == 'quote':
                        feed.add_record(MotivationalQuote(record_data[1], record_data[2]))
                    else:
                        print(f"Unknown record type '{record_type}'. Skipping line.")

            # Save records to the file
            feed.save_to_file()
            print("File processed successfully!")

            # Remove the file after successful processing
            os.remove(self.file_path)
            print(f"File '{self.file_path}' removed.")
        except Exception as e:
            print(f"An error occurred while processing the file: {e}")


def get_valid_date(prompt):
    # Helper function to validate date input from the user
    while True:
        user_input = input(prompt)
        try:
            return datetime.datetime.strptime(user_input, '%Y-%m-%d')
        except ValueError:
            print(f"Invalid date format. Please enter the date in 'YYYY-MM-DD' format.")


def main():
    feed = NewsFeed()

    while True:
        print("\nSelect type of operation:")
        print("1. Add record manually")
        print("2. Process records from text file")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            # If the user wants to add records manually
            print("\nSelect type of record to add:")
            print("1. News")
            print("2. Private Ad")
            print("3. Motivational Quote")
            subtype = input("Enter your choice: ")

            if subtype == '1':
                # Add a News record
                text = input("Enter the news text: ")
                city = input("Enter the city: ")
                feed.add_record(News(text, city))

            elif subtype == '2':
                # Add a Private Ad record
                text = input("Enter the private ad text: ")
                expiration_date = get_valid_date("Enter the expiration date (YYYY-MM-DD): ")
                feed.add_record(PrivateAd(text, expiration_date))

            elif subtype == '3':
                # Add a Motivational Quote record
                text = input("Enter the motivational quote text: ")
                author = input("Enter the author of the quote: ")
                feed.add_record(MotivationalQuote(text, author))

            else:
                print("Invalid input. Please try again.")

            # Save the manually added record to the file
            feed.save_to_file()
            print("Record saved successfully!")

        elif choice == '2':
            # If the user wants to process records from a file
            file_path = input("Enter file path or press Enter for default folder: ")
            processor = FileProcessor(file_path if file_path else None)
            processor.process_file(feed)

        elif choice == '3':
            # Exit the program
            print("Exiting program.")
            break

        else:
            print("Invalid input. Please try again.")


if __name__ == '__main__':
    main()