#!/usr/bin/env python

import subprocess
import os
import collections
import csv
from contextlib import contextmanager

@contextmanager
def cd(path):
    cwd = os.getcwd()
    os.chdir(path)
    yield path
    os.chdir(cwd)

if __name__ == "__main__":

    list_of_trees = collections.OrderedDict()

    with cd("/usr/local") as homebrew_directory:

        raw_output = subprocess.check_output([
            "git", "log", "--date=short", "--pretty=format:%cd %H %T",
            ])

        for line in raw_output.split("\n"):
            date, commit, tree = line.split(" ")
            if date not in list_of_trees:
                list_of_trees[date] = {
                    "tree": tree,
                    "commit": commit,
                    "count": [],
                }

        expressions = collections.OrderedDict()

        versions = [
            "total",
            "yosemite",
            "mountain_lion",
            "lion",
            "snow_leopard",
            "leopard",
            "tiger",
        ]

        for version in versions:

            if version == 'total':
                expression = 'class .* Formula'
            else:
                expression = "sha1 .* :" + version

            for date, info in list_of_trees.iteritems():

                try:
                    raw_output = subprocess.check_output([
                        "git", "grep", expression, info['tree'],
                        ])
                except: # not found
                    raw_output = ''

                info['count'].append(len(filter(None, map(str.strip, raw_output.split('\n')))))

    with open('homebrew-bottles', 'wb') as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow(['Date'] + versions)

        for date, info in list_of_trees.iteritems():

            writer.writerow([date] + info['count'])

