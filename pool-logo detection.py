import cv2
import numpy as np

# Define the path to the video file
video_path = 'center.mp4'

# Define the parameters for circle detection
circle_params = dict(
    dp=1,         # Inverse ratio of the accumulator resolution to the image resolution
    minDist=50,   # Minimum distance between the centers of the detected circles
    param1=50,    # Upper threshold for edge detection
    param2=30,    # Threshold for center detection
    minRadius=100,  # Minimum radius of the detected circles
    maxRadius=600   # Maximum radius of the detected circles
)

# Create a VideoCapture object to read the video file
cap = cv2.VideoCapture(video_path)

sift = cv2.SIFT_create()

firstframe = 0

out = cv2.VideoWriter('ball.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, (300,300))

lastx = 0

# Loop over the frames of the video
while cap.isOpened():
    # Read a frame from the video capture device
    ret, frame = cap.read()

    # If the frame was not read successfully, break the loop
    if not ret:
        break

    # Convert the frame to grayscale
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect circles in the frame
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, **circle_params)

    cropped = frame[300:600, 300:600]
    
# ensure at least some circles were found   
    if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
	# loop over the (x, y) coordinates and radius of the circles
        maxr = 0 
        for (x, y, r) in circles:
            if r > maxr:
                maxr = r
                cropped = frame[y-r:y+r, x-r:x+r]
                kp = sift.detect(cropped, None)
                cropped = cv2.drawKeypoints(cropped,kp, cropped, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                deltax = x - lastx 
                lastx = x
                pixres = r / 2.25
                deltax = deltax * pixres
                print(deltax)
                
    # Display the frame

    resized = cv2.resize(cropped, (300, 300), interpolation = cv2.INTER_AREA)

    cv2.imshow('frame', resized)
    out.write(resized)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close all windows
cap.release()
out.release()
cv2.destroyAllWindows()
