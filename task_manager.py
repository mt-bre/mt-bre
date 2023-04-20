# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

# Set the date-time string format
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt and user.txt if they don't exist
def create_default_files():
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

# Reads user data from the file and returns a dictionary with username-password pairs
def read_user_data():
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    return username_password

# Reads task data from the file and returns a list of dictionaries with task information
def read_task_data():
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        curr_t = {}
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)

    return task_list


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''

# Handles user login, returns True if login is successful, otherwise returns False
def login(username_password):
    logged_in = False
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True

    return curr_user

# Registers a new user by updating the dictionary and saving it to the file
def reg_user(username_password):
    # Prompt for a new username
    new_username = input("New Username: ")

    # Check if the username already exists
    if new_username in username_password:
        print("Username already exists. Please try a different username.")
        return

    # Get the new password and confirm it
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    # Check if the passwords match
    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
    else:
        print("Passwords do no match")

# Adds a new task to the task list after taking necessary input from the user
def add_task(username_password, task_list):
    # Request the user to input the username of the person assigned to the task
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return

    # Request the user to input the task title and description
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    # Validate and caputre the task due date
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()

    # Create a new task dictionary and append it to the task list
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)

    # Write the new task to the tasks.txt file
    with open("tasks.txt", "a") as task_file:
        task_file.write(
            f"\n{task_username};{task_title};{task_description};{task_due_date};"
            f"{curr_date.strftime(DATETIME_STRING_FORMAT)};No"
            )

# Displays all the tasks in the task list
def view_all(task_list):
    if not task_list:
        print("There are no tasks.")
        return
    
    for task in task_list:
        print_task(task)

# Displays tasks assigned to the current user and provides options to edit or mark them complete
def view_mine(username, task_list):
    # Filter the task list to display only the tasks assigned to the current user
    my_tasks = [task for task in task_list if task["username"] == username]

    if not my_tasks:
        print("You have no tasks.")
        return

    task_indices = []
    task_number = 1
    for task in my_tasks:
        print(f"Task {task_number}:")
        print_task(task)
        task_indices.append(task_list.index(task))
        task_number += 1

    # Prompt the user for an action to perform on a task
    print("\nSelect a task to edit (enter the task number) or enter -1 to return to the main menu.")
    selected_task = int(input())

    if selected_task == -1:
        return
    elif 1 <= selected_task <= len(my_tasks):
        selected_index = task_indices[selected_task - 1]
        edit_task(task_list, task_list[selected_index])
    else:
        print("Invalid input. Returning to the main menu.")

# Marks the given task as complete in the task list
def mark_task_complete(task_list, task_to_complete):
    # Iterate through the task list to find and mark the task as complete
    for task in task_list:
        # Update the tasks.txt file with the updated task list
        if task == task_to_complete:
            task['completed'] = True
            update_tasks_file(task_list)
            break

# Edits the given task in the task list based on user input
def edit_task(task_list, task_to_edit):
    if not task_list:
        print("There are no tasks.")
        return

    # Prompt the user to input the new username and/or due date for the task
    new_username = input("Enter the new username for the task or leave blank to keep the current one: ").strip()
    if new_username:
        task_to_edit['username'] = new_username

    new_due_date = input("Enter the new due date (YYYY-MM-DD) for the task or leave blank to keep the current one: ").strip()
    
    # Update the task with new details, if provided
    if new_due_date:
        try:
            due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT).date()
            task_to_edit['due_date'] = due_date_time
        except ValueError:
            print("Invalid datetime format. Due date not updated")

    # Update the tasks.txt file with the updated task list
    save_task_data(task_list)


# Updates the tasks file with the latest task list
def update_tasks_file(task_list):
    # Open the tasks.txt file in write mode and iterate through the task list
    with open("tasks.txt", "w") as task_file:
        for task in task_list:
            task_file.write(
                f"{task['username']};{task['title']};{task['description']};"
                f"{task['due_date'].strftime(DATETIME_STRING_FORMAT)};"
                f"{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};"
                f"{'Yes' if task['completed'] else 'No'}\n"
                )
            
