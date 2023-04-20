### --- OOP Email Simulator --- ###

# Define the Email class
class Email:
    # Initialize and Email object with its properties
    def __init__(self, email_address, subject_line, email_content):
        self.email_address = email_address
        self.subject_line = subject_line
        self.email_content = email_content
        self.has_been_read = False

    # Mark the email as read
    def mark_as_read(self):
        self.has_been_read = True

# List of emails in the inbox and sent_emails
inbox = []
sent_emails = []

# Function to populate the inbox with sample emails
def populate_inbox():
    sample_emails = [
        Email("no-reply@hyperiondev.com", "Welcome to HyperionDev!", "Welcome to the bootcamp!"),
        Email("mentor@hyperiondev.com", "Great work on the bootcamp!", "Keep up the good work!"),
        Email("support@hyperiondev.com", "Your excellent marks!", "Congratulations on your progress!"),
    ]
    inbox.extend(sample_emails)

# Function to list emails in a given list (inbox or sent)
def list_emails(email_list, show_read_status=False):
    for idx, email in enumerate(email_list):
        read_status = "Read" if email.has_been_read else "Unread"
        if show_read_status:
            print(f"{idx} {read_status}: {email.subject_line}")
        else:
            print(f"{idx} {email.subject_line}")

# Function to read an email from a list (inbox or sent) based on the index
def read_email(email_list, index):
    email = email_list[index]
    print(f"\nEmail from {email.email_address}:\nSubject: {email.subject_line}\nContent: {email.email_content}\n")
    email.mark_as_read()

# Function to write and send a new email
def write_email():
    to_email_address = input("To: ")
    subject_line = input("Subject: ")
    email_content = input("Content: ")
    new_email = Email(to_email_address, subject_line, email_content)
    sent_emails.append(new_email)
    print("Email sent!")

# Function to delete an email from a list (inbox or sent) based on the index
def delete_email(email_list, index):
    del email_list[index]
    print("Email deleted!")

# Populate the inbox with sample emails
populate_inbox()

# Initialize a menu variable to control the main menu loop
menu = True

# Main menu loop
while menu:
    while True:
        try:
            user_choice = int(input('''\nMain menu:
            1. Inbox - all emails
            2. Unread emails
            3. Sent emails
            4. Write new email
            5. Delete emails
            6. Quit application

            Enter selection: '''))
            break
        except ValueError:
            print("Oops - incorrect input. Please enter a number.")


    # Handle user input to perform different actions on emails
    # Option 1: List all emails in the inbox
    if user_choice == 1:
        # Display the list of emails in the inbox
        list_emails(inbox)
        # Prompt the user to choose an email to read or exit
        while True:
            try:
                index = int(input("\nEnter the index of the email you want to read or -1 to return to the main menu: "))
                if 0 <= index < len(inbox):
                    read_email(inbox, index)
                    break
                elif index == -1:
                    break
                else:
                    print("Invalid index. Please try again.")
            except ValueError:
                print("Oops - incorrect input. Please enter a number.")


    # Option 2: List unread emails
    elif user_choice == 2:
        # Create a list of unread emails
        unread_emails = [(idx, email) for idx, email in enumerate(inbox) if not email.has_been_read]
        
        # If there are any unread emails, display them
        if unread_emails:
            print("\nUnread emails:")
            for idx, email in unread_emails:
                print(f"{idx} {email.subject_line}")
            
            while True:
                try:
                    index = int(input("\nEnter the index of the email you want to read or -1 to return to the main menu: "))
                    if any(idx == index for idx, email in unread_emails):
                        read_email(inbox, index)
                        break
                    elif index == -1:
                        break
                    else:
                        print("Invalid index. Please try again.")
                except ValueError:
                    print("Oops - incorrect input. Please enter a number.")
        else:
            print("\nNo unread emails!")

    # Option 3: List sent emails
    elif user_choice == 3:
        # If there are any sent emails, display them
        if sent_emails:
            print("\nSent emails:")
            list_emails(sent_emails)
            while True:
                try:
                    index = int(input("\nEnter the index of the email you want to read or -1 to return to the main menu: "))
                    if 0 <= index < len(sent_emails):
                        read_email(sent_emails, index)
                        break
                    elif index == -1:
                        break
                    else:
                        print("Invalid index. Please try again.")
                except ValueError:
                    print("Oops - incorrect input. Please enter a number.")
        else:
            print("\nNo sent emails!")

    # Option 4: Write and send a new email
    elif user_choice == 4:
        write_email()

    # Option 5: Delete emails from selected categories
    elif user_choice == 5:
            # Prompt the user to choose a category to delete emails from
            while True:
                try:
                    delete_choice = int(input('''\nSelect an email category to delete from:
                    1. Inbox
                    2. Unread emails
                    3. Sent emails
                    4. Go back to main menu

                    Enter selection: '''))
                    if 1 <= delete_choice <= 4:
                        break
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Oops - incorrect input. Please enter a number.")

            # Display emails from the chosen category
            if delete_choice == 1:
                list_emails(inbox, show_read_status=True)
                category = inbox
            elif delete_choice == 2:
                unread_emails = [email for email in inbox if not email.has_been_read]
                list_emails(unread_emails, show_read_status=True)
                category = unread_emails
            elif delete_choice == 3:
                list_emails(sent_emails)
                category = sent_emails
            elif delete_choice == 4:
                continue

            # Prompt the user to choose an email to delete or exit
            while True:
                try:
                    index = int(input("\nEnter the index of the email you want to delete or -1 to return to the previous menu: "))
                    if 0 <= index < len(category):
                        delete_email(category, index)
                        break
                    elif index == -1:
                        break
                    else:
                        print("Invalid index. Please try again.")
                except ValueError:
                    print("Oops - incorrect input. Please enter a number.")

    # Option 6: Quit the application
    elif user_choice == 6:
        print("Goodbye!")
        menu = False

    # Handle invalid user input
    else:
        print("Oops - incorrect input. Please enter a number between 1 and 6.")
