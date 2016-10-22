# -*- coding: utf-8 -*-
"""
Created on Sat May 16 22:40:37 2016

@author: chenshangyu
"""

import csv
from collections import defaultdict
import pandas as pd
import numpy as np
from matplotlib import *
#from StringIO import StringIO

#general function
def quotforjavascript(string):
     strnew = "\\\""
     parts = string.split("\"")
     string = strnew.join(parts)
     strnew = "\\\'"
     parts = string.split("\'")
     string = strnew.join(parts[0:])
     return string




#function for chart3
def count_column(col):
    dic = defaultdict(int)
    csvdata = csv.DictReader(open("Melbourne_Public_Artwork.csv"))
    for row in csvdata:
        dic[row[col]] += 1
    return dic


def main_data_chart3():
    main_dict = defaultdict(dict)
    csvdata = csv.DictReader(open("Melbourne_Public_Artwork.csv"))
    for row in csvdata:
        address = row["Address Point"]
        spilt_add = address.split(", ")
        if len(spilt_add) != 1:
                suburb = spilt_add[-1]
                if (not main_dict[row["Xorg"]]):
                    main_dict[row["Xorg"]]=defaultdict(int)
                main_dict[row["Xorg"]][suburb]+= 1
    return (main_dict)



def main_data_json():
    dataneed = count_column("Xorg")
    datalist = dataneed.items()
    datajson = """[{name: '%s', y: %d, drilldown: '%s'}"""%(datalist[0][0], datalist[0][1], datalist[0][0])
    for i in range(1, len(datalist)):
        datajson = datajson + ", {name: '%s', y: %d, drilldown: '%s'}"%(datalist[i][0], datalist[i][1], datalist[i][0])
    datajson = datajson + "]}], "
    return (datajson)


def drilldowndata():
    data_format = """{name: '%s',\nid: '%s', data: [%s]}"""
    dict_of_subtable = main_data_chart3()
    list_of_subtable = dict_of_subtable.items()

    list_of_subdict = (list_of_subtable[0][1]).items()
    data_data = "['%s', %d]"%(list_of_subdict[0][0], list_of_subdict[0][1])
    for j in range(1, len(list_of_subdict)):
         data_data = data_data + ", ['%s', %d]"%(list_of_subdict[j][0], list_of_subdict[j][1])
    series = data_format%(list_of_subtable[0][0], list_of_subtable[0][0], data_data)
    totle_subdata = series

    for i in range(1, len(list_of_subtable)):
        list_of_subdict = (list_of_subtable[i][1]).items()
        data_data = "['%s', %d]"%(list_of_subdict[0][0], list_of_subdict[0][1])
        for j in range(1, len(list_of_subdict)):
             data_data = data_data + ", ['%s', %d]"%(list_of_subdict[j][0], list_of_subdict[j][1])
        series = data_format%(list_of_subtable[i][0], list_of_subtable[i][0], data_data)
        totle_subdata = totle_subdata + ",\n%s"%(series)
    return (totle_subdata)


#def white_zero(data, color='beige'):
#    attr = 'background-color: {}'.format(color)
#    is_zero = data == 0
#    return [attr if v else '' for v in is_zero]



from IPython.display import HTML

#import seaborn as sns


def hover(hover_color="gray"):
    return dict(selector="tr:hover", props=[("background-color", "%s" % hover_color)])


def highlight_max(s):
    is_max = s == s.max()
    return ['background-color: pink' if v else '' for v in is_max]



def pivot_table(filter_attribute, greater_than, less_than, row, col, aggregate_func, value):
    data = pd.read_csv("Melbourne_Public_Artwork.csv")
    data.head()
    data = data.where((data[filter_attribute] <= less_than) & (data[filter_attribute] >= greater_than))
    if aggregate_func=="MAX":
        table = pd.pivot_table(data, index=[row], values=value, columns=[col], aggfunc=[max], fill_value=0)
    elif aggregate_func=="MIN":
        table = pd.pivot_table(data, index=[row], values=value, columns=[col], aggfunc=[min], fill_value=0)
    elif aggregate_func=="Count":
        table = pd.pivot_table(data, index=[row], values=value, columns=[col], aggfunc=[len], fill_value=0)
    elif aggregate_func=="Centre":
        table = pd.pivot_table(data, index=[row], values=value, columns=[col], aggfunc=[np.mean], fill_value=0)
    elif aggregate_func=="None":
        table = pd.pivot_table(data, index=[row], values=value, columns=[col], fill_value=0)
        
        
    styles = [hover(), dict(selector="th", props=[("font-size", "100%"), ("text-align", "center")]), dict(selector="caption", props=[("caption-side", "bottom"), ("font-size", "10%")]), dict(selector="table", props=[("border", "1"), ("align", "center")])]
    try:
        html = ('').join(table.style.set_table_styles(styles).apply(highlight_max).set_caption("Hover to highlight.\nPink is the max value in column.").render().split('\n'))
        return(html)
    except:
        return None
    