# Prints a single task with proper formatting
def print_task(task):
    # Print the task details with appropriate labels
    print(f"Assigned to: {task['username']}")
    print(f"Task Title: {task['title']}")
    print(f"Task Description: {task['description']}")
    print(f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
    print(f"Assigned Date: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
    print(f"Completed: {'Yes' if task['completed'] else 'No'}\n")

# Generates reports for tasks and users, and saves them in separate text files
def generate_reports(task_list, username_password):
    # Initialize task and user overview data
    task_overview = {
        "total_tasks": len(task_list),
        "completed_tasks": 0,
        "incomplete_tasks": 0,
        "overdue_tasks": 0,
    }

    user_overview = {username: {"total_tasks": 0, "completed_tasks": 0} for username in username_password.keys()}

    # Calculate task and user overview data
    now = datetime.now().date()
    for task in task_list:
        completed = task['completed'] != "Not yet completed"

        if completed:
            task_overview["completed_tasks"] += 1
        else:
            task_overview["incomplete_tasks"] += 1

        due_date_str = task["due_date"]
        due_date = due_date_str
        if not completed and now > due_date:
            task_overview["overdue_tasks"] += 1

        user_overview[task["username"]]["total_tasks"] += 1
        if completed:
            user_overview[task["username"]]["completed_tasks"] += 1

    # Write task overview data to task_overview.txt file
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write("Total tasks: " + str(task_overview["total_tasks"]) + "\n")
        task_overview_file.write("Completed tasks: " + str(task_overview["completed_tasks"]) + "\n")
        task_overview_file.write("Incomplete tasks: " + str(task_overview["incomplete_tasks"]) + "\n")
        task_overview_file.write("Overdue tasks: " + str(task_overview["overdue_tasks"]) + "\n")

        if task_overview["total_tasks"] > 0:
            completion_rate = round(task_overview["completed_tasks"] / task_overview["total_tasks"] * 100, 2)
            task_overview_file.write(f"Completion rate: {completion_rate}%\n")

            overdue_rate = round(task_overview["overdue_tasks"] / task_overview["total_tasks"] * 100, 2)
            task_overview_file.write(f"Overdue rate: {overdue_rate}%\n")

    # Write user overview data to user_overview.txt file
    with open("user_overview.txt", "w") as user_overview_file:
        for username in user_overview:
            user_overview_file.write("User: " + username + "\n")
            user_overview_file.write("Total tasks: " + str(user_overview[username]["total_tasks"]) + "\n")
            user_overview_file.write("Completed tasks: " + str(user_overview[username]["completed_tasks"]) + "\n")
            if user_overview[username]["total_tasks"] > 0:
                completion_rate_raw = user_overview[username]["completed_tasks"] / user_overview[username]["total_tasks"]
                completion_rate = round(completion_rate_raw * 100, 2)
                user_overview_file.write(f"Completion rate: {completion_rate}%\n")

            user_overview_file.write("\n")

# Displays the statistics generated by the task and user overviews
def display_statistics(task_list, username_password):
    # Remove "admin" from username_password dictionary
    username_password_filtered = {user: pwd for user, pwd in username_password.items() if user != "admin"}

    # Check if the overview files exist; if not, generate the reports
    if not (os.path.exists("task_overview.txt") and os.path.exists("user_overview.txt")):
        generate_reports(task_list, username_password)

    # Display the content of the task_overwiew.txt file
    print("\nTask Overview:")
    with open("task_overview.txt", "r") as task_overview_file:
        print(task_overview_file.read())

    # Display the content of the user_overview.txt file
    print("\nUser Overview:")
    with open("user_overview.txt", "r") as user_overview_file:
        print(user_overview_file.read())

# Deletes a task from the task list
def delete_task(task_list):
    if not task_list:
        print("There are no tasks.")
        return
    
    # Request the user to input the task number to delete   
    task_num = int(input("Enter the task number to delete: "))
    
    # Check if the task number is valid and delete the task if it is
    if 0 < task_num <= len(task_list):
        del task_list[task_num - 1]
        print("Task deleted successfully.")
    else:
        print("Invalid task number. No task was deleted.")

# Changes the completion status of a task in the task list
def change_task_status(username, task_list):
    if not task_list:
        print("There are no tasks.")
        return
    
    # Request the user to input the task number to change its status
    task_num = int(input("Enter the task number to change its status: "))
    
    # Check if the task number is valid and the task belongs to the user
    if 0 < task_num <= len(task_list):
        task = task_list[task_num - 1]
        # Change the task's completion status and print the new status
        if task['username'] == username:
            task['completed'] = not task['completed']
            new_status = "completed" if task['completed'] else "incomplete"
            print(f"Task status changed to {new_status}.")
        else:
            print("You can only change the status of your own tasks.")
    else:
        print("Invalid task number. No status was changed.")

# Saves the task data to the tasks file
def save_task_data(task_list):
    # Open the tasks.txt file in write mode and iterate through the task list
    with open("tasks.txt", "w") as tasks_file:
        for task in task_list:
            tasks_file.write(
                f"{task['username']};{task['title']};{task['description']};"
                f"{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};"
                f"{task['due_date'].strftime(DATETIME_STRING_FORMAT)};"
                f"{task['completed']}\n"
                )

# Saves the user data to the user.txt file
def save_user_data(username_password):
    # Open the user.txt file in write mode and iterate through the dictionary
    with open("user.txt", "w") as user_file:
        for username, password in username_password.items():
            # Write each username-password pair to the file using a semicolon as a delimiter
            user_file.write(f"{username};{password}\n")

# Loads task data from the tasks file and returns a list of task dictionaries
def load_task_data():
    task_list = []
    # Handle the case where tasks.txt file does not exist yet with the try-except block
    try:
        # Open the tasks.txt file in read mode and process each line
        with open("tasks.txt", "r") as task_file:
            for line in task_file:
                data = line.strip().split(";")
                # If the line is properly formatted, convert it into a task dictionary and and add it to the task list
                if len(data) == 6:
                    username, title, description, due_date, assigned_date, completed = data
                    due_date = datetime.strptime(due_date, DATETIME_STRING_FORMAT).date()
                    assigned_date = datetime.strptime(assigned_date, DATETIME_STRING_FORMAT).date()
                    completed = completed == "Yes"

                    task_list.append({
                        "username": username,
                        "title": title,
                        "description": description,
                        "due_date": due_date,
                        "assigned_date": assigned_date,
                        "completed": completed
                    })
                else:
                    print(f"Warning: Skipping improperly formatted line: {line.strip()}")
    except FileNotFoundError:
        print("tasks.txt not found. A new file will be created upon saving tasks.")
    
    # Return the list of task dictionaries
    return task_list

# Loads user data from the user.txt file and returns a dictionary of username-password pairs
def load_user_data():
    username_password = {}
    # Handle the case where user.txt file does not exist yet with try-except block
    try:
        # Open the user.txt file in read mode and process each line
        with open("user.txt", "r") as user_file:
            for line in user_file:
                # Strip leading and trailing whitespaces and then split by semicolon
                data = line.strip().split(";")
                # If the line is properly formatted, add the username and password to the dictionary
                if len(data) == 2:
                    username, password = data
                    username_password[username.strip()] = password.strip()
                else:
                    print(f"Warning: Skipping improperly formatted line: {line.strip()}")
    except FileNotFoundError:
        print("user.txt not found. A new file will be created upon saving user data.")

    # Return the dictionary of username-password pairs
    return username_password

# Main function that runs the Task Manager program
def main():
    # Load user and task data from their respective files
    username_password = load_user_data()
    task_list = load_task_data()

    # Initialize login and admin status variables
    is_admin = False
    logged_in = False

    # Display the welcome message and start the login process
    print("Welcome to the Task Manager!")
    # Repeat until the user logs in successfully
    while not logged_in:
        # Prompt user for username and password
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")

        # Check if the provided credentials are correct
        if username_password.get(username) == password:
            logged_in = True
            # Check if the user is an admin
            if username == "admin":
                is_admin = True
        else:
            print("Invalid username or password. Please try again.")

    # Main loop for processing user input
    while True:
        # Display menu options
        print("\nPlease choose an option:")
        print("a - add task")
        print("va - view all tasks")
        print("vm - view my tasks")
        print("cs - change task status")
        if is_admin:
            print("r - register user")
            print("da - delete a task")
            print("gr - generate reports")
            print("ds - display statistics")
        print("e - exit")

        # Process user input
        user_input = input().lower()

        # Call the respective functions
        if user_input == "a":
            add_task(username_password, task_list)
            save_task_data(task_list)
        elif user_input == "va":
            view_all(task_list)
        elif user_input == "vm":
            view_mine(username, task_list)
            save_task_data(task_list)
        elif user_input == "cs":
            change_task_status(username, task_list)
            save_task_data(task_list)
        elif is_admin:
            if user_input == "r":
                reg_user(username_password)
                save_user_data(username_password)
            elif user_input == "da":
                delete_task(task_list)
                save_task_data(task_list)
            elif user_input == "gr":
                generate_reports(task_list, username_password)
                print("Reports generated.")
            elif user_input == "ds":
                display_statistics(task_list, username_password)
        if user_input == "e":
            break

# Executes the main function of the Task Manager program when the script is run directly
if __name__ == "__main__":
    main()
