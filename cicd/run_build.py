#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
import re
import subprocess


def read_text(path):
    with open(path, "rb") as f:
        content = f.read().decode("utf-8")
    return content


def strip_comment_line_with_symbol(line, start):
    """
    Strip comments from line string.
    """
    parts = line.split(start)
    counts = [len(re.findall(r'(?:^|[^"\\]|(?:\\\\|\\")+)(")', part))
              for part in parts]
    total = 0
    for nr, count in enumerate(counts):
        total += count
        if total % 2 == 0:
            return start.join(parts[:nr + 1]).rstrip()
    else:  # pragma: no cover
        return line.rstrip()


def strip_comments(string, comment_symbols=frozenset(('#', '//'))):
    """
    Strip comments from json string.
    :param string: A string containing json with comments started by comment_symbols.
    :param comment_symbols: Iterable of symbols that start a line comment (default # or //).
    :return: The string with the comments removed.
    """
    lines = string.splitlines()
    for k in range(len(lines)):
        for symbol in comment_symbols:
            lines[k] = strip_comment_line_with_symbol(lines[k], start=symbol)
    return '\n'.join(lines)


def get_json_value(file_path, json_path):
    """
    Read specific field from JSON file.
    :param file_path: the absolute path for a json file
    :param json_path: json path notation.
    """
    # find absolute path
    cwd = os.getcwd()

    if not os.path.isabs(file_path):
        file_path = os.path.abspath(os.path.join(cwd, file_path))

    # fix json_path
    if json_path.startswith("$."):
        json_path = json_path.replace("$.", "", 1)

    with open(file_path, "rb") as f:
        data = json.loads(strip_comments(f.read().decode("utf-8")))

    value = data
    for part in json_path.split("."):
        if part in value:
            value = value[part]
        else:
            raise ValueError("'$.{}' not found in {}".format(json_path, file_path))
    return value


DIR_HERE = os.path.dirname(__file__)
DIR_PROJECT_ROOT = os.path.dirname(DIR_HERE)

DIR_CICD = DIR_HERE
DIR_CFT = os.path.join(DIR_PROJECT_ROOT, "cft")
DIR_REPOS = os.path.join(DIR_PROJECT_ROOT, "repos")

AWS_REGION = os.environ["AWS_DEFAULT_REGION"]
AWS_ACCOUNT_ID = os.environ["AWS_ACCOUNT_ID"]
ENVIRONMENT_NAME = os.environ["ENVIRONMENT_NAME"]

todo_list = list()
for repo_basename in os.listdir(DIR_REPOS):
    dir_repo_root = os.path.join(DIR_REPOS, repo_basename)
    if os.path.isdir(dir_repo_root):
        for tag_name in os.listdir(dir_repo_root):
            dir_tag = os.path.join(dir_repo_root, tag_name)
            if os.path.exists(os.path.join(dir_tag, "Dockerfile")):
                todo = (
                    dir_repo_root, dir_tag, repo_basename, tag_name
                )
                todo_list.append(todo)

for todo in todo_list:
    dir_repo_root, dir_tag, repo_basename, tag_name = todo
    local_repo_identifier = f"{repo_basename}:{tag_name}"
    remote_repo_identifier = f"{AWS_ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com/{ENVIRONMENT_NAME}-{repo_basename}:{tag_name}"
    logging.warning(f"Build docker image in context at {dir_tag} ...")
    try:
        subprocess.check_output(["docker", "build", "-t", local_repo_identifier, dir_tag])
        subprocess.check_output(["docker", "tag", local_repo_identifier, remote_repo_identifier])
    except subprocess.CalledProcessError as e:
        pass
