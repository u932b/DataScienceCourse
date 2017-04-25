'''
Convert Yelp Academic Dataset from JSON to CSV
Requires Pandas (https://pypi.python.org/pypi/pandas)
By Paul Butler, No Rights Reserved
'''
import json
# import pandas as pd
import sys
import re
import pickle
import csv


def clean(string):
    string = re.sub(r'[ .*+?^${}()|[\]\/\\\']', '', string)
    # print (string)
    return string.lstrip()


def str2bool(v):
    if v.lower() in ("yes", "true", "t", "True"):
        return True
    elif v.lower() in ("False", 'false'):
        return False
    else:
        return v


def convert(x, test=False):
    ''' Convert a json string to a flat python dictionary
        which can be passed into Pandas. '''
    ob = json.loads(x)
    return_dict = {}
    for k, v in ob.items():
        if k == "attributes" and v:
            # print (v)
            nested_keys = ["Ambience", "BusinessParking", "GoodForMeal",
                           "Music", "BestNights"]
            # tmp_dict = {}
            for attr in v:
                attr = (attr.split(':', 1))
                if attr[0] in nested_keys:
                    attr2_list = (attr[1].split(','))
                    for attr2 in attr2_list:
                        attr2 = attr2.split(':')
                        key = attr[0] + "_" + clean(attr2[0])
                        value = clean(attr2[1])
                        value = str2bool(value)
                        return_dict[key] = value
                else:
                    return_dict[attr[0]] = str2bool(clean(attr[1]))
            # del ob[k]
        else:
            if isinstance(v, list):
                # print (k, v)
                return_dict[k] = ','.join(v)
            elif isinstance(v, dict):
                # print (k, v)
                for kk, vv in v.items():
                    return_dict['%s_%s' % (k, kk)] = vv
            else:
                return_dict[k] = v
                # del ob[k]
    # print ("return_dict: ", return_dict)
    return return_dict
# for json_filename in glob('*.json'):
#     csv_filename = '%s.csv' % json_filename[:-5]
count = 0
json_filename = sys.argv[1]
print (json_filename)
csv_filename = '%s.csv' % json_filename[:-5]
pickle_filename = '%s.pickle' % json_filename[:-5]
print ('Converting %s to %s' % (json_filename, csv_filename))
print ('Converting %s to %s' % (json_filename, pickle_filename))
result_dict = {}

with open(json_filename, 'r') as json_file:
    for line in json_file:
        # print (line)
        # count += 1
        line_dict = convert(line, True)
        # df = pd.DataFrame(line_dict, index=line_dict['business_id'])
        result_dict[line_dict['business_id']] = line_dict
        # if count > 1:
        # break

test = False
if not test:
    with open(pickle_filename, 'wb') as handle:
        pickle.dump(result_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # with open(csv_filename, 'wb') as f:
    #     w = csv.DictWriter(f, result_dict.keys())
    #     w.writerow(dict((fn, fn) for fn in result_dict.keys()))
    #     w.writerow(result_dict)
    # df.to_csv(csv_filename, encoding='utf-8', index=False)
