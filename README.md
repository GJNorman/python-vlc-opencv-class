# python-vlc-opencv-class
class for interfacing python-vlc with opencv


example usage

    from vlcOpencvClass import vlcOpencvClass
    import cv2 as cv

    # settings are defined in a dictionary
    camera_settings = { 
        "Camera_fmt": "RV24",
        "Camera_Horizontal_Resolution":1280,
        "Camera_Vertical_Resolution":720,
        "Camera_Interface":"rtsp://192.168.0.1:1234"
    }

    # interface replciates opencv's

    cap = vlcOpencvClass(camera_settings)

    while cap.isOpened():
        success,frame = cap.read()

        if success:
            cv.imshow('hello!',frame)
    cap.release()
