import os # checking the file path and clearing the terminal
import argparse # main structure to take terminal command to variables
import json # data format
import sys # for analyzing the terminal command

# File for the data:
DATA_FILE = "taskdata.json"

# =========================== FUNCTIONS ===========================
# prints the variable from the terminal commands
def TerminalCmdInfo():
    print(sys.argv)

def clear():
    '''
    to clear the terminal for a better console UI
    '''
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE,"r") as f:
        return json.load(f)

def add_to_data(id,title,status):
    data = load_data()
    data.append({
        "id":id,
        "title":title,
        "status":status
    })
    write_data(data)

def write_data(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f,indent=4)

def create_task_id():
    data = load_data()
    ids = []
    for i in range(len(data)):
        ids.append(data[i]["id"])
    try:
        next_id = max(ids)+1
    except:
        next_id = 1
    return next_id

def update_data(id,new_title):
    data = load_data()
    if data == []:
        print(">>> NOTHING TO SHOW HERE")
        return
    for i in range(len(data)):
        if data[i]["id"] == id:
            data[i]["title"] = new_title
            print(">>> Task updated.")
            write_data(data)
            return
    print(">>> No such task found.")

def delete_data(id):
    data = load_data()
    for i in range(len(data)):
        if data[i]["id"] == id:
            data.pop(i)
            print(">>> Task deleted.")
            write_data(data)
            return
    print(">>> No such task found.")

def show_data(filter=None):
    data = load_data()
    if data == []:
        print(">>> NOTHING TO SHOW HERE")
        return
    print(f"{'ID':<5}  {'TASK':<30}  {'STATUS':<12}")
    print("-" * 50)
    if filter:
        for task in data:
            if task['status'] == filter:
                print(f"{task['id']:<5}  {task['title']:<30}  {task['status']:<12}")
    else:
        for task in data:
            print(f"{task['id']:<5}  {task['title']:<30}  {task['status']:<12}")
        

# =========================== ARGPARSE ============================
description_text = '''
Task manager for you that can add, remove update and mark 

version    : 1.0

add        : adds new task to list
                - python taskmgr.py add "title"
                - python taskmgr.py add "title" --mark "mark"
update     : updates name of an existing task
                - python taskmgr.py update task_id "new_title"
delete     : deletes an existing task
                - python taskmgr.py delete task_id
list       : shows all the tasks
                - python taskmgr.py list
                - python taskmgr.py list --filter "mark"
'''
cmd = argparse.ArgumentParser(description=description_text,formatter_class=argparse.RawDescriptionHelpFormatter)
cmd.add_argument(
    "-v","--version",
    action="store_true",
    help="show version"
)
subcmd = cmd.add_subparsers(dest="command")

#    ======================== commands ========================

#                ============== add ==============
add_cmd = subcmd.add_parser("add",help="python taskmgr.py add 'title' --mark 'mark'")
#                   ======== arguments ========
add_cmd.add_argument("title",type = str,help = "a new task (string)")
add_cmd.add_argument(
    "-m","--mark",
    choices = ["todo","done","in-progress"],
    default = "todo",
    help = "default : todo"
)

#               ============== update ==============
update_cmd = subcmd.add_parser("update",help="python taskmgr.py update task_id 'new_title'")
#                   ========= arguments ========
update_cmd.add_argument("task_id",type = int,help = "task number (int)")
update_cmd.add_argument("new_title",type = str,help = "a new task name (string)")

#               ============== update ==============
delete_cmd = subcmd.add_parser("delete",help="python taskmgr.py delete task_id")
#                   ========= arguments ========
delete_cmd.add_argument("task_id",type = int,help = "task number (int)")

#               ============== list ==============
list_cmd = subcmd.add_parser("list",help="python taskmgr.py list --filter 'mark'")
#                  ========= arguments ========
list_cmd.add_argument(
    "-f","--filter",
    choices = ["todo","done","in-progress"],
    help = "shows all the tasks"
)

#  ======================== Finalizing ========================
args = cmd.parse_args()

#  ========================= version ==========================
if args.version:
    print("taskmgr version 1.0")
    sys.exit()

# =========================== main ============================
if args.command == "add":
    clear()
    add_to_data(create_task_id(),args.title,args.mark)
    print(">>> Task added.")
    print("\n")
    show_data()

elif args.command == "update":
    clear()
    update_data(args.task_id,args.new_title)
    print("\n")
    show_data()

elif args.command == "delete":
    clear()
    delete_data(args.task_id)
    print("\n")
    show_data()

elif args.command == "list":
    clear()
    show_data(args.filter)

# else:
#     print("Wrong command\n try --h or --help to know what to do")