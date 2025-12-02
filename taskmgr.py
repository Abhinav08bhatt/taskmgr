import os # checking the file path and clearing the terminal
import argparse # main structure to take terminal command to variables
import json # data format
import sys # for analyzing the terminal command

import sqlite3
# ======================= DATABASE CHECK ===========================
DATA_FILE = "taskdata.db"

def get_conn():
    return sqlite3.connect(DATA_FILE)

def init_db():
    conn = get_conn()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            priority TEXT NOT NULL
        );'''
        )
    conn.commit()
    conn.close()
# ===================================================================

# ====================== RICH MODULE CHECK ==========================
def try_install_rich():
    print(">>> Module 'rich' not found. Attempting installation...")

    commands = [
        f"{sys.executable} -m pip install rich",
        "pip install rich",
        "pip3 install rich",
        f"{sys.executable} -m pip3 install rich"
    ]

    for cmd in commands:
        print(f">>> Trying: {cmd}")
        result = os.system(cmd)
        if result == 0:  # installation succeeded
            try:
                import rich  # try to import again
                print(">>> Successfully installed 'rich'.")
                return True
            except ImportError:
                pass  # installation said success but import failed

    # If all attempts failed:
    print("\n>>> Could NOT install the 'rich' module.")
    print(">>> Please install it manually using one of the following commands:")
    print("    pip install rich")
    print("    pip3 install rich")
    print(f"    {sys.executable} -m pip install rich")
    print("\n>>> Exiting...")
    return False

try:
    import rich
except ImportError:
    if not try_install_rich():
        sys.exit(1)

from rich.console import Console
from rich.table import Table
# =================================================================

# =========================== FUNCTIONS ===========================
# prints the variable from the terminal commands
def TerminalCmdInfo():
    print(sys.argv)

def clear():
    '''
    to clear the terminal for a better console UI
    '''
    os.system('cls' if os.name == 'nt' else 'clear')

def add_task(title,status,priority):
    conn = get_conn()
    conn.execute(
        "INSERT INTO tasks (title, status, priority) VALUES (?, ?, ?)",(title, status, priority)
    )
    conn.commit()
    conn.close()

def update_task(task_id, new_title=None, status=None, priority=None):
    conn = get_conn()
    cur = conn.execute("SELECT title, status, priority FROM tasks WHERE id=?", (task_id,))
    row = cur.fetchone()

    if row is None:
        print(">>> No such task found.\n\n")
        return

    if new_title is not None:
        final_title = new_title
    else:
        final_title = row[0]
    if status is not None:
        final_status = status
    else:
        final_status = row[1]
    if priority is not None:
        final_priority = priority
    else:
        final_priority = row[2]

    conn.execute('''
        UPDATE tasks
        SET title=?, status=?, priority=?
        WHERE id=?''', 
        (final_title, final_status, final_priority, task_id)
        )
    conn.commit()
    conn.close()

    print(">>> Task updated.\n\n")

def delete_task(task_id):
    conn = get_conn()
    cur = conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

    if cur.rowcount == 0:
        print(">>> No such task found.\n\n")
    else:
        print(">>> Task deleted.\n\n")

def clear_all_tasks():
    conn = get_conn()
    conn.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()
    print(">>> All tasks erased.\n\n")

def list_tasks(filter_value=None):
    conn = get_conn()
    cursor = conn.cursor()

    if filter_value in ["todo","done","in-progress"]:
        cursor.execute("SELECT * FROM tasks WHERE status=?", (filter_value,))
    elif filter_value in ["low","normal","important"]:
        cursor.execute("SELECT * FROM tasks WHERE priority=?", (filter_value,))
    else:
        cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(">>> NOTHING TO SHOW HERE\n\n")
        return

    table = Table(title="Task Manager", expand=False)

    table.add_column("ID", style="cyan", justify="center", min_width=4)
    table.add_column("Title", style="white", justify="left", min_width=40)
    table.add_column("Status", justify="center", min_width=12)
    table.add_column("Priority", justify="center", min_width=12)

    for row in rows:
        task_id     = str(row[0])
        title       = row[1]
        status      = row[2]
        priority    = row[3]

        if status == "done":
            status_display = f"[green]{status}[/green]"
        elif status == "in-progress":
            status_display = f"[blue]{status}[/blue]"
        else:  # todo
            status_display = f"[red]{status}[/red]"

        if priority == "low":
            priority_display = f"[yellow]{priority}[/yellow]"
        elif priority == "normal":
            priority_display = f"[orange1]{priority}[/orange1]"
        else:  # important
            priority_display = f"[red]{priority}[/red]"

        table.add_row(task_id, title, status_display, priority_display)

    console = Console()
    console.print(table)


# =========================== ARGPARSE ============================
description_text = '''
Task manager for you that can add, remove update and status 

