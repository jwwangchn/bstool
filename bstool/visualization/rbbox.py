import numpy as np
import cv2
import math


def draw_rectangle_by_points(im, point, color=(0, 0, 255)):
    """
    docstring here
        :param points: [x,y,...] (1*8) 
    """
    for idx in range(-1, 3, 1):
        cv2.line(im, (int(point[idx*2]), int(point[idx*2+1])), (int(point[(idx+1)*2]), int(point[(idx+1)*2+1])), color, 3)

    return im

def show_bbox(im, bbox, color=(0, 0, 255)):
    """show bounding box

    Args:
        im (np.array): input image
        bbox (list): (xmin, ymin, h, w)
        color (tuple, optional): color of box. Defaults to (0, 0, 255).

    Returns:
        np.array: output image
    """
    cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])), color, 2)

    return im

def show_pointobb(im, pointobb, color=(0, 0, 255)):
    """show pointobb

    Args:
        im (np.array): input image
        pointobb (list): (x1, y1, x2, y2, x3, y3, x4, y4)
        color (tuple, optional): color of box. Defaults to (0, 0, 255).

    Returns:
        np.array: output image
    """
    im = draw_rectangle_by_points(im, pointobb, color=color)
    return im

def show_thetaobb(im, thetaobb, color=(0, 0, 255)):
    """show thetaobb

    Args:
        im (np.array): input image
        thetaobb (list): (cx, cy, w, h, theta)
        color (tuple, optional): color of box. Defaults to (0, 0, 255).

    Returns:
        np.array: output image
    """
    cx, cy, w, h, theta = thetaobb

    rect = ((cx, cy), (w, h), theta / np.pi * 180.0)
    rect = cv2.boxPoints(rect)
    rect = np.int0(rect)
    cv2.drawContours(im, [rect], -1, color, 3)

    return im

def show_hobb(im, hobb, color=(0, 0, 255)):
    """show hobb

    Args:
        im (np.array): input image
        hobb (list): (x1, y1, x2, y2, h)
        color (tuple, optional): color of box. Defaults to (0, 0, 255).

    Returns:
        np.array: output image
    """
    first_point_x = hobb[0]
    first_point_y = hobb[1]
    second_point_x = hobb[2]
    second_point_y = hobb[3]
    h = hobb[4]

    angle_first_second = np.pi / 2.0 - np.arctan2(second_point_y - first_point_y, second_point_x - first_point_x)
    delta_x = h * np.cos(angle_first_second)
    delta_y = h * np.sin(angle_first_second)

    forth_point_x = first_point_x - delta_x
    forth_point_y = first_point_y + delta_y

    third_point_x = second_point_x - delta_x
    third_point_y = second_point_y + delta_y

    pointobb = [first_point_x, first_point_y, second_point_x, second_point_y, third_point_x, third_point_y, forth_point_x, forth_point_y]

    im = draw_rectangle_by_points(im, pointobb, color=color)

    return im