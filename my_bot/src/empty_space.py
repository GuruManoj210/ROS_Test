#!/usr/bin/env python

import rospy
import numpy as np
from nav_msgs.msg import OccupancyGrid
from nav_msgs.msg import MapMetaData

class empty_space_founder:

    def __init__(self):
        self.map_width = 0
        self.map_height = 0
        self.map_resolution = 0
        self.map_origin = None
        self.origin_x = 0
        self.origin_y = 0
        self.map_data = None

    # callback function for map topic subscriber
    def map(self,data):
        # print(len(data.data),"points are found in map")
        rospy.loginfo("%d points found in map",len(data.data))
        self.map_data = np.asarray(data.data)
        rospy.Subscriber("map_metadata", MapMetaData, self.meta_data)


    # callback function for the MapMetaData Subscriber
    def meta_data(self,data):
        self.map_width = int(data.width)
        self.map_height = int(data.height)
        self.map_resolution = float(data.resolution)
        self.map_origin = data.origin
        self.origin_x = self.map_origin.position.x
        self.origin_y = self.map_origin.position.y
        # print(self.map_width,self.map_height ,self.map_resolution,self.map_origin)
        self.space_finder()

    # funtion to find the 
    def space_finder(self):
        free_space=[]
        for width in range(0,self.map_width,1):
            for height in range(0,self.map_height,1):
                if (self.map_data[height*self.map_width + width]==0):
                    x = (width*self.map_resolution + self.map_resolution/2)+float(self.origin_x)
                    y = (height*self.map_resolution + self.map_resolution/2)+float(self.origin_y)
                    free_space.append((x,y))

        file1 = open(r"src/my_bot/empty_space_points/point.txt","w")
        file1.write(str(free_space))
        file1.close()
        rospy.loginfo("%d points are free in map",len(free_space))


def main():
    obj = empty_space_founder()
    rospy.init_node('empty_space', anonymous=True)
    rospy.Subscriber("map", OccupancyGrid, obj.map)
    rospy.spin()

main()