#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import csv

import rospy
from sensor_msgs.msg import LaserScan


def laser_listener(data, csv_writer):
    index = 0
    angle = data.angle_min
    for range in data.ranges:
        if math.isinf(range):
            range = 0

        row = [str(index), str(angle), str(range), str(data.intensities[index])]
        csv_writer.writerow(row)
        rospy.loginfo(row)

        angle = angle + data.angle_increment
        index = index + 1
    #rospy.signal_shutdown()


def usage():
    print("missing args, usage:")
    print("    rosrun laser_record laser_record_zero _dir=<dir> _range=<range> _topic=</scanx>")


def main(argv):
    rospy.init_node("laser_recorder", anonymous=True)
    dir = rospy.get_param("~dir", "")
    if dir == "":
	print("1")
        usage()
        return
    topic = rospy.get_param("~topic", "")
    if topic == "":
	print("2")
        usage()
        return
    csv_file_path = dir + "/" + "laser_recorder" + ".csv"
    #rospy.loginfo(csv_file_path)
    csv_file = open(csv_file_path, "wb")
    csv_writer = csv.writer(csv_file)
    rospy.Subscriber(topic, LaserScan, laser_listener, csv_writer, queue_size=10)
    #rospy.loginfo("laser_recorder start")
    rospy.spin()
    csv_file.close()


if __name__ == "__main__":
    main(sys.argv)
