#!/localdisk/python3-venv/bin/python
import cv2
import matplotlib.pyplot as plt
import numpy as np

def canny(image):
	gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
	blur = cv2.GaussianBlur(gray, (5,5), 0)
	canny = cv2.Canny(blur, 50, 150)
	return canny

def display_line(image, lines):
	line_image = np.zeros_like(image)
	if lines is not None:
		for line in lines:
			line = np.round(line,0)
			x1, y1, x2, y2 = line.reshape(4)
			cv2.line(line_image, (int(x1),int(y1)), (int(x2),int(y2)), (255, 255, 255), 10)
	return line_image

def average_slope_intercept(image, lines):
	left_border = []
	right_border = []
	top_border = []
	bottom_border = []
	obstacles = []

	for line in lines:
		x1, y1, x2, y2 = line.reshape(4)
		if y1 <= 20:
			top_border.append(line)
		elif y1 >= 500:
			bottom_border.append(line)
		elif x1 <= 20:
			left_border.append(line)
		elif x1 >= 900:
			right_border.append(line)
		else:
			obstacles.append(line)

	left_border_average = np.average(left_border, axis=0)
	left_border_average[0][1] = 0
	left_border_average[0][3] = image.shape[0]

	right_border_average = np.average(right_border, axis=0)
	right_border_average[0][1] = 0
	right_border_average[0][3] = image.shape[0]

	top_border_average = np.average(top_border, axis=0)
	top_border_average[0][0] = 0
	top_border_average[0][2] = image.shape[1]

	bottom_border_average = np.average(bottom_border, axis=0)
	bottom_border_average[0][0] = 0
	bottom_border_average[0][2] = image.shape[1]	

	left_line = make_coordinates(image, left_border_average)
	right_line = make_coordinates(image, right_border_average)
	top_line = make_coordinates(image, top_border_average)
	bottom_line = make_coordinates(image, bottom_border_average)

	obstacle_lines = np.array([])
	for line in obstacles:
		obstacle_lines = np.append(obstacle_lines, make_coordinates(image, line), axis=0)

	obstacle_lines = obstacle_lines.reshape((int(obstacle_lines.shape[0]/4),4))
	cleaned_lines = np.array([left_line, right_line, top_line, bottom_line])
	cleaned_lines= np.append(cleaned_lines, obstacle_lines, axis=0)
	print(cleaned_lines)
	print(obstacle_lines)
	return cleaned_lines

def make_coordinates(image, line):
	x1, y1, x2, y2 = line.reshape(4)
	return np.array([x1, y1, x2, y2])

image = cv2.imread("images/input_image_filled.jpg")    
image = cv2.resize(image, (960, 540))
lane_image = np.copy(image)
canny = canny(lane_image)

#extract red channel
red_channel = image[:,:,2]

#Houghline to show only borders
lines = cv2.HoughLinesP(canny, 2, np.pi/180, 100, np.array([]), minLineLength=50, maxLineGap=5)
averaged_lines = average_slope_intercept(lane_image,lines)

#line_image = display_line(lane_image, averaged_lines)
line_image = display_line(lane_image, lines)

#show image using opencv
#cv2.imshow('original', image)
#cv2.imshow('canny', canny)
#cv2.imshow('result',line_image)
#cv2.waitKey(0)

#show image using matplotlib
#plt.imshow(line_image)
plt.imshow(red_channel)
plt.show()

#save image
#cv2.imwrite('maps/sample_map.png',line_image)