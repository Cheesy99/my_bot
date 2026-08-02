import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch.actions import TimerAction

def generate_launch_description():

    package_name = 'my_bot'

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
        )]), launch_arguments={'use_sim_time' : 'true'}.items()
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py",
            )
        ),
        launch_arguments={
            "gz_args": "-r empty.sdf"
        }.items(),
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'my_bot',
            '-x', '0',
            '-y', '0',
            '-z', '0.2'
        ],
        output='screen'
    )

    bridge = Node(
    package="ros_gz_bridge",
    executable="parameter_bridge",
    arguments=[
        "/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist",
        "/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry",
        "/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock",
        "/world/empty/model/my_bot/joint_state@sensor_msgs/msg/JointState@gz.msgs.Model",
        "/model/my_bot/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V",
    ],
    remappings=[
        ("/model/my_bot/tf", "/tf"),
    ],
    output="screen",
)
    


    return LaunchDescription([
        rsp,
        gazebo,
        spawn_robot,
        bridge
    ])