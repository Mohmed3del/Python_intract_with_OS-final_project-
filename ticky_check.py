#!/usr/bin/env python3

import re
import csv
from collections import defaultdict

# Initialize dictionaries for error messages and user statistics
error_dict = defaultdict(int)
user_dict = defaultdict(lambda: {'INFO': 0, 'ERROR': 0})

# Define regular expressions for INFO and ERROR messages
info_pattern = r"INFO ([\w]+)"
error_pattern = r"ERROR ([\w]+)"

# Open and read the syslog.log file
with open('./syslog.log', 'r') as file:
    for line in file:
        # Check for INFO messages
        info_match = re.search(info_pattern, line)
        if info_match:
            username = info_match.group(1)
            user_dict[username]['INFO'] += 1

        # Check for ERROR messages
        error_match = re.search(error_pattern, line)
        if error_match:
            error_msg = error_match.group(1)
            error_dict[error_msg] += 1

# Sort dictionaries
sorted_error_dict = sorted(error_dict.items(), key=lambda x: x[1], reverse=True)
sorted_user_list = sorted([(user, stats['INFO'], stats['ERROR']) for user, stats in user_dict.items()])

# Insert column names
sorted_error_dict.insert(0, ("Error", "Count"))
sorted_user_list.insert(0, ("Username", "INFO", "ERROR"))

# Write to CSV files
with open('error_message.csv', 'w', newline='') as error_csv:
    csv_writer = csv.writer(error_csv)
    csv_writer.writerows(sorted_error_dict)

with open('user_statistics.csv', 'w', newline='') as user_csv:
    csv_writer = csv.writer(user_csv)
    csv_writer.writerows(sorted_user_list)
