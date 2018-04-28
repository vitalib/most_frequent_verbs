import ast
import collections
import os

from nltk import pos_tag


def is_verb(word):
    if not word:
        return False
    part_of_speach = pos_tag([word])
    return part_of_speach[0][1] == 'VB'


def fetch_python_files_from_dir(dir_path, files_quantity):
    for dir_name, subdirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py') and files_quantity > 0:
                yield os.path.join(dir_name, file)
                files_quantity -= 1
            if files_quantity <= 0:
                raise StopIteration()


def get_trees(dir_path, include_filenames=False,
              include_file_content=False, max_files=100):
    for filename in fetch_python_files_from_dir(dir_path, max_files):
        with open(filename, 'r', encoding='utf-8') as file:
            file_content = file.read()
        try:
            tree = ast.parse(file_content)
        except SyntaxError:
            tree = None
        tree_info = []
        if include_filenames:
            tree_info.append(filename)
        if include_file_content:
            tree_info.append(file_content)
        tree_info.append(tree)
        yield tuple(tree_info)


def get_non_empty_trees(trees):
    yield from (tree[-1] for tree in trees if tree[-1])


def get_all_names(tree):
    yield from (node.id for node in ast.walk(tree)
                if isinstance(node, ast.Name))


def get_all_function_names(tree):
    yield from (node.name.lower() for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef))


def is_predefined_name(name):
    return name.startswith('__') and name.endswith('__')


def get_all_words_from_files_in_path(path):
    trees = get_non_empty_trees(get_trees(path))
    for tree in trees:
        for name in get_all_names(tree):
            if not is_predefined_name(name):
                yield from name.split('_')


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_top_verbs_in_path(path, top_size=10):
    verbs = []
    for function_name in get_all_function_names_in_path(path):
        verbs.extend(get_verbs_from_function_name(function_name))
    return collections.Counter(verbs).most_common(top_size)


def get_all_function_names_in_path(path):
    trees = get_non_empty_trees(get_trees(path))
    for tree in trees:
        for function_name in get_all_function_names(tree):
            if not is_predefined_name(function_name):
                yield function_name


def get_top_functions_names_in_path(path, top_size=10):
    functions = get_all_function_names_in_path(path)
    return collections.Counter(functions).most_common(top_size)
