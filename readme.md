# taskmgr version 1.0 (`taskmgr.py`)
Sample solution for the [task-tracker](https://roadmap.sh/projects/task-tracker) challenge from [roadmap.sh](https://roadmap.sh/projects/task-tracker).

## How to run
Clone the repository and run the following command:
```bash
git clone https://github.com/Abhinav08bhatt/taskmgr
cd task-tracker
```
## Example CLI commands :

#### 1. Add a task :
```bash
    python taskmgr.py add "title"
```
- `title` : str : positional
##### Add a task with a mark : 
```bash
    python taskmgr.py add "title" --mark "mark"
```
- `title` : str : positional
- `mark` : str : optional (done,todo,in-progress)
#### 2. Update a task:
```bash
    python taskmgr.py update task_id "new_title"
```
- `task_id` : int : positional
- `new_title` : str : positional
#### 3. Delete a task:
```bash
    python taskmgr.py delete task_id
```
- `task_id` : int : positional
#### 4. List all task:
```bash
    python taskmgr.py list
```
###### List task by status:
```bash
    python taskmgr.py list --filter "mark"
```
- `mark` : str : optional (done,todo,in-progress)


## Version 1.0 must support these actions : (`subparsers`)
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

## Data Structure using in version 1.0:
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

