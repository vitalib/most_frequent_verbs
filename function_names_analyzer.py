import ast
import collections
import os

from nltk import pos_tag


def is_verb(word):
    if not word:
        return False
    part_of_speach = pos_tag([word])
    return 'VB' in part_of_speach[0][1]


def fetch_python_files_from_dir(dir_path):
    for dir_name, subdirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):
                yield os.path.join(dir_name, file)


def get_ast_tree(file_content):
    try:
        tree = ast.parse(file_content)
    except SyntaxError:
        tree = None
    return tree


def get_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def get_trees_with_filenames(dir_path, include_file_content=False):
    for filename in fetch_python_files_from_dir(dir_path):
        file_content = get_file_content(filename)
        tree = get_ast_tree(file_content)
        tree_info = {'title': filename, 'tree': tree}
        if include_file_content:
            tree_info['file_content'] = file_content
        yield tree_info


def get_trees(dir_path):
    for filename in fetch_python_files_from_dir(dir_path):
        with open(filename, 'r', encoding='utf-8') as file:
            file_content = file.read()
        yield get_ast_tree(file_content)


def get_non_empty_trees(trees):
    yield from (tree for tree in trees if tree)


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