def correlation_data(X_axis, compare_with):
    main_dict = defaultdict(dict)
    comparelistdict = defaultdict(int)
    csvdata = csv.DictReader(open("Melbourne_Public_Artwork.csv"))
    for row in csvdata:
        if (not main_dict[row[X_axis]]):
            main_dict[row[X_axis]]=defaultdict(int)
        main_dict[row[X_axis]][row[compare_with]]+= 1
        comparelistdict[row[compare_with]]+= 1
    return (main_dict, comparelistdict.keys())








#percentage for each structure type
def chart2_data():
    count = 1
    structure = defaultdict(int)
    csvdata = csv.DictReader(open("Melbourne_Public_Artwork.csv"))
    for row in csvdata:
        structure[row["Structure"]] += 1
    for (key, value) in structure.items():

        if value == 1:
            structure.pop(key)
            structure["Other"]+= 1
            
    return structure


def chart2_data_sum():
    structure = chart2_data()
    sum = 0.0
    for t in structure.keys():
        sum += structure[t]
    return sum
    
def chart2_data_transform():
    structure = chart2_data()
    data = ""
    sum = chart2_data_sum()
    type_list = structure.keys()
    for t in type_list[:-1]:
        data = data + "['%s',%f], "%(t,structure[t]/sum)
    data = data + "['%s',%f] "%(type_list[-1],(structure[type_list[-1]])/sum)
    return data




#chart1
def is_number(s):
    try:
        int(s)
        return True
        
    except ValueError:
        return False

def year_record():
    reader = csv.DictReader(open("Melbourne_Public_Artwork.csv"))
    years = []
    i = 0
    for row in reader:
        if is_number(row["Art Date"][-4:]):            
            years.append(int(row["Art Date"][-4:]))
            i = i + 1
    earliest = min(years)
    lastest = max(years)
    return earliest, lastest

def chart1_sub():
    reader = csv.DictReader(open("Melbourne_Public_Artwork.csv"))
    sub_list = []
    sub_list.append("Other")
    for row in reader:
        temp_data = row["Address Point"][::-1]
        if temp_data.find(",")>=0 :
            temp_index = temp_data.find(",")
            suburb = row["Address Point"][-1*temp_index+1:]
            if suburb not in sub_list:
                sub_list.append(suburb)            
    return sub_list

def tenyearmost(start):
    reader = csv.DictReader(open("Melbourne_Public_Artwork.csv"))
    sub_dict = {}
    sub_dict["Other"]=0
    for row in reader:
        temp_data = row["Address Point"][::-1]
        if is_number(row["Art Date"][-4:]):
            if start<=int(row["Art Date"][-4:])<=start+9:
                if temp_data.find(",")>=0 :
                    temp_index = temp_data.find(",")
                    suburb = str(row["Address Point"][-1*temp_index+1:])
                    if suburb in sub_dict:
                        sub_dict[suburb]+=1
                    else:
                        sub_dict[suburb]=1
                else:
                    sub_dict["Other"] += 1
    return sub_dict

def sub_data(start,num_of_period, subname):
    temp = start
    data = "["
    subname = str(subname)
    for i in xrange(num_of_period-1):
        sub_dict = tenyearmost(temp)
        if subname in sub_dict.keys():
            data = data + "%s, "%(sub_dict[subname])
        else:
            data = data + "%d, "%(0)
        temp = temp + 10
    sub_dict = tenyearmost(temp)
    if subname in sub_dict.keys():
        data = data + "%s ]"%(sub_dict[subname])
    else:
        data = data + "%d ]"%(0)
    return data
    

    
def chart1_year():
    start,end = year_record()
    temp = start
    num_of_ten_year = (end - start)//10
    data = []
    for i in xrange(num_of_ten_year):
        data.append('%s ~ %s'%(str(temp),str(temp+9)))  
        temp = temp + 10
    data.append('%s ~ %s'%(str(temp),str(end)))
    return data

def chart1_data():
    start,end = year_record()
    temp = start
    num_of_ten_year = (end - start)//10
    data = ""
    sub_list = chart1_sub()
    for sub in sub_list[:-1]:
        data = data + "{ name: '%s', data: %s}, "%(sub,sub_data(start,num_of_ten_year+1,str(sub)))
    data = data + "{ name: '%s', data: %s} "%(sub_list[-1],sub_data(start,num_of_ten_year+1,str(sub_list[-1])))
    return data