from animate_max7219 import Screen, Animate

#init the max7219 8x8 screen
screen = Screen()

#init the Animate class and a pass the screen to it
loop = Animate(screen, fps=8)

#a list of .bmp file names that will be each frame in the animation 
frames = []
frames.append('sprite/bat/bat-0001.bmp')
frames.append('sprite/bat/bat-0002.bmp')
frames.append('sprite/bat/bat-0003.bmp')
frames.append('sprite/bat/bat-0004.bmp')
frames.append('sprite/bat/bat-0005.bmp')
frames.append('sprite/bat/bat-0006.bmp')
frames.append('sprite/bat/bat-0007.bmp')

#add frames to Animate class
loop.add_frames(frames)

#run the animation
loop.run()
