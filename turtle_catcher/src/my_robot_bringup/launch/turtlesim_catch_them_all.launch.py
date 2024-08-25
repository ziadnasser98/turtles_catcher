from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    ld = LaunchDescription()


    ss = DeclareLaunchArgument(
            'spawn_frequency',
            default_value= "2.0",
            description='The spawning frequency of the target turtles'
        )
    ld.add_action(ss)

    turtlesim_node = Node(
        package= 'turtlesim',
        executable= 'turtlesim_node',
        name = "catcher"
    )

    spawn_turtle_node = Node(
        package= "turtles_catcher",
        executable="spawn_turtle",
        parameters=[{'spawn_frequency':LaunchConfiguration('spawn_frequency')}]
    )

    control_node = Node(
        package= "turtles_catcher",
        executable="control_turtle"
    )

    ld.add_action(turtlesim_node)
    ld.add_action(spawn_turtle_node)
    ld.add_action(control_node)

    return ld
