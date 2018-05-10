# Function's names analyzer 

Determine most used python functions in given directory and verbs that were utilized in names of these functions.

## Getting Started
Script should be run in Python3, dependencies must be installed as follows:
```bash
pip install -r requirements.txt
```

Example of utilization 
```python
# test.py
import function_names_analyzer 

dir_path = '/usr/lib/python3.6'
most_used_functions = function_names_analyzer.get_top_functions_names_in_path(dir_path)
most_used_verbs_in_functions_names = function_names_analyzer.get_top_verbs_in_path(dir_path)

print(most_used_functions)
print(most_used_verbs_in_functions_names)
```

```bash
python3 test.py
[('decode', 201), ('encode', 200), ('close', 152), ('getregentry', 123), ('write', 61), ('run', 58), ('transform', 52), ('reset', 50), ('read', 46), ('get', 42)]
[('get', 760), ('is', 188), ('add', 176), ('find', 131), ('run', 112), ('make', 104), ('do', 77), ('remove', 65), ('has', 44), ('save', 39)]
```




