# ! /usr/bin/env python
# -*- coding:utf-8 -*-
import csv, time

legal_image = ("jpg", "jpeg", "png")
def get_imname_urlstr(url_str):
	last_item = url_str.split("/")[-1]
	if last_item.endswith(legal_image):
		return last_item
	else:
		print("No image")

def rm_backslash(str_list):
	new_s_list = []
	for item in str_list:
		item.replace("\\", "")
		new_s_list.append(item)
	return new_s_list

####################################
########### Pass Test
def rm_redundant(csv_file, gen_csv):
	csv_set = set()

	with open(csv_file, newline="") as file:
		csv_lines = csv.reader(file)
		for row in csv_lines:
			csv_set.add(row[0])

	new_csv = []
	for i in csv_set:
		i = i.replace("\\","")
		new_csv.append(i)

	with open(gen_csv, "a+", newline="") as new:
		csv_writer = csv.writer(new, dialect="excel")
		for row in new_csv:
			csv_writer.writerow([row])

# add source url_strings to target line in csv file
def combine_csv(source, target, result):

	source_list = []
	with open(source, newline="") as source_csv:
		source_csv_lines = csv.reader(source_csv)
		for row in source_csv_lines:
			row[0] = row[0].replace("\\", "")
			# print(row)
			source_list.append(row)

	target_list = []
	with open(target, newline="") as target_csv:
		target_csv_lines = csv.reader(target_csv)
		for row in target_csv_lines:
			# print(row)
			target_list.append(row)

	b_time = time.time()
	new_csv_items = []
	for t_item in target_list:
		for s_url_item in source_list:
			if s_url_item[0].find(t_item[0]) >= 0:
				# print(s_url_item[0], t_item[0])
				t_item.insert(0, s_url_item[0])
				# print(t_item)
				new_csv_items.append(t_item)
	e_time = time.time()
	print("Matching takes {:.4f} seconds".format(e_time-b_time))

	with open(result, "a+", newline="") as new:
		csv_writer = csv.writer(new, dialect="excel")
		for row in new_csv_items:
			csv_writer.writerow(row)
		print("Write to {}".format(result))

if __name__ == "__main__":
	# rm_redundant("source.csv", "new_source.csv")
	combine_csv("source.csv", "target.csv", "last_one.csv")
