import glob
import os
from PIL import Image
import numpy as np

width = 100     # Width of all images
height = 100    # Height of all images

# Get all images and labels from base path subdivided by class
def get_images_and_labels(base_path):
    X = []      # A list for store the images
    Y = []      # A list for store the labels

    for class_path in glob.glob(base_path + "/*"):    # Get all class paths from base path
        label = os.path.basename(class_path)          # Get label from class path
        for img_path in glob.glob(class_path + "/*"): # Get all image paths from class path
            grey_image = Image.open(img_path).convert("L")      # Convert RGB image to grey_scale image
            img = np.array(grey_image.resize((width, height)))  # Resize the grey image and convert it to numpy array
            img = img / 255                                     # Normalize the image array
            X.append(img)                                       # Append image array to X
            Y.append(label)                                     # Append label to Y

    X = np.array(X)                                         # Convert list X to numpy array
    X = X.reshape(X.shape[0], width, height, 1)             # Reshape the X

    # return to_categorical(Y), Y
    from keras.utils import to_categorical
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(Y)
    return X, integer_encoded


    return X, Y

# Get base path
base_path = "images"

# Get images and labels
X, Y = get_images_and_labels(base_path)
print(X.shape)


# Dict label_encoder classes
label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(Y)
print(integer_encoded)

# Convert labels to onehot labels
from keras.utils import to_categorical
onehot_labels = to_categorical(integer_encoded)
print(onehot_labels)

# Split dataset to train and test

   