# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

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

def reg_user():
    '''Add a new user to the user.txt file'''
    while True:
        # - Request input of a new username
        new_username = input("New Username: ")

        # - Check if the username already exists
        if new_username in username_password:
            print("Username already exists. Please choose a different username.")
            continue

        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password

            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
            break
        # - Otherwise you present a relevant message.
        else:
            print("Passwords do not match")


def add_task():
    '''Allow a user to add a new task to task.txt file.
    Prompt a user for the following: 
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task, and 
    - the due date of the task.
    '''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Get the current date.
    curr_date = date.today()
    
    # Add the data to the file task.txt and include 'No' to indicate if the task is complete.
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

def view_all():
    '''
    Reads the tasks from 'tasks.txt' file and prints them to the console 
    in the specified format.
    '''
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        curr_t = {}

        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

def view_mine(curr_user):
    '''
    Displays tasks assigned to the current user.
    '''
    print("Tasks Assigned to You:")
    for idx, t in enumerate(task_list, start=1):
        if t['username'] == curr_user:
            disp_str = f"{idx}. Task: \t\t {t['title']}\n"
            disp_str += f"   Assigned to: \t {t['username']}\n"
            disp_str += f"   Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"   Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"   Task Description: \n {t['description']}\n"
            disp_str += f"   Status: \t {'Completed' if t['completed'] else 'Not Completed'}\n"
            print(disp_str)
            action = input("Do you want to edit this task? (Y/N): ").lower()
            if action == 'y':
                edit_action = input("Do you want to edit (U)ser, (D)ate, (T)itle/Description, or (C)omplete status?: ").lower()
                if edit_action == 'u':
                    new_username = input("Enter new username: ")
                    t['username'] = new_username
                elif edit_action == 'd':
                    new_due_date = input("Enter new due date (YYYY-MM-DD): ")
                    t['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                elif edit_action == 't':
                    new_title_description = input("Enter new title/description: ")
                    t['title'] = new_title_description.split(';')[0]
                    t['description'] = new_title_description.split(';')[1]
                elif edit_action == 'c':
                    mark_complete = input("Mark as complete? (Y/N): ").lower()
                    if mark_complete == 'y':
                        t['completed'] = True
                    else:
                        t['completed'] = False
                else:
                    print("Invalid action.")
                # Update the tasks.txt file after editing
                with open("tasks.txt", "w") as task_file:
                    task_list_to_write = []
                    for task in task_list:
                        str_attrs = [
                            task['username'],
                            task['title'],
                            task['description'],
                            task['due_date'].strftime(DATETIME_STRING_FORMAT),
                            task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                            "Yes" if task['completed'] else "No"
                        ]
                        task_list_to_write.append(";".join(str_attrs))
                    task_file.write("\n".join(task_list_to_write))
                print("Task successfully updated.")
# Amended per mentor comments

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
gr - Generate reports                
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        '''Add a new user to the user.txt file'''
        # - Request input of a new username
        reg_user()


    elif menu == 'a':
        add_task()


    elif menu == 'va':
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''
        view_all()


    elif menu == 'vm':
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
        view_mine(curr_user)
                

    elif menu == 'gr':
    # Task Overview
        total_tasks = len(task_list)
        completed_tasks = sum(1 for t in task_list if t['completed'])
        incomplete_tasks = total_tasks - completed_tasks
        overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'] < datetime.today()) # amended per mentor comments
        incomplete_percentage = (incomplete_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        task_overview_content = f'''Task Overview:
        Total tasks: {total_tasks}
        Completed tasks: {completed_tasks}
        Uncompleted tasks: {incomplete_tasks}
        Overdue tasks: {overdue_tasks}
        Percentage of incomplete tasks: {incomplete_percentage}%
        Percentage of overdue tasks: {overdue_percentage}%
        ''' #changed indentation per mentor comments

    elif menu == 'ds' and curr_user == 'admin':
        '''If the user is an admin, they can display statistics about the number of users and tasks.'''
        # Check if the reports exist, if not, generate them
        if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
            # Task Overview
            total_tasks = len(task_list)
            completed_tasks = sum(1 for t in task_list if t['completed'])
            incomplete_tasks = total_tasks - completed_tasks
            overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'] < datetime.today()) #amended per mentor comments
            incomplete_percentage = (incomplete_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0

            task_overview_content = f'''Task Overview:
            Total tasks: {total_tasks}
            Completed tasks: {completed_tasks}
            Uncompleted tasks: {incomplete_tasks}
            Overdue tasks: {overdue_tasks}
            Percentage of incomplete tasks: {incomplete_percentage}%
            Percentage of overdue tasks: {overdue_percentage}%
            '''

            # User Overview
            total_users = len(username_password)
            user_task_stats = {}
            for user in username_password.keys():
                user_tasks = [t for t in task_list if t['username'] == user]
                total_user_tasks = len(user_tasks)
                completed_user_tasks = sum(1 for t in user_tasks if t['completed'])
                incomplete_user_tasks = total_user_tasks - completed_user_tasks
                overdue_user_tasks = sum(1 for t in user_tasks if not t['completed'] and t['due_date'] < datetime.today()) # amended per mentor comments

                user_task_stats[user] = {
                    'total_tasks': total_user_tasks,
                    'completed_tasks': completed_user_tasks,
                    'incomplete_tasks': incomplete_user_tasks,
                    'overdue_tasks': overdue_user_tasks,
                    'percentage_total_tasks': (total_user_tasks / total_tasks) * 100 if total_tasks > 0 else 0,
                    'percentage_completed_tasks': (completed_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0,
                    'percentage_incomplete_tasks': (incomplete_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0,
                    'percentage_overdue_tasks': (overdue_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
             }

            user_overview_content = f'''User Overview:
            Total users: {total_users}
            Total tasks: {total_tasks}
            '''
            for user, stats in user_task_stats.items():
                user_overview_content += f'''
                User: {user}
                Total tasks assigned: {stats['total_tasks']}
                Percentage of total tasks: {stats['percentage_total_tasks']}%
                Percentage of completed tasks: {stats['percentage_completed_tasks']}%
                Percentage of incomplete tasks: {stats['percentage_incomplete_tasks']}%
                Percentage of overdue tasks: {stats['percentage_overdue_tasks']}%
                '''

        # Write to files
            with open('task_overview.txt', 'w') as task_overview_file:
                task_overview_file.write(task_overview_content)

            with open('user_overview.txt', 'w') as user_overview_file:
                user_overview_file.write(user_overview_content)

            print("Reports generated successfully.")

        # Display reports
        with open('task_overview.txt', 'r') as task_overview_file:
            task_overview_content = task_overview_file.read()

        with open('user_overview.txt', 'r') as user_overview_file:
            user_overview_content = user_overview_file.read()

        print("-----------------------------------")
        print("Task Overview:")
        print(task_overview_content)
        print("-----------------------------------")
        print("User Overview:")
        print(user_overview_content)
        print("-----------------------------------")


     # User Overview
        total_users = len(username_password)
        user_task_stats = {}
        for user in username_password.keys():
            user_tasks = [t for t in task_list if t['username'] == user]
            total_user_tasks = len(user_tasks)
            completed_user_tasks = sum(1 for t in user_tasks if t['completed'])
            incomplete_user_tasks = total_user_tasks - completed_user_tasks
            overdue_user_tasks = sum(1 for t in user_tasks if not t['completed'] and t['due_date'] < datetime.today()) # amended per mentor commnents

            user_task_stats[user] = {
                'total_tasks': total_user_tasks,
                'completed_tasks': completed_user_tasks,
                'incomplete_tasks': incomplete_user_tasks,
                'overdue_tasks': overdue_user_tasks,
                'percentage_total_tasks': (total_user_tasks / total_tasks) * 100 if total_tasks > 0 else 0,
                'percentage_completed_tasks': (completed_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0,
                'percentage_incomplete_tasks': (incomplete_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0,
                'percentage_overdue_tasks': (overdue_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
            }

        user_overview_content = f'''User Overview:
        Total users: {total_users}
        Total tasks: {total_tasks}
        '''
        for user, stats in user_task_stats.items():
            user_overview_content += f'''
        User: {user}
            Total tasks assigned: {stats['total_tasks']}
            Percentage of total tasks: {stats['percentage_total_tasks']}%
            Percentage of completed tasks: {stats['percentage_completed_tasks']}%
            Percentage of incomplete tasks: {stats['percentage_incomplete_tasks']}%
            Percentage of overdue tasks: {stats['percentage_overdue_tasks']}%
            '''

        # Write to files
        with open('task_overview.txt', 'w') as task_overview_file:
            task_overview_file.write(task_overview_content)

        with open('user_overview.txt', 'w') as user_overview_file:
            user_overview_file.write(user_overview_content)

        print("Reports generated successfully.")
 # increased indentation on lines 268-390 per mentor comments
    
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")