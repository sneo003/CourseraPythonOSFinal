#!/usr/bin/env python3

import re
import sys
import operator
import csv

#dictionary counting errors
error_dict = {}
#dictionary with users, splitting into errors and info
user_dict = {}

with open("syslog.log") as fp:
  #read each line in log
  for line in fp:
    #strip whitespace and newline
    line = line.strip()
    #search for error message and user
    result = re.search(r"ticky: ([\w]*) (.*) \(([\w.]*)\)$", line)
    #assign username and error message type to variables
    log_code = result.group(1)
	error_msg = result.group(2)
	user = result.group(3)
	
	#add user into dictionary and add nested dictionary to user
    if user not in user_dict.keys():
	  user_dict[user] = {}
	  user_dict[user]["ERROR"] = 0
	  user_dict[user]["INFO"] = 0
	if log_code == "ERROR":
	  #add error message and count to error dictionary
	  error_dict[error_msg] = error_dict.get(error_msg, 0) + 1
	  #add error count to user dictionary
	  user_dict[user]["ERROR"] = user_dict[user].get("ERROR", 0) + 1
	if log_code == "INFO":
	  #add info count to user dictionary
	  user_dict[user]["INFO"] = user_dict[user].get("INFO", 0) + 1

fp.close()

#sort by username
user_list = sorted(user_dict.items(), key=operator.itemgetter(0))
#sort by the number of errors from most common to least common.
error_list = sorted(error_dict.items(), key=operator.itemgetter(1), reverse=True)

#insert column names into error list
error_list.insert(0, ("Error", "Count"))
#insert column names into user list
#user_list.insert(0,  ("Username", "INFO", "ERROR"))

with open('error_message.csv', 'w') as error_csv:
  writer = csv.writer(error_csv)
  writer.writerows(error_list)
  
with open('user_statistics.csv', 'w') as user_csv:
  user_csv.write("Username, INFO, ERROR" + '\n')
  for key, value in user_list:
    user_csv.write(str(key) + ',' + str(value["INFO"]) + ',' + str(value["ERROR"]) + '\n')
