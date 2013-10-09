# -*- coding: cp1252 -*-
import re
import csv
import operator
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

#pre-seeded tags
top_list = {'osx': 51812, 'sharepoint': 15701, 'xcode': 52513, 'rest': 14426, 'datetime': 12427, 'node.js': 20280,
          'session': 14695, 'linq-to-sql': 11376, 'mysql': 172182, 'query': 28931, 'xml': 64157, 'cakephp': 13882,
          'java-ee': 13579, 'ruby-on-rails': 116883, 'ms-access': 12743, 'flash': 27458, 'authentication': 15932,
          'apache2': 27619, 'forms': 30026, 'matlab': 18149, 'multithreading': 37619, 'variables': 13871,
          'homework': 32535, 'css3': 13332, 'flex': 22248, 'string': 37802, 'python': 184928, 'vba': 14490,
          'internet-explorer': 21583, 'windows-7': 58487, 'ssl': 13545, 'facebook': 43393, 'ssh': 17866,
          'unit-testing': 19166, 'vim': 14790, 'nhibernate': 14863, 'permissions': 13341, 'design-patterns': 14634,
          'silverlight': 26932, 'sorting': 13541, 'qt': 20586, 'android-layout': 14609, 'gui': 13275, '.net': 162359,
          'list': 21628, 'c++': 199280, 'css': 129107, '.htaccess': 21022, 'security': 34499,
          'windows-server-2008': 16323, 'mod-rewrite': 13275, 'calculus': 15679, 'google': 14480, 'centos': 13523,
          'spring': 26995, 'testing': 13805, 'web-services': 30141, 'design': 14833, 'plugins': 15560, 'loops': 11494,
          'web-applications': 12147, 'php': 392451, 'sql-server-2008': 29743, 'command-line': 17475, 'scala': 15343,
          'actionscript-3': 27111, 'delphi': 21367, 'sql-server-2005': 18812, 'winforms': 37370, 'generics': 12901,
          'real-analysis': 14853, 'email': 26888, 'math': 12826, 'redirect': 13338, 'hibernate': 24880, 'xslt': 12785,
          'winapi': 16422, 'javascript': 365623, 'drupal': 12895, 'maven': 12482, 'ajax': 62239, 'html5': 31243,
          'ubuntu': 43002, 'apache': 26990, 'networking': 38323, 'bash': 33116, 'jquery': 305614, 
          'listview': 13760, 'postgresql': 18471, 'google-maps': 16319, 'vb.net': 46653, 'opengl': 11813, 'gwt': 13235,
          'mvc': 15325, 'swing': 25872, 'pdf': 15619, 'browser': 11742, 'jquery-ajax': 14113, 'firefox': 21427,
          'ruby-on-rails-3': 43166, 'probability': 12930, 'active-directory': 12460, 'image': 32280, 'parsing': 17471,
          'cocoa': 26062, 'jquery-ui': 21395, 'unix': 20205, 'api': 22037, 'linux': 127606, 'table': 13730,
          'linear-algebra': 15457, 'ios5': 12090, 'sockets': 17598, 'regex': 59223, 'git': 29377, 'java': 412189,
          'codeigniter': 18259, 'google-app-engine': 18505, 'encryption': 11417, 'perl': 28641,
          'visual-studio-2008': 15500, 'json': 43451, 'wordpress': 30556, 'iphone': 183573, 'dns': 16179,
          'memory': 17362, 'function': 17967, 'shell': 22309, 'iis': 18552, 'google-chrome': 20408, 'c#': 463526,
          'xaml': 15665, 'search': 16901, 'linq': 29543, 'oop': 19016, 'logging': 13849, 'ruby': 73502, 'ipad': 27098,
          'exception': 13366, 'tomcat': 14848, 'arrays': 50055, 'asp.net-mvc-3': 34422, 'dom': 12360, 'eclipse': 44092,
          'database-design': 11759, 'url': 15163, 'zend-framework': 15609, 'cocoa-touch': 26314,
          'video': 14300, 'powershell': 13518, 'visual-studio-2010': 34433, 'debugging': 18936, 'sqlite': 20741,
          'uitableview': 15544, 'nginx': 11889, 'objective-c': 133932, 'magento': 15082, 'file': 23406,
          'facebook-graph-api': 13830, 'asp.net': 177334, 'sql-server': 74921, 'windows-phone-7': 17245, 'excel': 24025,
          'windows-xp': 20193, 'html': 165507, 'wcf': 31490, 'performance': 39377, 'android': 320622, 'events': 15884,
          'visual-studio': 30148, 'templates': 16900, 'jsf': 14650, 'http': 19768, 'mongodb': 15499, 'object': 11765,
          'ios': 136080, 'c#-4.0': 14168, 'caching': 12960, 'mac': 11698, 'jsp': 17012, 'sql': 132465, 'date': 13697,
          'wpf': 65836, 'asp.net-mvc': 57859, 'tsql': 20544, 'class': 18363, 'svn': 19727, 'audio': 14966,
          'algorithm': 29773, 'database': 59799, 'windows': 98100, 'optimization': 14304, 'entity-framework': 23978,
          'django': 52030, 'visual-c++': 13740, 'debian': 12570, 'oracle': 29382, 'validation': 17713}
