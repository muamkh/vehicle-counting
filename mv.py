
# coding: utf-8

# In[ ]:


import numpy as np
import cv2
import time


# In[ ]:


def record_video():
    # Create a VideoCapture object
    cap = cv2.VideoCapture(url)

    # Check if ther is internet /  the link is correct
    if (cap.isOpened() == False):
        print("No internet conection or the link is broken")

    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    # We convert the resolutions from float to integer.
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define the codec and create VideoWriter object.The output is stored in 'file_name' file.
    out = cv2.VideoWriter(file_name,cv2.VideoWriter_fourcc('M','J','P','G'),fps,(frame_width,frame_height))

    limit_time = duration *(fps/10)
    start_time = time.time()
    while time.time() - start_time < limit_time:
        ret, frame = cap.read()

        if ret == True:
            # Write the frame into the file 'file_name'
            out.write(frame)
            
            # Display the resulting frame 
            cv2.imshow('recording....', frame)

            # Press Q on keyboard to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break
        
    # When everything done, release the video capture and video write objects
    cap.release()
    out.release()


# In[ ]:


def diff(f0,f1):
    difference = cv2.absdiff(f1,f0)
    return difference


# In[ ]:


def frame_difference():
    cap = cv2.VideoCapture(file_name)

    ret, frame0 = cap.read()
    ret, frame1 = cap.read()
    
    frame0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    while (cap.isOpened()):
        cv2.imshow("Diference",diff(frame0,frame1))
        
        ret,next_frame = cap.read()
        if ret == True:
            frame0 = frame1
            frame1 = cv2.cvtColor(next_frame,cv2.COLOR_BGR2GRAY)
        
            cv2.imshow('frame',frame0)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break


# In[ ]:


def background_modeling(tipe):
    cap = cv2.VideoCapture(file_name)
    i=0
    list_frame = list()
    while i < 30:
        if i%1 == 0:        
            ret,frame = cap.read()
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            list_frame.append(frame)
        i+=1
    list_frame = np.array(list_frame)

    if tipe == "mean":
        list_frame = np.mean(list_frame,axis=0).astype(np.uint8)
    if tipe == "median":
        list_frame = np.median(list_frame,axis=0).astype(np.uint8)
        
    cv2.imshow('bg',list_frame)
    return list_frame


# In[ ]:


def treshold(frame):
    frame[frame < T] = 0
    frame[frame>=T] =255

    return frame


# In[ ]:


def foreground_mask(bg):
    cap = cv2.VideoCapture(file_name)

    while (cap.isOpened()):
        ret,frame = cap.read()
        if ret == True:            
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            frame = diff(bg,frame)
            frame = treshold(frame)
            cv2.imshow("foreground mask", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break


# In[ ]:


####------> Main Program <------####------> Main Program <------####------> Main Program <------####------> Main Program <------####------> Main Program <------####
url = 'http://cctv-dishub.sukoharjokab.go.id/zm/cgi-bin/nph-zms?mode=jpeg&monitor=8&scale=100&maxfps=15&buffer=1000&user=user&pass=user'
file_name = 'output.avi'
duration = 120 # durasi in sec
fps = 15
T = 50

## record video from cctv sukoharjo with certain duration
record_video()

## frame differencing
frame_difference()

##background modeling
bg = background_modeling("mean")

## foreground mask
foreground_mask(bg)


cv2.waitKey()
# Closes all the frames
cv2.destroyAllWindows() 

