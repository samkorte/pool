# pool
Various OpenCV Python scripts for pool/billiards analysis.

pool-pose.py:  script using OpenCV and Mediapipe to calcluate pose metrics during pool stroke.  Estimates elbow angle, elbow drop, max elbow drop, head drop, and max head drop.  To do:  detect when the cue ball moves to store metrics at moment of impact.

![image](https://user-images.githubusercontent.com/62845571/232592539-92e520c7-586a-4d1d-aaa2-ed287ced1d0e.png)

pool-logo detection.py:  simple script using OpenCV and Hough Circles to detect and crop cue ball location in a video feed.  Uses keypoints to identify logos and other features within the cropped cue ball image.  Todo:  calculate spin and speed metrics.

![GIF](https://user-images.githubusercontent.com/62845571/232593153-bca554d9-f3bc-4c73-997f-acaea8fd9cc4.gif)
