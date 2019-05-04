# -*- coding: utf-8 -*-
import csv
import pandas
# read csv as a dict


def read_csv(file_csv):
    csvFile = open(file_csv, 'r')
    reader = csv.DictReader(csvFile)
    dict_csv = {}
    for row in reader:
        keys = list(row.keys())
        for i in range(0, len(keys)):
            dict_csv.setdefault(keys[i], []).append(row[keys[i]])
    return dict_csv
# save dict to csv


def dict2csv(var_dict, path_csvfile):
    pandas.DataFrame(var_dict).to_csv(path_csvfile, index=False)
