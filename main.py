import numpy as np
import cv2
import  imutils
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def func(cap, image, idx, count) :	
	#cv2.imwrite("frame%d.jpg" % count, image)
		
	# Resize the image - change width to 1500
	image = imutils.resize(image, width=1500)

	# Display the original image
	#cv2.imshow("Original Image", image)
	#cv2.waitKey(100)


	# RGB to Gray scale conversion
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#cv2.imshow("1 - Grayscale Conversion", gray)
	#cv2.waitKey(100)



	# Noise removal with iterative bilateral filter(removes noise while preserving edges)
	gray = cv2.bilateralFilter(gray, 11, 17, 17)
	#cv2.imshow("2 - Bilateral Filter", gray)
	#cv2.waitKey(100)

	
	# Find Edges of the grayscale image
	edged = cv2.Canny(gray, 170, 200)
	#cv2.imshow("3 - Canny Edges", edged)
	#cv2.waitKey(100)


	# Find contours based on Edges
	cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30] #sort contours based on their area keeping minimum required area as '30' (anything smaller than this will not be considered)
	NumberPlateCnt = None #we currently have no Number plate contour
	flag = 0

		# loop over our contours to find the best possible approximate contour of number plate
		
	for c in cnts:
	        peri = cv2.arcLength(c, True)
	        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	        if len(approx) == 4:  # Select the contour with 4 corners
	            NumberPlateCnt = approx #This is our approx Number Plate Contour
	            x, y, w, h = cv2.boundingRect(c)
	            new_img = image[y : y+h, x : x+w]
	            cv2.imwrite(str(idx) + '.jpg', new_img)
	            flag = 1

	            break



	# print(([NumberPlateCnt]))
	if flag==1 :

		# Drawing the selected contour on the original image
		cv2.drawContours(image, [NumberPlateCnt], -1, (0,255,0), 3)
		cv2.imshow("Final Image With Number Plate Detected", image)
		cv2.waitKey(10)
		

		cropped_img_loc = str(idx)+'.jpg'
		xyz = cv2.imread(cropped_img_loc)

		
		#cv2.imshow("Cropped image", xyz)
		#cv2.waitKey(10)

		xyz = imutils.resize(xyz, width=1500)

		#cropped_img_loc = imutils.resize(cropped_img_loc, width = 1500)


		text = pytesseract.image_to_string(xyz, lang='eng')
		print("Number is", text)
		#cv2.destroyAllWindows()
	else :
		print("image not found")
	

	#return text
		



idx = 8
count = 0
# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('http://192.168.1.101:8080/')
cap = cv2.VideoCapture('test.mp4')


#cap.set(1, 5)
#cap.set(3, 3000)
#cap.set(4, 2000)
#print("Total number of frames in this video is : ", cap.get(7))
#cap.set(1, 100)
success, image = cap.read()
#total_frames = int(cap.get(7))
#cap.set(1, 2000)
temp = 0
count = 0
while success :
	for j in range(1, 31):
		pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
		func(cap, image, idx, count)
		success, image = cap.read()
		count += 1
		idx+=1
		temp += 2
	cap.set(1, temp)


print("count : ", count)