version    : 1.0

add        : adds new task to list
                - python taskmgr.py add "title"
                - python taskmgr.py add "title" --status "status"
                - python taskmgr.py add "title" --priority "priority"
update     : updates name of an existing task
                - python taskmgr.py update task_id "new_title"
                - python taskmgr.py update task_id --status "status"
                - python taskmgr.py update task_id --priority "priority"
delete     : deletes an existing task
                - python taskmgr.py delete task_id
list       : shows all the tasks
                - python taskmgr.py list
                - python taskmgr.py list --filter "status"
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
add_cmd = subcmd.add_parser("add",help="python taskmgr.py add 'title' --status 'status'")
#                   ======== arguments ========
add_cmd.add_argument("title",type = str,help = "a new task (string)")
add_cmd.add_argument(
    "-s","--status",
    choices = ["todo","done","in-progress"],
    default = "todo",
    help = "default : todo"
)
add_cmd.add_argument(
    "-p","--priority",
    choices = ["low","normal","important"],
    default = "normal",
    help = "default : normal"
)

#               ============== update ==============
update_cmd = subcmd.add_parser("update",help="python taskmgr.py update task_id 'new_title'")
#                   ========= arguments ========
update_cmd.add_argument("task_id",type = int,help = "task number (int)")
update_cmd.add_argument("new_title",type = str,nargs="?", help="new title (string) (optional)")
update_cmd.add_argument(
    "-s","--status",
    choices = ["todo","done","in-progress"],
    default = "todo",
    help = "default : todo"
)
update_cmd.add_argument(
    "-p","--priority",
    choices = ["low","normal","important"],
    default = "normal",
    help = "default : normal"
)

#               ============== update ==============
delete_cmd = subcmd.add_parser("delete",help="python taskmgr.py delete task_id")
#                   ========= arguments ========
delete_cmd.add_argument("task_id",type = int,help = "task number (int)")

#               ============== list ==============
list_cmd = subcmd.add_parser("list",help="python taskmgr.py list --filter 'status'")
#                  ========= arguments ========
list_cmd.add_argument(
    "-f","--filter",
    choices = ["todo","done","in-progress"],
    help = "shows all the tasks"
)

#              ============== clear ==============
clear_cmd = subcmd.add_parser("clear", help="Erase all tasks")


#  ======================== Finalizing ========================
args = cmd.parse_args()
init_db()

#  ========================= version ==========================
if args.version:
    print("taskmgr version 2.0")
    sys.exit()

# =========================== main ============================
if args.command == "add":
    clear()
    add_task(args.title, args.status, args.priority)
    list_tasks()

elif args.command == "update":
    clear()
    update_task(args.task_id, args.new_title, args.status, args.priority)
    list_tasks()

elif args.command == "delete":
    clear()
    delete_task(args.task_id)
    list_tasks()

elif args.command == "list":
    clear()
    list_tasks(args.filter)

elif args.command == "clear":
    sure = input("This command will erase all the tasks. Are you sure [y/n] : ")
    if sure == "y":
        clear()
        clear_all_tasks()
    print(">>> Task not erased.\n\n")
    list_tasks()