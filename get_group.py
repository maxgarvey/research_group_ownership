'''/get_group.py'''
from csv import reader

def get(filename, csv_file):
    '''this method takes the filename you want the ownership of and
    the csv file's name that you're looking at. It returns the group
    that owns the file that you are interested in.'''
    csv_reader = reader(open(csv_file))
    csv_dic = {}
    for line in csv_reader:
        csv_dic[line[0].strip()] = line[1].strip()
    return csv_dic[filename]
