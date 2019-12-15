# -*- coding: utf-8 -*-

import wx

class PhotoViewer(wx.App):
    def __init__(self, fps, attrs, DLGAN_fps, DLGAN_zw, DLGAN_attrs):
        '''
        fps, attrs are used to display the top 4 biggest faces with their compelete attributes.
        fps represents the file path.

        DLGAN_fps, DLGAN_zw, DLGAN_attrs are used to display the results of DLGAN.
        DLGAN_zw is the label, like man with black hair, or woman with brown hair.
        '''
    
        wx.App.__init__(self)
        self.fps = fps
        self.attrs = attrs
        self.DLGAN_fps = DLGAN_fps
        self.DLGAN_zw = DLGAN_zw
        self.DLGAN_attrs = DLGAN_attrs

        # Display Title
        self.frame = wx.Frame(None, title='史上最强Project', size = (1280, 720), pos = (0, 50))
        self.panel = wx.Panel(self.frame)
        
        # Define font
        self.title_font = wx.Font(22, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.body_font = wx.Font(15, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)

        # Draw segmentation Line
        segment1 = wx.StaticLine(self.panel, pos = (470, 10), size = (8, 370), style = wx.LI_VERTICAL)
        segment1.SetBackgroundColour(wx.BLACK)

        segment2 = wx.StaticLine(self.panel, pos = (10, 380), size = (1220, 8), style = wx.LI_HORIZONTAL)
        segment2.SetBackgroundColour(wx.BLACK)

        self.partI()    # display Part I (marked picture)
        self.partII()   # display Part II (top 4 biggest faces)
        self.partIII()  # display Part III (DLGAN)

        # the 'finish' botton 
        self.btn = wx.Button(self.panel, label="Finish", pos = (600, 665))
        self.Bind(wx.EVT_BUTTON, self.Event_Close, self.btn)

        # show
        self.panel.Layout()
        self.frame.Show()

    def partI(self): # Show Marked Image
        title = wx.StaticText(self.panel, label = "一、人脸检测", pos = (150, 10))
        title.SetFont(self.title_font)

        marked = wx.Image("face/marked.png", wx.BITMAP_TYPE_ANY) # 430 * 320
        wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(marked), pos = (20, 50))

    def partII(self): # Show faces
        title = wx.StaticText(self.panel, label = "二、属性分析（仅分析上镜率最高的四个人）", pos = (650, 10))
        title.SetFont(self.title_font)

        for i, (fp, attr) in enumerate(zip(self.fps, self.attrs)):
            # The coordinates
            face_coor = (500 if i < 2 else 890, 60 if i == 0 or i == 2 else 220)
            text_coor = (face_coor[0] + 140, face_coor[1] - 5)
            
            face = wx.Image(fp, wx.BITMAP_TYPE_ANY)
            wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(face), pos = face_coor)
            
            text = wx.StaticText(self.panel, label = attr, pos = text_coor)
            text.SetFont(self.body_font)
    
    def partIII(self): # Show DLGAN Results
        title = wx.StaticText(self.panel, label = "三、DLGAN 换脸结果（上镜率最高的人才能被换脸哦）", pos = (390, 400))
        title.SetFont(self.title_font)

        for i, (fp, zw, attr) in enumerate(zip(self.DLGAN_fps, self.DLGAN_zw, self.DLGAN_attrs)):
            # the coordinates
            zw_coor = (70 + i * 160, 440)
            face_coor = (70 + i * 160, 460)
            text_coor = (face_coor[0] + 10, face_coor[1] + 140)
            
            zx = wx.StaticText(self.panel, label = zw, pos = zw_coor)
            zx.SetFont(self.body_font)

            face = wx.Image(fp, wx.BITMAP_TYPE_ANY)
            wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(face), pos = face_coor)

            text = wx.StaticText(self.panel, label = attr, pos = text_coor)
            text.SetFont(self.body_font)

    def Event_Close(self, event):
        self.frame.Close(True)