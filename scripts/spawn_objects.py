#!/usr/bin/env python
import rospy
import tf
import rospkg
from gazebo_msgs.srv import SpawnModel, GetModelState
from geometry_msgs.msg import *
import os
# from pathlib import Path
from tf import TransformListener
from tf.transformations import quaternion_from_euler

class spawn_objects():
	def __init__(self):
		rospy.init_node('spawn_model')

		rospack = rospkg.RosPack()
		self.Home = rospack.get_path('ssggcnn_ur5_grasping')

		self.Spawning1 = rospy.ServiceProxy("gazebo/spawn_sdf_model", SpawnModel)
		rospy.wait_for_service("gazebo/spawn_sdf_model")
		model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)

		# The spawn need some time to wait the UR5 to show in Gazebo
		object_coordinates = model_coordinates("robot", "")
		self.z_position = object_coordinates.pose.position.z
		self.y_position = object_coordinates.pose.position.y
		self.x_position = object_coordinates.pose.position.x

	def spawning(self, model_name, path, ptFinal, oriFinal):
		obj_path = self.Home + path
		
		with open(obj_path) as f:
			product_xml = f.read()

		print("Spawning model: {}".format(model_name))

		# X and Y positions are somewhat in an incorrect order in Gazebo
		item_pose = Pose(Point(x=self.y_position + ptFinal[0], y=self.x_position + ptFinal[1], z=self.z_position + ptFinal[2]),
						 Quaternion(oriFinal[0], oriFinal[1], oriFinal[2], oriFinal[3]))
		
		self.Spawning1(model_name, product_xml, "", item_pose, "world")

if __name__ == '__main__':
	spawn_obj = spawn_objects()

	object_path = '/models/mahler_obj/vase/model.sdf'
	ptFinal = [-0.1, -0.5, 0.019762]
	oriFinal = quaternion_from_euler(0.0, 0.0, 0.0)
	spawn_obj.spawning('vase', object_path, ptFinal, oriFinal)

	object_path = '/models/mahler_obj/part_1/model.sdf'
	ptFinal = [-0.1, -0.4, -0.0046]
	oriFinal = quaternion_from_euler(0.0, 0.0, 0.0)
	spawn_obj.spawning('part_1', object_path, ptFinal, oriFinal)

	object_path = '/models/mahler_obj/bar_clamp/model.sdf'
	ptFinal = [0.0, -0.4, -0.004335]
	oriFinal = quaternion_from_euler(-0.024091, 0.0, 0.0)
	spawn_obj.spawning('bar_clamp', object_path, ptFinal, oriFinal)

	object_path = '/models/mahler_obj/gear_box/model.sdf'
	ptFinal = [-0.20, -0.4, -0.005056]
	oriFinal = quaternion_from_euler(0.0, 0.0, 0.0)
	spawn_obj.spawning('gear_box', object_path, ptFinal, oriFinal)

	object_path = '/models/mahler_obj/nozzle/model.sdf'
	ptFinal = [-0.20, -0.5, 0.0]
	oriFinal = quaternion_from_euler(0.0, 0.0, 0.0)
	spawn_obj.spawning('nozzle', object_path, ptFinal, oriFinal)

	object_path = '/models/mahler_obj/part_3/model.sdf'
	ptFinal = [0.0, -0.5, 0.0]
	oriFinal = quaternion_from_euler(0.0, 0.0, 0.0)
	spawn_obj.spawning('part_3', object_path, ptFinal, oriFinal)

	# THESE OBJECTS'S MESH NEED TO BE CORRECTED
	# THEY ARE NOT DISPLAYING CORRECTLY IN GAZEBO

	# object_path = '/models/mahler_obj/pawn/model.sdf'
	# ptFinal = [0.05, -0.4, 0.0]
	# oriFinal = quaternion_from_euler(0.0, 0.0, 0.0)
	# spawn_obj.spawning('pawn', object_path, ptFinal, oriFinal)

	# object_path = '/models/mahler_obj/turbine_housing/model.sdf'
	# ptFinal = [0.05, -0.5, 0.0]
	# oriFinal = quaternion_from_euler(0.0, 0.0, 0.0)
	# spawn_obj.spawning('turbine_housing', object_path, ptFinal, oriFinal)