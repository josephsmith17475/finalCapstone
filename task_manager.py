# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os


from datetime import datetime, date


import tabulate


DATETIME_STRING_FORMAT = "%Y-%m-%d"
print(os.getcwd())


# - Create tasks.txt if it doesn't exist. I turned this into a function to reuse code
def if_task_doesnt_exist():
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass


if_task_doesnt_exist()

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

# - Tracker variables for the creation of overview txt files
task_num_tracker = 0
completed_task_tracker = 0
tasks_overdue = 0
total_users = 0

task_list = []
for t_str in task_data:
    curr_t = {}

    # - Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['task_num'] = task_components[0]
    curr_t['username'] = task_components[1]
    curr_t['title'] = task_components[2]
    curr_t['description'] = task_components[3]
    curr_t['due_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[5], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[6] == "Yes" else False

    task_num_tracker += 1

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''


# - If no user.txt file, write one with a default account, turned into function to reuse code
def if_user_doesnt_exist(total_users): 
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")
            total_users+=1


if_user_doesnt_exist(total_users)

# - Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")
    total_users += 1

# - Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

# - Functions


# - This is used to write the changes of the task_file list to the file
def Write_tasks():
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['task_num'],
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(map(str, str_attrs)))
        task_file.write("\n".join(task_list_to_write))


# - Registers the user by taking a username and password and storing it in user.txt
def Reg_user(total_users):
    while True:
        '''Add a new user to the user.txt file'''
        # - Request input of a new username
        new_username = input("New Username: ")

        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")
        # - Check if the user is about to create a duplicate account and stop it
        if new_username in username_password.keys():
            print("User already exists. Please try a different username. ")
            continue
        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                    # - counter for all users in the users.txt file
                    total_users+=1
                out_file.write("\n".join(user_data))
            break
        # - Otherwise you present a relevant message.
        else:
            print("Passwords do no match")
            break


