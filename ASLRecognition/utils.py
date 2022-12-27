import random
import math
import tensorflow as tf
import numpy as np
import os
import cv2
from sklearn.model_selection import train_test_split

train_directory = "datasets/asl_alphabet_train"
dev_directory = "datasets/asl_alphabet_dev"
def load_data():
	images, labels = load_image(load_directory = dev_directory)
	X_train, X_test, Y_train, Y_test = train_test_split(images, labels, test_size = 0.3)
	Y_train = Y_train.reshape((1, Y_train.shape[0]))
	Y_test = Y_test.reshape((1, Y_test.shape[0]))

	return X_train, X_test, Y_train, Y_test

def load_image(load_directory):
	images=[]
	labels=[]
	size=64,64
	print()
	print("Loading... " + load_directory + ": ",end = "")
	for folder_index, folder in enumerate(os.listdir(load_directory)):
		print(folder,end='|')
		for image in os.listdir(load_directory + "/" + folder):
			temp_img = cv2.imread(load_directory + '/' + folder +'/' + image)
			temp_img = cv2.resize(temp_img,size)
			images.append(temp_img)
			labels.append(folder_index)
	# Normalize image vectors
	images = np.array(images)/255.0
	images = images.astype('float32')
	labels = np.array(labels)
	return images, labels


def convert_to_one_hot(Y, C):
	Y = np.eye(C)[Y.reshape(-1)].T
	return Y
	
def random_mini_batches(X, Y, mini_batch_size = 64, seed = 0):
	m = X.shape[1]                  # number of training examples
	mini_batches = []
	np.random.seed(seed)
    
	# Step 1: Shuffle (X, Y)
	permutation = list(np.random.permutation(m))
	shuffled_X = X[:, permutation]
	shuffled_Y = Y[:, permutation].reshape((Y.shape[0],m))

	# Step 2: Partition (shuffled_X, shuffled_Y). Minus the end case.
	num_complete_minibatches = math.floor(m/mini_batch_size) # number of mini batches of size mini_batch_size in your partitionning
	for k in range(0, num_complete_minibatches):
		mini_batch_X = shuffled_X[:, k * mini_batch_size : k * mini_batch_size + mini_batch_size]
		mini_batch_Y = shuffled_Y[:, k * mini_batch_size : k * mini_batch_size + mini_batch_size]
		mini_batch = (mini_batch_X, mini_batch_Y)
		mini_batches.append(mini_batch)
    
    # Handling the end case (last mini-batch < mini_batch_size)
	if m % mini_batch_size != 0:
		mini_batch_X = shuffled_X[:, num_complete_minibatches * mini_batch_size : m]
		mini_batch_Y = shuffled_Y[:, num_complete_minibatches * mini_batch_size : m]
		mini_batch = (mini_batch_X, mini_batch_Y)
		mini_batches.append(mini_batch)
    
	return mini_batches