minvalue = min(top_list.values())
count_items = sum(1 for x in top_list.values())
sum_items = sum(top_list.values())

#calculate MLE
logsum = 0
for key in top_list:
    logsum += math.log(top_list[key] / minvalue)

alpha = 1 + count_items * logsum

top_list_estimators ={}
for key in top_list:
    estimator = (alpha - 1) / minvalue * math.pow(top_list[key] / minvalue, -alpha) * 1.
    top_list_estimators[key] = estimator

top_list.update({'matlab': minvalue})
special = {'matlab': minvalue}
#'r': 26863, 'c': 95453

#open SampleTest and apply words in title to
ofile = open('Test2.csv', "wb")
writer = csv.writer(ofile, quoting=csv.QUOTE_ALL)
head_tag = ['Id', 'Tags']
writer.writerow(head_tag)

test_file = open('Test.csv', "rb")
test_reader = csv.reader(test_file)
for row in test_reader:
    new_row = [x.lower() for x in row]
    if new_row[0] == 'id':
        continue
    else:
        #look for top words in the row and add
        word_list = ""
        for word in top_list:
            if word in new_row[1] or word in new_row[2]:
                word_list += word + " " 

        #look for special words
        for word in special:
            title_search = re.search('\\b' + word + '\\b', new_row[1], flags=re.IGNORECASE)
            body_search = re.search('\\b' + word + '\\b', new_row[2], flags=re.IGNORECASE)
            if title_search:
                word_list += title_search.group() + " "
            if body_search:
                word_list += body_search.group() + " "
            #print word_list

        #if word list is still empty add up most common words in title and body

    #rate the relevance of the words
    word_count_list= list(word_list.split())
    word_count_dict = {}
    for word in word_count_list:
        #if it's already in the dictionary add the value
        if word in word_count_dict:
            word_count_dict[word] += top_list_estimators[word]
        else:
            word_count_dict[word] = top_list_estimators[word]            
            
    #sort them in order of relevance
    sorted_word = sorted(word_count_dict.iteritems(), key=operator.itemgetter(1), reverse=True)

    #show the top x values
    break_value = 3
    row_value_list = []
    if len(sorted_word)>=break_value:
        for word in range(break_value):
            row_value_list.append(sorted_word[word][0])
    elif len(sorted_word) > 0 and len(sorted_word)<break_value:
        for word in range(len(sorted_word)):
            row_value_list.append(sorted_word[word][0])  

    row_values = " ".join(row_value_list)
    #print row_values
    write_row = [new_row[0], row_values]
    writer.writerow(write_row)

test_file.close()
ofile.close()