# - This will handle the proceess of adding tasks to the task.txt file
def Add_task(task_num_tracker):
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
         - A username of the person whom the task is assigned to,
         - A title of a task,
         - A description of the task and 
         - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return False
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")


    # - Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    
    ''' This will add another 1 to the task tracker as it will allow for
        the task selection implementation to be much easier later on'''
    task_num_tracker += 1
    new_task = {
        "task_num": str(task_num_tracker),
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    Write_tasks()
    print("Task successfully added.")


# - This will take all of the tasks from the task.txt file and display them in the console
def view_all():
    for t in task_list:
        disp_str = [
            ["Task:", t['title']],
            ["Assigned to:", t['username']],
            ["Date Assigned:", t['assigned_date'].strftime(DATETIME_STRING_FORMAT)],
            ["Due Date:", t['due_date'].strftime(DATETIME_STRING_FORMAT)],
            ["Task Description:", t['description']],
            [""],
            ["Task Completed:", t['completed']]
        ]
        # - Tabulate function offers a easy way to neatly display a list
        print("\n",tabulate.tabulate(disp_str, headers= ["Task number: ",t['task_num']]))


# - This will display all the tasks of the current users and will allow for the
#   user to edit the tasks they are assigned
def view_mine(completed_task_tracker):
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
    '''
    for t in task_list:
        if t['username'] == curr_user:
            # - List changed to be  more suited to tabulate function
            disp_str = [
                ["Task:", t['title']],
                ["Assigned to:", t['username']],
                ["Date Assigned:", t['assigned_date'].strftime(DATETIME_STRING_FORMAT)],
                ["Due Date:", t['due_date'].strftime(DATETIME_STRING_FORMAT)],
                ["Task Description:", t['description']],
                [""],
                ["Task Completed:", t['completed']]
            ]
            # - Tabulate function offers a easy way to neatly display a list
            print("\n",tabulate.tabulate(disp_str, headers= ["Task number: ",t['task_num']]))
    choice = int(input("\nDo you want to select a task?(enter number assigned to the task or -1 to not): "))
    if choice != -1:
        for i, t in enumerate(task_list):
            if t['task_num'] == str(choice):
                print("\nTask Found")
                option = input("\nWould you like to mark the task as complete or edit the task?(input mark or edit): ")
                if option.lower() == "mark":
                    t['completed'] = True
                    print("\n(",t['title'], ") task has been marked as completed.")
                    completed_task_tracker +=1
                    Write_tasks()
                    break
                elif option.lower() == "edit":
                    if t['completed'] != True:
                        print("What would you like to edit?:")
                        print("\n\t1.change the user who the task is assigned to?")
                        print("\n\t2.change due date of the task?")
                        inp = int(input(": "))
                        if inp == 1:
                            name = input("\nWho would you like to assign this task to?: ")
                            t['username'] = name
                            Write_tasks()
                            print("\nTasks username has been changed.")

                        if inp == 2:
                            day = input("\nWhat would you like to set the due date to?(YYYY-MM-DD): ")
                            converted_day = datetime.strptime(day, DATETIME_STRING_FORMAT)
                            t['due_date'] = converted_day
                            Write_tasks()
                            print("\nChanged the due date of the task")
                    
                    else:
                        print("\ncant edit the task due to it already being marked as completed.")
                else:
                    print("Invalid option please try again.")


# - This will generate 2 txt files called task and user_overview.txt which documents
#   a bunch of facts about the users and tasks based on the data already given
def generate_reports(task_num_tracker, completed_task_tracker, tasks_overdue, total_users):
    with open("task_overview.txt", "w") as overview_file:
        for t in task_list:
            if t['due_date'] < datetime.now():
                tasks_overdue+=1
        overview_file.write(f'''Total number of tasks: {task_num_tracker}
Number of tasks finished: {completed_task_tracker}
Number of tasks uncompleted: {task_num_tracker-completed_task_tracker}
Number of uncompleted tasks that are overdue: {tasks_overdue}
Percentage of incomplete tasks: {(task_num_tracker/(task_num_tracker-completed_task_tracker)) * 100}%
Percentage of tasks that are overdue: {(tasks_overdue/task_num_tracker) * 100}%
''')
    
    with open("user_overview", "w") as overview_file:
        overview_file.write(f'''Total number of users: {total_users}
Total number of tasks: {task_num_tracker}''')
        for t in task_list:
            total_tasks = 0
            completed_tasks = 0
            incomplete_tasks = 0
            incomplete_overdue = 0
            for u in username_password:
                if t['username'] == u:
                    total_tasks+=1
                    if t['completed'] == True:
                        completed_tasks +=1
                    elif t['completed'] == False:
                        incomplete_tasks +=1
                        if t['due_date'] < datetime.now():
                            incomplete_overdue+=1
            overview_file.write(f'''\n\nUser: {t['username']}
\n\tTotal number of tasks assigned to this user: {total_tasks}
\tPercentage of tasks assigned to this user: {round((total_tasks/task_num_tracker)*100)}%
\tPercentage of tasks assigned to user that are completed: {round((completed_tasks/total_tasks)*100)}%
\tPercentage of tasks assigned to user that are incomplete: {round((incomplete_tasks/total_tasks)* 100)}%
\tPercentage of tasks assigned to user that are incomplete and overdue: {round((incomplete_overdue/total_tasks)* 100)}%
''')


# Log in system
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

while True:
    # - Presenting the menu to the user and making sure that the
    #   user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        Reg_user(total_users)
    elif menu == 'a':
        Add_task(task_num_tracker)
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine(completed_task_tracker)
    elif menu == "gr":
        generate_reports(task_num_tracker, completed_task_tracker, tasks_overdue, total_users)
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}\n")
        print("Tasks.txt: \n")
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r")as file:
                temp = file.read().split('\n')
                for t in temp:
                    t = t.split(';')
                    print(f'''Task: {t[0]}
User: {t[1]}
Title: {t[2]}
Description: {t[3]}
Due date: {t[4]}
Assigned date: {t[5]}
Completed: {t[6]}''')
        else:
            if_task_doesnt_exist()
            
        print("\nUser.txt:\n")
        if os.path.exists("tasks.txt"):
            with open("user.txt", 'r')as file:
                temp = file.read().split('\n')
                for t in temp:
                    t = t.split(';')
                    print(f"Username: {t[0]}\nPassword: {t[1]}\n")
        else:
            if_user_doesnt_exist(total_users)
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        if curr_user != 'admin':
            print("You dont have the permission to use this option")
        print("You have made a wrong choice, Please Try again")