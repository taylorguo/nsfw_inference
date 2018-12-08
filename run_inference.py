# ! /usr/bin/env python
# -*- coding:utf-8 -*-
# import necessary packages
import os, time, csv
# from multiprocessing import Process,Manager, Pool
# import 3'rd party packages
from skimage import io, color

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
# import Mask RCNN packages
from mrcnn.config import Config
from mrcnn import model as modellib

###### Utility Functions ######
def get_files_name_of_folder(path):
	for root, dirs, files in os.walk(path):
		# return root     # get dir path
		# return dirs     # get sub-folders in current path
		return files

###### Constant for DCNN  ######
class_names = ['BG', 'butt', 'private', 'breast', 'animal', 'cartoon_kiss', 'cartoon_breast']
model_dirname = "models"
weights_filename = "mask_rcnn_nsfw_0494.h5"
project_path = os.path.dirname(os.path.realpath(__file__))
weights_path = os.path.join(project_path, model_dirname, weights_filename)

class nsfwConfig(Config):
	NAME = "nsfw"
	IMAGES_PER_GPU = 1
	NUM_CLASSES = 1 + 6
	STEPS_PER_EPOCH = 100
	DETECTION_MIN_CONFIDENCE = 0.8

class InferenceConfig(nsfwConfig):
	GPU_COUNT = 1
	IMAGES_PER_GPU = 1

###### Main Functions for Mask-RCNN Inference ######
def load_model_memory():
	print("\n\t ====== Loading Model ...")
	config = InferenceConfig()
	# config.display()
	###### Create Model ######
	model = modellib.MaskRCNN(mode="inference", config=config, model_dir=weights_path)
	###### Load Weights ######
	model.load_weights(weights_path, by_name=True)
	print("\t ==== Model & Weights loaded.")
	return model

def classify_process(image, model):
	print("\n\t ** Running on {}".format(image))
	batch = io.imread(image)
	if len(batch.shape) < 3:
		batch = color.gray2rgb(batch)
	if batch.shape[2] > 3:
		batch = color.rgba2rgb(batch)
	print("\t **** Image size: {}".format(batch.shape))
	r = model.detect([batch], verbose=0)[0]
	print("\t {} class(es):{}, scores {}".format(len(r["class_ids"]), r["class_ids"], r["scores"]))
	return r

def get_result(image_name, r):
	if len(r["class_ids"]) == 0:
		csv_nb = str(0)
		csv_class_name = str(0)
		csv_class_score = str(0)
		# cost_time = ret - rst
	elif len(r["class_ids"]) > 0:
		csv_nb = len(r["class_ids"])
		csv_class_name = []
		for i in r["class_ids"]:
			csv_class_name.append(class_names[i])
		csv_class_score = r["scores"]
		# cost_time = ret - rst
	result_list = [image_name, csv_nb, csv_class_name, csv_class_score]
	return result_list

def write_to_csv(*result_list):
	with open("d_result.csv", "a", newline="") as dr:
		csv_write = csv.writer(dr, dialect="excel")
		# csv_write.writerow([images[2], csv_nb, csv_class_name, csv_class_score, cost_time])
		csv_write.writerow(result_list)
		print("\t Finished Write CSV !")

def main_process():
	pass

if __name__ == "__main__":

	image_folder_name = "imtest"
	images = get_files_name_of_folder(image_folder_name)
	# # print(type(images), len(images))
	# # images_path = os.path.join(project_path, "imgnew", images[2])

	# single_image_name = "1e21be9e9fde3783ff0e58f34e4479f4.jpeg"
	# images_path = os.path.join(project_path, "imgnew", single_image_name)

	full_image_path_list = []
	for i in images:
		full_image_path_list.append(os.path.join(project_path, image_folder_name, i))

	mst = time.time()
	model = load_model_memory()
	met = time.time()
	print("\t ==== Model loaded takes {:.4f} seconds !".format(met-mst))

	# with Manager() as manager:
	# 	shared_result_list = manager.list()
	#
	# with Pool(processes=5) as pool:
	# 	print("***************",pool.map(classify_process,full_image_path_list))

	reslut_list = []
	image_nb = 1
	for one_image in full_image_path_list:
		try:
			rst = time.time()
			r = classify_process(one_image, model)
			ret = time.time()
			inference_time = ret-rst
			print("\t **** Inference takes {:.4f} seconds .".format(inference_time))

			single_image_name = one_image.split("\\")[-1]
			# print(single_image_name)
			one_result = get_result(single_image_name, r)
			one_result.append(inference_time)
			# print(one_result)
			reslut_list.append(one_result)

			csvStime = time.time()
			with open("d3_result.csv", "a", newline="") as dr:
				csv_write = csv.writer(dr, dialect="excel")
				csv_write.writerow(one_result)
			csvEtime = time.time()
			print("\t Write No.{} in CSV - {:.6f} seconds . \n".format(image_nb,(csvEtime-csvStime)))
			image_nb += 1

		except NameError:
			print("Wrong Image!")

		# single_image_name = one_image.split("\\")[-1]
		# # print(single_image_name)
		# one_result = get_result(single_image_name, r)
		# one_result.append(inference_time)
		# print(one_result)
		# reslut_list.append(one_result)

	# for item in reslut_list:
	# 	with open("dd_result.csv", "a", newline="") as dr:
	# 		csv_write = csv.writer(dr, dialect="excel")
	# 		csv_write.writerow(item)
	# 		# csv_write.writerow(result_list)
	# print("\t Finished Write {} items in CSV !".format(len(reslut_list)))




