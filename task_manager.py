# Task 25
# This program is a simple task manager for a small business
# It will work with 2 files: User.txt is used for password
# text.txt Is used for tasks
# The user will also have a option to review his own tasks marking it complete and not complete
# It will also generate 2 files in which the task data will be displayed

# Imported fuctions
from datetime import datetime

# Opened files and created empty lists
task_file = open('text1.txt', 'r+')
user_file = open('user.txt', 'r+')
file_username = []
file_password = []

# Split file into lists
for line in user_file:
    file_data = line.split(', ')
    file_username.append(file_data[0])
    file_password.append(file_data[1].strip("\n"))
user_file.seek(0)

# Created password checker function
def login():
    login = False
    while not login:
        username = input('Enter your username: ')
        password = input('Enter your password: ')

        for i in range(len(file_username)):
            if username == file_username[i] and password == file_password[i]:
                print('Password accepted')
                return username

        if not login:
            print("You have entered the incorrect login credentials.")

# Defined function to add user if username exits can't add new user
def reg_user():
    if username == "admin":
        user = True
        
        if username != file_username:
            user = False
            print("\nRegister New User")
            new_username = input("Please enter new user's username: ")

            if new_username in file_username:
                print("Error username already exists")
                reg_user()

            new_password = input("Please enter new user's password: ")
            conf_password = input("Please confirm password: ")

            if (new_password == conf_password):
                new_user = "\n"+new_username + ", " + new_password
                user_file.write(new_user)
                user_file.close()
    else:
        print("You are not allowed to register new users")

# Defined add task function to add new tasks and assign them to users
def add_task():
    print("\nInput New Task")
    task_user = input("Assign a username to this task: ")
    task_title = input("Enter the title of this task: ")
    task_descr = input("Please describe the task: ")
    task_due = input("Enter due date for example 20 Oct 2019: ")
    date_added = datetime.date(datetime.now())

# Specified file to write a new line to the file
    for line in task_file:
        task_file.write('\n')
        task_file.write(f"{task_user}, {task_title}, {task_descr}, {date_added}, {task_due}, No/n")

# Defined view all function to view all tasks
def view_all():
    for line in task_file:
        tasks = line.split(', ')
        print(
            f'''Username: {tasks[0]}
Task to be performed: {tasks[1]}
Instructions: {tasks[2]}
Date added: {tasks[3]}
Due Date: {tasks[4]}
Is the task completed: {tasks[5]}''')

# Defined view all function and allowed user to change if Task is completed or not
def view_mine():
    count = 0
    user_tasks = []
    for line in task_file:
        tasks = line.split(', ')

        if username == tasks[0]:
            # Colleccting tasks info
            user_tasks.append(tasks)
            count += 1
            print(
                f'''
{count}
Username: {tasks[0]}
Task to be performed: {tasks[1]}
Instructions: {tasks[2]}
Date added: {tasks[3]}
Due Date: {tasks[4]}
Is the task completed: {tasks[5]}''')

    choice = int(input("Select a task by entering its number or enter -1 to return to main menu: "))

    if choice == -1:
        menu()
    else:
        print(user_tasks)

        edit_choice = int(input("Do you want to 1. Mark as completed? 2. Edit"))
        if edit_choice == 1:
            user_tasks[choice - 1][5] = "Yes\n"

        elif edit_choice == 2:
            user_tasks[choice - 1][2] = input("Enter text you want to edit")

        print(user_tasks)
        other_file = open("text1.txt", "w")

        for task in user_tasks:
            other_file.write(", ".join(task))

        other_file.close()

# Defined task overview function opened file to display statistics
def task_overview():
    overview = open('task_overview.txt', 'w+')

    completed = 0
    count = 0
    uncompleted = 0
    uncompleted_overdue = 0
    task_overdue = 0

    for line in task_file:
        line = line.split(", ")


        task_status = line[5].strip("\n")
        count += 1

        if task_status == "Yes":
            completed += 1
        else:
            uncompleted += 1

        due_date = line[4]
        due_date = datetime.strptime(due_date, "%d %b %Y")
        current_date = datetime.now()
        is_overdue = current_date > due_date

        if is_overdue and task_status == "No":
            uncompleted_overdue += 1
            
        if current_date > due_date:
            task_overdue += 1

    task_file.seek(0)

    perc_uncompleted = (uncompleted / count) * 100
    perc_uncompl_overdue = (uncompleted_overdue / count) * 100
    perc_overdue = (task_overdue / count) * 100
    
    overview.write(f'''
    Total tasks: {count}
    Total completed tasks: {completed}
    Total uncompleted tasks: {uncompleted}
    Percentage uncompleted and overdue: {perc_uncompl_overdue}
    Percentage uncompleted: {perc_uncompleted}
    Percentage overdue: {perc_overdue}
    ''')

    overview.close()

# Defined user_statistics to open and write statistics to a file
def user_statistics():
    user_overview = open('user_overview.txt', 'w+')

    total_tasks = 0
    total_users = 0
    tasks_user = 0
    user_overdue = 0
    user_completed = 0
    user_uncompleted = 0

    for line in task_file:

        line = line.strip('\n').split(', ')

        if line[0] == username:
            tasks_user += 1

        total_tasks += 1
        total_users += 1
        
        if line[0] == username and line[5] == "Yes":
            user_completed += 1
            
        if line[0] == username and line[5] == "No":
            user_uncompleted += 1
    
        due_date = line[4]
        due_date = datetime.strptime(due_date, "%d %b %Y")
        current_date = datetime.now()
        is_overdue = current_date > due_date

        if line[0] == username and line[5] == "No" and is_overdue:
            user_overdue += 1

    task_file.seek(0)

    perc_assigned_task = (tasks_user / total_tasks) * 100
    perc_completed_task = (user_completed / tasks_user) * 100
    perc_uncompleted_task = (user_uncompleted / tasks_user) * 100
    perc_overdue = (user_overdue / tasks_user) * 100
    
    user_overview.write(f'''
    Total number of users: {total_users}
    Total number of tasks: {total_tasks}
    Percentage tasks assigned to user: {perc_assigned_task}
    Percentage tasks completed by user: {perc_completed_task}
    Percentage still to be completed by user: {perc_uncompleted_task}
    Percenage of tasks not completed and overdue: {perc_overdue}''')
    
    user_overview.close()
    
        
# Defined menu
def menu():
    print("\nPlease select one of the following options: ")
    print("r - register user")
    print("a - add task")
    print("va - view all tasks")
    print("vm - view my tasks")
    print("gr - generate reports")
    if username == 'admin':
        print("ds - display statistics")
    print("e - exit")
    menu_choice = input("What would you like to do: ").lower()

# Called all fuctions 
    if menu_choice == "r":
        reg_user()

    if menu_choice == "a":
        add_task()

    if menu_choice == "va":
        view_all()

    if menu_choice == "vm":
        view_mine()

    if menu_choice == "gr":
        task_overview()
        user_statistics()
        
    if menu_choice == "ds":
        
    # Got total tasks and total users printed out results
        total_tasks = len(task_file.readlines())
        print("The total number of tasks are:", total_tasks)
        total_users = len(file_username)
        print("The total number of tasks are: ", total_users)
   
    # Ends all the programs
    if menu_choice == "e":
        task_file.close()
        user_file.close()

# Called functions
username = login()
menu()
