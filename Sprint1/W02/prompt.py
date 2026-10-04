"""A simple command-line input and output program."""


def main():
    """Collect information from the user and print a response."""
    print("Welcome to the command-line prompt program!")

    name = input("What is your name? ").strip()

    while True:
        age_text = input("How old are you? ").strip()
        try:
            age = int(age_text)
            if age < 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a whole number that is zero or greater.")

    print(f"Hello, {name}! You are {age} years old.")
    print("Thanks for using the program.")


if __name__ == "__main__":
    main()
