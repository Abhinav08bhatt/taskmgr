# `taskmgr.py`
Solution for the [task-tracker](https://roadmap.sh/projects/task-tracker) challenge from [roadmap.sh](https://roadmap.sh).

## How to run
Clone the repository and run the following command:
```bash
git clone https://github.com/Abhinav08bhatt/taskmgr
cd task-tracker
```

## CLI commands :

#### 1. Add a task :
- Base command :
```bash
    python taskmgr.py add "title"
```
- Other commands :
```bash
    python taskmgr.py add "title" --status "status"
```
```bash
    python taskmgr.py add "title" --priority "priority"
```
```bash
    python taskmgr.py add "title" --status "status" --priority "priority"
```
- `title` : str : positional
- `status` : str : optional (done,todo,in-progress)
- `priority` : str : optional (low,normal,important)

#### 2. Update a task:
```bash
    python taskmgr.py update task_id "new_title"
```
- Other commands :
```bash
    python taskmgr.py update task_id --status "status"
```
```bash
    python taskmgr.py update task_id --priority "priority"
``` 
```bash
    python taskmgr.py update task_id "new_title --status "status" --priority "priority"
```
- `task_id` : int : positional
- `new_title` : str : positional
- `status` : str : optional (done,todo,in-progress)
- `priority` : str : optional (low,normal,important)
#### 3. Delete a task:
```bash
    python taskmgr.py delete task_id
```
- `task_id` : int : positional
#### 4. List all task:
```bash
    python taskmgr.py list
```
- Other commands :
```bash
    python taskmgr.py list --filter "status"
```
- `status` : str : optional (done,todo,in-progress)

## Version Info :

<details><summary><strong>Version 1.0</strong></summary>

#### Supported actions : (`subparsers`)
- Add a task (`add`)
- Update a task (`update`)
- Delete a task (`delete`)
- List tasks (`list`)
- Mark a task as:(`--status`) 
    - todo (default)
    - done 
    - in-progress
- List tasks filtered by: (`--filter`)
    - todo
    - done
    - in-progress

#### Data Structure used in version 1.0: (`json`)
```json
[
    {
        "id":1,
        "title":"Buy Eggs",
        "status":"todo"
    },
    {
        "id": 2,
        "title": "Learn Python",
        "status": "in-progress"
    }
]
```
</details>

---

<details><summary><strong>Version 2.0</strong> (latest)</summary>

#### Required module : `rich`
- Windows , Linux , Mac
```bash
    pip install rich
```
- Arch
```
    sudo pacman -S python-rich
```        

#### What's new?

- ##### Features added :
    - We can prioritize a task. (low,normal,important)
    - We can filter the tasks based on their priority.
    - The table format now looks beautiful. (cross-platform)
        - thanks to `rich` library in python

- ##### Changes made :
    - Introduced the **sqlite** database

#### Supported actions : (`subparsers`)
- Add a task (`add`)
- Update a task (`update`)
- Delete a task (`delete`)
- List tasks (`list`)
- Mark a task as: (`--status`) 
    - todo (default)
    - done 
    - in-progress
- Priorities a task as: (`--priority`)
    - low
    - normal (default)
    - important
- List tasks filtered by: (`--filter`)
    - todo
    - done
    - in-progress
    - low 
    - normal
    - important

#### Data Structure used in version 2.0: (`sqlite`)
```sql
+----+-------------------+--------------+-----------+
| id | title             | status       | priority  |
+----+-------------------+--------------+-----------+
| 1  | Buy Eggs          | todo         | normal    |
| 2  | Learn Python      | in-progress  | important |
| 3  | Clean room        | done         | low       |
+----+-------------------+--------------+-----------+
```
</details>
