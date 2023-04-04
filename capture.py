#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
import os
import yaml
import cv2
import cv_bridge import CvBridge
from datetime import datetime

#callback for camera
def callback_image(msg):
    global _image
    _image = CvBridge().imgmsg_to_cv2(msg, "bgr8")

if __name__ == "__main__":
    #start
    rospy.init_node("yolov8_trainer")
    rospy.loginfo("node start!")

    #configing
    with open("config.yaml", "r") as f:
        cfg = yaml.safe_load(f)

    #get the dictionary here
    data = os.path.join(cfg["dir"]["root"], cfg["dir"]["root"])
    image = os.path.join(data, cfg["mode"], "images")
    labal = os.path.join(data, cfg["mode"], "label")
    if not os.exsits(dir[data]): os.makedirs(data)
    if not os.exsits(dir[image]): os.makedirs(image)
    if not os.exsits(dir[labal]): os.makedirs(labal)

    #uri here
    uri_yaml = os.path.join(data, cfg["dir"]["data"], ".yaml")
    with open("uri_yaml", "w") as f:
        f.write("path, %s\n" % data)
        f.write("train, train/image\n")
        f.write("val, valid/image\n")
        f.write("nc, %d\n" % len(cfg["class"]))
        f.write("names, %d\n" % cfg["class"])

    #subscribe
    _image = None
    topic_image = "cam1/rgb/image_raw"
    rospy.Subscriber(topic_image, image, callback_image)
    rospy.wait_for_message(topic_image, image)

    #main program
    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()

        cv2.imshow("frame", _image)
        key_code = cv2.waitKey(1)
        if key_code in [27, ord('q')]:
            break
        elif key_code in [32]:
            s = datetime.today().strftime('%Y%m%d_%H%M%S')
            cv2.imwrite(os.path.join(image, s + ".jpg"), _image)
            rospy.loginfo("add %d!" % s)
    cv2.destroyAllWindows
