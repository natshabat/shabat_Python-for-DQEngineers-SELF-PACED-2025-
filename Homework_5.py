import datetime


class NewsFeed:
    FILE_PATH = r'C:\SwissRE\DynamicSeries\Pandas_Select\Homework_5.txt'

    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def save_to_file(self):
        with open(self.FILE_PATH, 'a', encoding='utf-8') as file:
            for record in self.records:
                file.write(record.publish() + '\n')
        self.records.clear()


class Record:
    def __init__(self, text):
        self.text = text

    def publish(self):
        raise NotImplementedError("Publish method must be implemented in subclasses")


class News(Record):
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city
        self.publish_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def publish(self):
        return f"News:\n{self.text}\nCity: {self.city}\nPublished at: {self.publish_date}\n{'-'*50}"


class PrivateAd(Record):
    def __init__(self, text, expiration_date):
        super().__init__(text)
        self.expiration_date = expiration_date
        self.days_left = (self.expiration_date - datetime.datetime.now()).days

    def publish(self):
        return (f"Private Ad:\n{self.text}\nExpiration date: {self.expiration_date.strftime('%Y-%m-%d')}\n"
                f"Days left: {self.days_left}\n{'-'*50}")


class MotivationalQuote(Record):  # Унікальний тип публікації
    def __init__(self, text, author):
        super().__init__(text)
        self.author = author
        self.publish_time = datetime.datetime.now().strftime('%H:%M:%S')

    def publish(self):
        return f"Motivational Quote:\n\"{self.text}\" - {self.author}\nPublished at: {self.publish_time}\n{'-'*50}"


def get_valid_date(prompt):
    while True:
        user_input = input(prompt)
        try:
            # Перетворення тексту на дату
            return datetime.datetime.strptime(user_input, '%Y-%m-%d')
        except ValueError:
            print(f"Invalid date format. Please enter the date in 'YYYY-MM-DD' format.")


def main():
    feed = NewsFeed()
    while True:
        print("\nSelect type of record to add:")
        print("1. News")
        print("2. Private Ad")
        print("3. Motivational Quote")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            text = input("Enter the news text: ")
            city = input("Enter the city: ")
            feed.add_record(News(text, city))

        elif choice == '2':
            text = input("Enter the private ad text: ")
            expiration_date = get_valid_date("Enter the expiration date (YYYY-MM-DD): ")
            feed.add_record(PrivateAd(text, expiration_date))

        elif choice == '3':
            text = input("Enter the motivational quote text: ")
            author = input("Enter the author of the quote: ")
            feed.add_record(MotivationalQuote(text, author))

        elif choice == '4':
            print("Exiting program.")
            break

        else:
            print("Invalid input. Please try again.")
            continue

        feed.save_to_file()
        print("Record saved successfully!")


if __name__ == '__main__':
    main()