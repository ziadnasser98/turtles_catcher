# Turtles_catcher
## Overview
A simple project In ROS2 based on the turtlesim package. The project was made for educational and training purposes without a useful end goal. The project demonstrates a main turtle and target turtles. The main turtle will chase the target turtles one by one according to the closest when the main turtle reaches a target turtle, The target turtle disappears.

In the beginning, only the main turtle exists. Then the target turtles get spawned into the GUI at a frequency determined by the user (there is a default value in case the user doesn't specify a spawning frequency).

## Project structure 
- turtlesim_node: A ROS2 node from the standard turtlesim package that provides a graphical interface with a turtle that can be controlled within a window.
- spawn_turtle: A custom ROS2 node that spawns additional turtles at random locations on the screen according to a user-defined frequency.
- control_turtle: A custom ROS2 node that controls the main turtle, making it follow and "catch" the spawned turtles.

## Installation instructions
1. Create a workspace and inside the workspace directory Clone this repository.
   ```
   mkdir ~/turtlesim_ws
   cd ~/turtlesim_ws
   git clone https://github.com/ziadnasser98/turtles_catcher.git
   ```
3. Build the workspace using Colcon build in your main directory.
   ```
   cd ~/turtlesim_ws
   colcon build 
   ```
5. Source the workspace installation file.
   ```
   source install/setup.bash
   ```
## Running the Project
To ensure convenient usage of the project, we created a launch file responsible of launching all the executables of the project at once with single line:
```
ros2 launch my_robot_bringup turtlesim_catch_them_all.launch.py spawn_frequency:=3.0
```
You can determine the spawning frequency using the launch argument 'spawn_frequency' or you can launch the launch file without the spawn_frequency argument. In this case, the spawn_frequency will be set to 2.0 by default.
