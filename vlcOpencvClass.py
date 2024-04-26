import vlc
import ctypes
import numpy as np
import cv2 as cv

class vlcOpencvClass():
     """
     callback to override the default vlc locking function
     """
     CorrectVideoLockcb = ctypes.CFUNCTYPE(ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p))

     @CorrectVideoLockcb
     def _lock_cb(opaque,planes):

         self = ctypes.cast(opaque,ctypes.POINTER(ctypes.py_object)).contents.value
         planes[0] = self.vlc_video_buf_p
         return
    """
    callback to override the default vlc read function
    """
    @vlc.CallbackDecorators.VideoDisplayCb
    def _display_cb(opaque,picture):
        self = ctypes.cast(opaque,ctypes.POINTER(ctypes.py_object)).contents.value
        self.vlcFrameBuffer = np.ndarray(shape=(self.height,self.width,self.channels),dtype=np.ubyte,buffer=self.vlc_video_buf)
        return
    """
    initialise the vlc player 
    """
    def __init__(self,camera_settings):

        self.width = camera_settings['Camera_Horizontal_Resolution']
        self.height = camera_settings['Camera_Vertical_Resolution']
        self.fmt = camera_settings["Camera_fmt"]
        self.channels = 3

        #video buffers
        self.vlc_video_buf=(ctypes.c_ubyte * self.width*self.height*self.channels)()
        self.vlc_video_buf_p = ctypes.cast(self.vlc_video_buf,ctypes.c_void_p)
        self.vlcFrameBuffer = np.zeros((self.height,self.width,self.channels),np.uint8)

        #private pointer to self for lock/display callbacks
        self.ref_ref = ctypes.py_object(self)
        self.ref_p = ctypes.byref(self.ref_ref)

        #media player, callbacks and format
        self.player=vlc.MediaPlayer(camera_settings['Camera_Interface'])
        vlc.libvlc_video_set_callbacks(self.player,self._lock_cb, None, self._display_cb, self.ref_p)
        self.player.video_set_format(self.fmt,self.width,self.height,self.width*self.channels)

        self.player.play()
    """
        replicas of opencv functions
    """

    def read(self):
        temp_frame = self.vlcFrameBuffer.copy()

        #convert to correct color format
        temp_frame = cv.cvtColor(temp_frame,cv.COLOR_RGB2BGR)

        return True,temp_frame

    def isOpened(self):
        
        return self.player.is_playing() 

    def release(self):
        self.player.stop()
        self.player.release()
        return 
    #these methods are for compatibility at the moment
    def get(self,var):
        return 0

    def set(self,var,val):
        return 0
