# taskmgr version 1.0 (`taskmgr.py`)

## Must support these actions : (`subparsers`)
- Add a task (`add`)
- Update a task (`update`)
- Delete a task (`delete`)
- list tasks (`list`)
- Mark a task as:(`--mark`) 
    - todo (default)
    - done 
    - in-progress
- list tasks filtered by: (`--filter`)
    - todo (default)
    - done
    - in-progress

## Example CLI commands :

#### 1. Add a task :
```py
    python taskmgr.py add "title"
```
- `title` : str : positional
##### Add a task with a mark : 
```py
    python taskmgr.py add "title" --mark "mark"
```
- `title` : str : positional
- `mark` : str : optional (done,todo,in-progress)
#### 2. Update a task:
```py
    python taskmgr.py update task_id "new_title"
```
- `task_id` : int : positional
- `new_title` : str : positional
#### 3. Delete a task:
```py
    python taskmgr.py delete task_id
```
- `task_id` : int : positional
#### 4. List all task:
```py
    python taskmgr.py list
```
###### List task by status:
```py
    python taskmgr.py list --filter "mark"
```
- `mark` : str : optional (done,todo,in-progress)

## Data Structure :
Data needs to look like this : 
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

