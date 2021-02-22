#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import csv

import rospy
from sensor_msgs.msg import LaserScan

count = 0


def laser_listener(data, csv_writer):
    """
    :type data: LaserScan
    """
    global count
    range = data.ranges[0]
    if math.isinf(range):
        range = 0
    if data.angle_min > data.angle_increment:
        return
    row = [str(data.angle_min), str(range)]
    csv_writer.writerow(row)
    rospy.loginfo(row)

    count += 1
    if count >= 2000:
        rospy.signal_shutdown("finish")


def usage():
    print("missing args, usage:")
    print("rosrun laser_record laser_record_zero _dir:=<dir> _range:=<range>")


def main(argv):

    rospy.init_node("laser_recorder", anonymous=True)
    dir = rospy.get_param("~dir", "")
    if dir == "":
        usage()
        return
    range = rospy.get_param("~range", "")
    if range == 0:
        usage()
        return
    topic = rospy.get_param("~topic", "")
    if topic == 0:
        usage()
        return
    csv_file_path = dir + "/" + "%05d" %(range) + ".csv"
    rospy.loginfo(csv_file_path)
    csv_file = open(csv_file_path, "wb")
    csv_writer = csv.writer(csv_file)
    rospy.Subscriber(topic, LaserScan, laser_listener, csv_writer, queue_size=10)
    rospy.loginfo("laser_recorder start")
    rospy.spin()
    csv_file.close()


if __name__ == "__main__":
    main(sys.argv)
