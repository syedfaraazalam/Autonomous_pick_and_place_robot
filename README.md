# Autonomous ball pick and place robot using openCV, Kivy(android) and Arduino

The aim of this project is to make a pick and place robot using opencv and python and deploy it on android phone using kivy and buildozer.

We have used the usbserial4a library from [https://github.com/jacklinquan/usbserial4a] to commuincate through usb port of our android phone and send data to arduino to control robot motion. It is suggested to visit that repository and go throught it's readme before continuing.

## How to use it

1) Install kivy and buildozer following the instrutions from [https://kivy.org/doc/stable/gettingstarted/installation.html] and [https://kivy.org/doc/stable/guide/packaging-android.html#buildozer].
2) Clone this repository into your system. Open the folder where you have cloned the repository, run a terminal and type buildozer android debug. If there are any errors, make sure the 'buildozer.spec' file is same as in this repository. Also make sure the changes suggested by [https://github.com/jacklinquan/usbserial4a] have been done.
3) Clone the repository from [https://github.com/Android-for-Python/c4k_opencv_example] into the same folder(for edge detection).
4) If there are no errors, you can go ahead and run buildozer android debug deploy run in the terminal, make sure you have enabled usb debugging in your android phone through developer options. If there are no errors, the app will be launhed as soon as it's deployed.

## How does it works

On opening the app, the camera tries to detect a ball of neon colour. If it doesn't detect the ball, it'll start rotating right to find one. As soon as the ball is detected, it starts moving towards it. If the ball is in right side of screen, the robot takes soft right(using only 1 wheel) and as soon as the ball is in centre, it starts moving forward. Once the robot is near enough to the ball, the program send a signal to arduino which rotates the servo and the arms picks the ball.
Once the ball is picked, the robot tries to find the drop location(pink color)(similar to ball detection). Once the drop location is detected, the robot moves towards it and stops at a certain distance, drops the ball and move backwards for 2 second.

The robot motion code is in the arduino folder. The connections to servo are similar to that done in [https://docs.arduino.cc/static/323f79da8e7a89e7d2ff9805c5976b25/29114/servo-knob-circuit.png] whereas the servo is controlled using microseconds command, more details here [https://www.arduino.cc/reference/en/libraries/servo/writemicroseconds/].

The ball colour and drop location colour can be changed inside the main_logic.py file. If you're not sure about what colour values to use, you can follow these steps to determine -

* Once you run the app, there will be two icons on the bottom, press the right icon.
* You'll see a red box on top left corner, place the object on a surface and place the camera in such a way that the square box is fully covered with the object. The box will give you the average value of colour in RGB format.
* Try to put the object in different lighting conditions and take screenshot. Convert these values to HSV and put them in main_logic.py file.
* The camera will detect the object between two colour limit, hence it is suggested that you take the readings in both low light and proper light conditions so the camera can detect the object without any issue.
* If there are any errors regarding cameraX kindly check that you have cloned the following repository correctly : [https://github.com/Android-for-Python/c4k_opencv_example]
