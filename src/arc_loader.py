import json
from pathlib import Path
from itertools import islice

# from utils.plot1task import plot_task

eval_folder = Path('../data/evaluation')
train_folder = Path('../data/training')

eval_tasks = {}
train_tasks = {}

for file in eval_folder.glob("*.json"):  # only JSON files
    with open(file, "r") as f:
        eval_tasks[file.name] = json.load(f)

for file in train_folder.glob("*.json"):  # only JSON files
    with open(file, "r") as f:
        train_tasks[file.name] = json.load(f)

eval_tasks_small = dict(islice(eval_tasks.items(), 10))
train_tasks_small = dict(islice(train_tasks.items(), 50))


# eval_tasks_synced = {k: eval_tasks[k] for k in sync}

# task = '0e671a1a.json'      #only from eval dataset

# print(eval_tasks[task]['train'])
# plot_task(eval_tasks[task])

# print(eval_tasks_small)


