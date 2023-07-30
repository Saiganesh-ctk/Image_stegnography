# Import the necessary libraries
from PIL import Image
from numpy import asarray

text = input("Enter the original image name(with extension) : ")
img = Image.open(text)
numpydata = asarray(img)
print(numpydata)
