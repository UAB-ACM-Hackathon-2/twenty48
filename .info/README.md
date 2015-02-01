# Twenty48

A clone of the game 2048 playable on the desktop or phone. The game is written in Python 2.7 using the Kivy library.

## How to Play

The game is very straightforward. The goal is to create a tile that has the value 2048. To achieve this goal, swipe 
across the screen using the mouse, a finger, or the arrow keys which will result in all the tiles moving in that direction.
If two tiles of the same value are pushed into each other, they will merge and result in a new tile with a value of 
two times the original tiles value. 

The score for the game is calculated based on the value of the tiles merged, so merging two tiles marked `4` will earn
four points. The goal of the game is not to earn points though, it is to get a tile marked `2048`.

### Android (Highly Recommended)

Download the `.apk` file from the `bin` folder onto your phone (downloading to the computer and attaching to an
email can help with this). Click on the downloaded file and install it onto your phone. If the app cannot be installed,
check the phone settings an ensure that you have permission to install from unknown sources (usually under developer 
options).

Once installed, just click the application icon to begin.

### Desktop

The game requires the following libraries to play on the desktop:

* Python 2.7
* [http://kivy.org/#home](Kivy 1.9)
* Pygame
* Python-Pillow

Run the app by moving into the folder and using the command `python2.7 main.py`

It is a little difficult to set up the desktop environment, so we recommend using the mobile phone.