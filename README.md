# Trash

This project is Trash. 

## Okay, so why did you make it?
Think about that time you were sitting in your bed, watching YouTube, eating snacks. You finish your bag of chips, or that candy bar, and you're left with some garbage. In the spirit of being clean and tidy, you want to throw that trash in the trash can. 

But wait! It's across the room! Now, what do you do? Your eyes squint, you turn around, and chuck that piece of trash towards the trash can...and yet despite your efforts, the trash bounces off the wall and on the floor.

You sigh. You get up from your bed, walk over, and place the trash in the trash can. You get back in bed, and keep watching YouTube. All this time, you think back to that moment that you missed.

There had to be a better way.

## The better way.
We were you at some point in time. We realized the five seconds it took for you to get up, put the trash in the can, and get back in bed is time you will never get back. So, to all of you who have shared this emotional experience, we have built Trash.

It consists of a setup of two cameras positioned towards the center of your room, where your trash can is. These cameras send the data stream over to the garbage tracking algorithm, which detects the garbage in each camera using a custom trained YOLOV8 model with over 2000 hand-labeled images. 

Our algorithm then takes the combined positions of the trash in both camera streams and calculates the expected position of the trash in real life. It then can determine the final position of the trash when it hits the floor, and sends the position to our Trash robot.
