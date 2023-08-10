#get the hostname

import os
import yaml

hostnames = []

filedir = "/home/f5-backup/files"
for subdir, dirs, files in os.walk(filedir):
	for file in files:
		hostname = (('{f}.networking.cardinalhealth.net').format(f=file))
		print (hostname)
		hostnames.append(hostname)



# Read the existing inventory file
with open('inventory.yaml', 'r') as yaml_file:
	existing_content = yaml_file.readlines()

# Find the line index where [f5-group] is located
group_line_index = None
for i, line in enumerate(existing_content):
	if line.strip() == '[f5-group]':
		group_line_index = i
		break

# Collect existing hostnames under [f5-group]
existing_hostnames = set()
if group_line_index is not None:
	for line in existing_content[group_line_index + 1:]:
		stripped_line = line.strip()
		if stripped_line and not stripped_line.startswith('['):
			existing_hostnames.add(stripped_line)

# Filter out duplicate hostnames
unique_hostnames = [hostname for hostname in hostnames if hostname not in existing_hostnames]

# Insert the hostnames under the [f5-group] section maintaining the alignment
if group_line_index is not None:
	updated_content = (
		existing_content[:group_line_index + 1] +
		[f'{hostname}\n' for hostname in unique_hostnames] +
	existing_content[group_line_index + 1:]
	)

    # Write the updated content back to the inventory file
	with open('inventory.yaml', 'w') as yaml_file:
		yaml_file.writelines(updated_content)
