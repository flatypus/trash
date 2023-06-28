# Trash

This project is Trash. 

## Okay, so why did you make it?
Think about that time you were sitting in your bed, watching YouTube, eating snacks. You finish your bag of chips, or that candy bar, and you're left with some garbage. In the spirit of being clean and tidy, you want to throw that trash in the trash can. 

But wait! It's across the room! Now, what do you do? Your eyes squint, you turn around, and chuck that piece of trash towards the trash can...and yet despite your efforts, the trash bounces off the wall and on the floor.

You sigh. You get up from your bed, walk over, and place the trash in the trash can. You get back in bed, and keep watching YouTube. All this time, you think back to that moment that you missed.

There had to be a better way.

## The better way.
We were you at some point in time. We realized the five seconds it took for you to get up, put the trash in the can, and get back in bed is time you will never get back. So, to all of you who have shared this emotional experience, we have built Trash.
![image](https://github.com/flatypus/trash/assets/68029599/ba4c2bce-e5ff-4235-a1ec-37697dbbad4d)

It consists of a setup of two cameras positioned towards the center of your room, where your trash can is. These cameras send the data stream over to the garbage tracking algorithm, which detects the garbage in each camera using a custom trained YOLOV8 model with over 14,000 hand-labeled images. Our algorithm then takes the combined positions of the trash in both camera streams, does some trigonometry, and calculates the expected position of the trash in real life. It then can determine the final position of the trash when it hits the floor, and sends the position to our Trash robot via Serial. We also wrote a plotting script to visualize the data in real time.

Model: https://universe.roboflow.com/flatypus/trash-7kbr4
![image](https://github.com/flatypus/trash/assets/68029599/2a8c83b2-8a8b-4aac-82f0-d0a88cc5092a)

Our trash robot consists of a PETG 3D printed frame and four mecanum wheels powered by Nema 17 stepper motors. We selected mecanum wheels for their ability to move omnidirectionally which enables the robot to move in the most efficient, straight line path to the trash regardless of its location. The steppers are driven by TB6560 drivers which can handle 3A of current at 35V. The robot is powered by a 3S, 2200mAh LiPo battery which can output 77A of current. The robot is controlled by a Teensy 4.0 microcontroller which was chosen over Arduino boards for its high clock speed (600 mHz vs. 16 mHz). This allows the steppers to run at the extremely high speeds required for the robot to move fast enough to catch the trash. 

We used the AccelStepper Arduino library to control the stepper motors. Our code takes the desired location coordinates, subtracts the current location coordinates, and does some vector math to determine the precise number of steps required for each wheel to spin to reach the desired location. As the robot continuously receives new, more accurate coordinates from the tracking system through serial communication, it uses the current number of steps each motor has taken to determine the current coordinates of the robot. These are saved as the current coordinates and the above process repeats, recalculating the number of steps for each motor to reach the new desired location. 

## Notes about the repo
 - `target_0` and `target_1` are continuously updated files containing the locations of trash in the two cameras. The cameras are positioned 245 cm from each other, facing 45 degrees towards the center of the room. We used files vs socket communication or an api for its simplicity.
 - `track_ball.py` contains the code to start a camera stream, detect the trash, and save the coordinates to the target files. Two instances of this script are run, one for each camera.
 - Simultaneously, `continue_plot.py` is run to plot the data in real time. This is done using matplotlib and the target files. It also handles the calculation of the expected position of the trash in real life. After it predicts the location, it saves the coordinates in another file, prediction.
 - `yolov8_model` is the currently used model; 47 epochs on 14256 images.
 - `yolov8_model_v2` is the same dataset trained for 300 epochs, however the 47 epoch model seems to work better.

# Running the code
- Install the requirements in `requirements.txt`
- Run `pnpm install` to install concurrently, a package that allows you to run multiple scripts at once.
- Install `nodemon` globally with `pnpm i -g nodemon`, to watch scripts for changes and restart them automatically.
- You need two cameras to run this. We used the webcam of the laptop, and a second webcam. Once you have both connected, you can run pnpm dev to start nodemon instances for two cameras and the plotter.
- If you just want to run the system, you can run pnpm start.

