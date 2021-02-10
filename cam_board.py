#!/usr/bin/env python3

import argparse
import configparser
import cv2
import os
import numpy

if(__name__ == "__main__"):

    # parsing command line arguments {

    parser = argparse.ArgumentParser(description = "Filter web cam image to look like a white/black board.")
    parser.add_argument("--invert" , "-i" , action = "store_true" , help = "Invert colors.")
    parser.add_argument("--denoise" , "-d" , action = "store_true" , help = "Denoise.")
    parser.add_argument("--ldenoise" , "-l" , action = "store_true" , help = "Denoise with color.")
    parser.add_argument("--fullscreen" , "-f" , action = "store_true" , help = "Full screen.")
    parser.add_argument("--warp" , "-w" , action = "store_true" , help = "Don't warp image to writable area.")
    parser.add_argument("--kernel" , "-k" , action = "store_true" , help = "Apply sharpening kernel to image.")
    parser.add_argument("--camera" , "-c" , help = "Provide integer to change the camera number, by default this value is 0.")
    parser.add_argument("--path" , "-p" , help = "Path to directory where frames will be saved. By default this is the current directory.")
    args = parser.parse_args() 

    save_dir = os.getcwd()
    if(args.path != None):
        save_dir = args.path

    # } parsing command line arguments

    # script directory {

    script_path = os.path.dirname(os.path.realpath(__file__))

    # } script directory

    # reading configuration file {

    config = configparser.ConfigParser()
    config.read(os.path.join(script_path , "aruco_cam_config"))
   
    buff = int(config["perspectiveMatrix"]["buffer"])
    
    levels = []
    for c in config["levels"]:
        levels.append(list(map(lambda x : float(x) , config["levels"][c].strip().split())))

    k_pix = int(config["fragment"]["k_pix"])

    f_buff = int(config["smooth"]["f_buff"])

    l_col = float(config["levels1"]["l_col"])

    # } reading configuration file

    # getting camera {
    if(args.camera == None):
        # by default uses the first camera
        args.camera = 0
    else:
        args.camera = int(args.camera)
    cap = cv2.VideoCapture(args.camera)
    # } getting camera 

    # window for cv {
    cv2.namedWindow('frame' , cv2.WINDOW_GUI_NORMAL)
    if(args.fullscreen):
        cv2.setWindowProperty('frame' , cv2.WND_PROP_FULLSCREEN , cv2.WINDOW_FULLSCREEN)
    # } window for cv

    # global {

    # for denoising 
    ones = None
    black = None
    white = None
    blur_kernel = numpy.ones((k_pix , k_pix) , dtype = numpy.float32) 
    blur_kernel = blur_kernel / numpy.sum(blur_kernel.flatten())

    # list of perspecive matrixes
    m_list = []

    # list of frames for smoothing
    frame_buff = []
    avg = False

    # points surrounfing the QR code available
    got_points = False

    # points surrounfing the QR code
    pointsglob = None

    # aruco markers
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_250)
    parameters =  cv2.aruco.DetectorParameters_create()

    # } global

    # main loop {

    try:
    
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
            
            if(len(corners) == 4):
                allids = [0 , 1 , 2 , 3]
                pts = [None , None , None , None]
                for i in range(4):
                    if(ids[i][0] <= 3 and ids[i][0] >= 0):
                        pts[ids[i][0]] = [
                                (int(corners[i][0][0][0]) , int(corners[i][0][0][1])) ,
                                (int(corners[i][0][1][0]) , int(corners[i][0][1][1])) ,
                                (int(corners[i][0][2][0]) , int(corners[i][0][2][1])) ,
                                (int(corners[i][0][3][0]) , int(corners[i][0][3][1]))
                                ];

                ok = not None in pts
            
                if(ok):
                    ones = numpy.ones(frame.shape[:2] , numpy.uint8)
                    black = 0 * ones
                    white = 255 * ones
                    got_points = True
                    pointsglob = pts

            warped = frame

            if(got_points and (not args.warp)):

                src = numpy.array([pointsglob[0][0] , pointsglob[1][1] , pointsglob[3][2] , pointsglob[2][3]] , numpy.float32)
                dst = numpy.array([[frame.shape[1] , frame.shape[0]] , [0.0 , frame.shape[0]] , [0.0 , 0.0] , [frame.shape[1] , 0.0]] , numpy.float32)
                m = cv2.getPerspectiveTransform(src , dst)
                m_list.append(m)
                if(len(m_list) > buff):
                    m_list.pop(0)
                m_avg = numpy.zeros(m.shape , dtype = m.dtype)
                for mm in m_list:
                    m_avg = m_avg + mm

                m_avg = m_avg / float(len(m_list))
                warped = cv2.warpPerspective(frame , m_avg , (frame.shape[1] , frame.shape[0]))


            # Our operations on the frame come here
            if((args.denoise or args.ldenoise) and got_points):

                hls = None
                if(args.ldenoise):
                    hls = cv2.cvtColor(warped , cv2.COLOR_BGR2HLS)

                gray = cv2.cvtColor(warped , cv2.COLOR_BGR2GRAY) 
                gray = 255 - gray
                gray = gray.astype("float32")

                gray[0:3 , :] = 0.0
                gray[gray.shape[0] - 3 : gray.shape[0] , :] = 0.0
                gray[: , 0:3] = 0.0
                gray[: , gray.shape[1] - 3 : gray.shape[1]] = 0.0

                blured_gray = cv2.filter2D(gray , -1 , blur_kernel)
                
                stdv = numpy.sqrt(numpy.mean(((gray - blured_gray) * (gray - blured_gray)).flatten()))

                if(not args.ldenoise):
                    res = white

                    for l in levels:
                        res = numpy.where((gray - blured_gray) > l[0] * stdv , int(l[1]) * ones , res)

                    warped = cv2.merge((res , res , res))
                else:

                    h_res = hls[: , : , 0]
                    l_res = white.astype("float32")
                    s_res = hls[: , : , 2]
                    
                    l = levels[0]
                    
                    l_res = numpy.where((gray - blured_gray) > l_col * stdv , hls[: , : , 1] , l_res)

                    b_res = white.astype("float32")
                    
                    warped = cv2.cvtColor(cv2.merge((h_res.astype("uint8") , l_res.astype("uint8") , s_res.astype("uint8"))) , cv2.COLOR_HLS2BGR)

            
            if(args.kernel):
                kernel = numpy.array(
                            [
                                [ 0 , -1 ,  0] ,
                                [-1 ,  5 , -1] ,
                                [ 0 , -1 , 0 ]
                            ]
                        )
                warped = cv2.filter2D(warped , -1 , kernel)

            tosave = warped

            if(args.invert):
                warped = cv2.bitwise_not(warped)

            if(avg):
                frame_buff.append(warped)
                if(len(frame_buff) > f_buff):
                    frame_buff.pop(0)
               
                smooth = numpy.zeros(warped.shape , numpy.float32)

                for f in frame_buff:
                    smooth = smooth + f

                smooth = smooth / len(frame_buff)
                smooth = smooth.astype(warped.dtype)
                warped = smooth


            # Display the resulting frame
            cv2.imshow('frame',warped)

            key = cv2.waitKey(1)
 
            if(key == ord('q')):
                break
            elif(key == ord('s')):
                maxPng = 0
                for f in os.listdir(save_dir):
                    if(f[-4:] == ".png" and f[:-4].isdigit() and len(f) == 8):
                        if(int(f[:-4]) > maxPng):
                            maxPng = int(f[:-4])
                cv2.imwrite(os.path.join(save_dir , str(maxPng + 1).zfill(4) + ".png") , tosave)
            elif(key == ord('a')):
                avg = not avg
                frame_buff = []
            elif(key == ord('i')):
                args.invert = not args.invert
            elif(key == ord('d')):
                args.denoise = not args.denoise
            elif(key == ord('l')):
                args.ldenoise = not args.ldenoise
            elif(key == ord('w')):
                args.warp = not args.warp
            elif(key == ord('k')):
                args.kernel = not args.kernel
            elif(key == ord('f')):
                args.fullscreen = not args.fullscreen
                if(args.fullscreen):
                    cv2.setWindowProperty('frame' , cv2.WND_PROP_FULLSCREEN , cv2.WINDOW_FULLSCREEN)
                else:
                    cv2.setWindowProperty('frame' , cv2.WND_PROP_FULLSCREEN , cv2.WINDOW_NORMAL)


        # } main loop

    finally:

        cap.release()
        cv2.destroyAllWindows()
