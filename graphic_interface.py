# -*- coding: utf-8 -*-

import wx
flag = -1
class PhotoViewer_init(wx.App):
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
        self.frame = wx.Frame(None, title='史上最强Project', size = (1280, 500), pos = (0, 50))
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

        # the bottons of four application
        self.btn1 = wx.Button(self.panel, label="修改性别和头发颜色", pos=(100, 400))
        self.Bind(wx.EVT_BUTTON, self.Event_Close1, self.btn1)

        self.btn2 = wx.Button(self.panel, label="自动提取图片特征", pos=(400, 400))
        self.Bind(wx.EVT_BUTTON, self.Event_Close2, self.btn2)

        self.btn3 = wx.Button(self.panel, label="引入高斯噪声", pos=(700, 400))
        self.Bind(wx.EVT_BUTTON, self.Event_Close3, self.btn3)

        self.btn4 = wx.Button(self.panel, label="图片插值", pos=(1000, 400))
        self.Bind(wx.EVT_BUTTON, self.Event_Close4, self.btn4)

        self.btn0 = wx.Button(self.panel, label="Close", pos=(550, 450))
        self.Bind(wx.EVT_BUTTON, self.Event_Close0, self.btn0)

        # show
        self.panel.Layout()
        self.frame.Show()

    def partI(self): # Show Marked Image
        title = wx.StaticText(self.panel, label = "人脸检测", pos = (150, 10))
        title.SetFont(self.title_font)

        marked = wx.Image("face/marked.png", wx.BITMAP_TYPE_ANY) # 430 * 320
        wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(marked), pos = (20, 50))

    def partII(self): # Show faces
        title = wx.StaticText(self.panel, label = "属性分析（仅分析上镜率最高的四个人）", pos = (650, 10))
        title.SetFont(self.title_font)

        for i, (fp, attr) in enumerate(zip(self.fps, self.attrs)):
            # The coordinates
            face_coor = (500 if i < 2 else 890, 60 if i == 0 or i == 2 else 220)
            text_coor = (face_coor[0] + 140, face_coor[1] - 5)
            
            face = wx.Image(fp, wx.BITMAP_TYPE_ANY)
            wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(face), pos = face_coor)
            
            text = wx.StaticText(self.panel, label = attr, pos = text_coor)
            text.SetFont(self.body_font)


    def Event_Close0(self, event):
        global flag
        flag = 0
        self.frame.Close(True)

    def Event_Close1(self, event):
        global flag
        flag = 1
        self.frame.Close(True)

    def Event_Close2(self, event):
        global flag
        flag = 2
        self.frame.Close(True)

    def Event_Close3(self, event):
        global flag
        flag = 3
        self.frame.Close(True)

    def Event_Close4(self, event):
        global flag
        flag = 4
        self.frame.Close(True)


class PhotoViewer_1(wx.App):
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
        self.frame = wx.Frame(None, title='史上最强Project', size=(1280, 720), pos=(0, 50))
        self.panel = wx.Panel(self.frame)

        # Define font
        self.title_font = wx.Font(22, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.body_font = wx.Font(15, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)

        segment2 = wx.StaticLine(self.panel, pos=(10, 230), size=(1220, 8), style=wx.LI_HORIZONTAL)
        segment2.SetBackgroundColour(wx.BLACK)

        # self.partI()  # display Part I (marked picture)
        self.partII()  # display Part II (top 4 biggest faces)
        self.partIII()  # display Part III (DLGAN)

        # the back botton

        self.btn0 = wx.Button(self.panel, label="Back", pos=(1150, 645))
        self.Bind(wx.EVT_BUTTON, self.Event_Close0, self.btn0)

        # show
        self.panel.Layout()
        self.frame.Show()

    def partI(self):  # Show Marked Image
        title = wx.StaticText(self.panel, label="一、人脸检测", pos=(150, 10))
        title.SetFont(self.title_font)

        marked = wx.Image("face/marked.png", wx.BITMAP_TYPE_ANY)  # 430 * 320
        wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(marked), pos=(20, 50))

    def partII(self):  # Show faces
        #title = wx.StaticText(self.panel, label="属性分析（仅分析上镜率最高的四个人）", pos=(400, 10))
        #title.SetFont(self.title_font)
        title = wx.StaticText(self.panel, label="应用一：修改性别和头发颜色", pos=(500, 10))
        title.SetFont(self.title_font)
        for i, (fp, attr) in enumerate(zip(self.fps, self.attrs)):
            if i == 1:
                break
            # The coordinates
            face_coor = (400 if i < 2 else 790, 60 if i == 0 or i == 2 else 220)
            text_coor = (face_coor[0] + 140, face_coor[1] - 5)

            face = wx.Image(fp, wx.BITMAP_TYPE_ANY)
            wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(face), pos=face_coor)

            text = wx.StaticText(self.panel, label=attr, pos=text_coor)
            text.SetFont(self.body_font)

    def partIII(self):  # Show DLGAN Results


        for i, (fp, zw, attr) in enumerate(zip(self.DLGAN_fps, self.DLGAN_zw, self.DLGAN_attrs)):
            # the coordinates
            zw_coor = (70 + i * 160, 300)
            face_coor = (70 + i * 160, 320)
            text_coor = (face_coor[0] + 10, face_coor[1]+ 140)

            zx = wx.StaticText(self.panel, label=zw, pos=zw_coor)
            zx.SetFont(self.body_font)

            face = wx.Image(fp, wx.BITMAP_TYPE_ANY)
            wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(face), pos=face_coor)

            text = wx.StaticText(self.panel, label=attr, pos=text_coor)
            text.SetFont(self.body_font)

    def Event_Close0(self, event):
        global flag
        flag = -1
        self.frame.Close(True)


class PhotoViewer_2(wx.App):
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
        self.frame = wx.Frame(None, title='史上最强Project', size=(1280, 720), pos=(0, 50))
        self.panel = wx.Panel(self.frame)

        # Define font
        self.title_font = wx.Font(22, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.body_font = wx.Font(15, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)

        # Draw segmentation Line

        #segment2 = wx.StaticLine(self.panel, pos=(10, 230), size=(1220, 8), style=wx.LI_HORIZONTAL)
        #segment2.SetBackgroundColour(wx.BLACK)

        # self.partI()  # display Part I (marked picture)
        self.partII()  # display Part II (top 4 biggest faces)
        self.partIII()  # display Part III (DLGAN)

        # the back botton

        self.btn0 = wx.Button(self.panel, label="Back", pos=(550, 665))
        self.Bind(wx.EVT_BUTTON, self.Event_Close0, self.btn0)

        # show
        self.panel.Layout()
        self.frame.Show()

    def partI(self):  # Show Marked Image
        title = wx.StaticText(self.panel, label="一、人脸检测", pos=(150, 10))
        title.SetFont(self.title_font)

        marked = wx.Image("face/marked.png", wx.BITMAP_TYPE_ANY)  # 430 * 320
        wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(marked), pos=(20, 50))

    def partII(self):  # Show faces
#        title = wx.StaticText(self.panel, label="属性分析（仅分析上镜率最高的四个人）", pos=(400, 10))
#        title.SetFont(self.title_font)
        title = wx.StaticText(self.panel, label="应用二：自动提取图片特征", pos=(500, 10))
        title.SetFont(self.title_font)

        for i, (fp, attr) in enumerate(zip(self.fps, self.attrs)):
            if i != 0:
                break
            # The coordinates
            face_coor = (800 if i < 2 else 790, 60 if i == 0 or i == 2 else 220)
            text_coor = (face_coor[0] + 140, face_coor[1] - 5)

            face = wx.Image(fp, wx.BITMAP_TYPE_ANY)
            wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(face), pos=face_coor)

            text = wx.StaticText(self.panel, label=attr, pos=text_coor)
            text.SetFont(self.body_font)

    def partIII(self):  # Show DLGAN Results
        for i, (fp, zw, attr) in enumerate(zip(self.DLGAN_fps, self.DLGAN_zw, self.DLGAN_attrs)):
            # the coordinates
            if i < 4:
                zw_coor = (100 + i * 160, 100)
                face_coor = (100 + i * 160, 120)
                text_coor = (face_coor[0] + 10, face_coor[1] + 140)
            else:
                j = i - 4
                zw_coor = (100 + j * 160, 380)
                face_coor = (100 + j * 160, 400)
                text_coor = (face_coor[0] + 10, face_coor[1] + 140)

            zx = wx.StaticText(self.panel, label=zw, pos=zw_coor)
            zx.SetFont(self.body_font)

            face = wx.Image(fp, wx.BITMAP_TYPE_ANY)
            wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(face), pos=face_coor)

            text = wx.StaticText(self.panel, label=attr, pos=text_coor)
            text.SetFont(self.body_font)

    def Event_Close0(self, event):
        global flag
        flag = -1
        self.frame.Close(True)


class PhotoViewer_3(wx.App):
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
        self.frame = wx.Frame(None, title='史上最强Project', size=(1280, 720), pos=(0, 50))
        self.panel = wx.Panel(self.frame)

        # Define font
        self.title_font = wx.Font(22, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.body_font = wx.Font(15, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)

        # Draw segmentation Line

        #segment2 = wx.StaticLine(self.panel, pos=(10, 230), size=(1220, 8), style=wx.LI_HORIZONTAL)
        #segment2.SetBackgroundColour(wx.BLACK)

        # self.partI()  # display Part I (marked picture)
        self.partII()  # display Part II (top 4 biggest faces)
        self.partIII()  # display Part III (DLGAN)

        # the back botton

        self.btn0 = wx.Button(self.panel, label="Back", pos=(550, 665))
        self.Bind(wx.EVT_BUTTON, self.Event_Close0, self.btn0)

        # show
        self.panel.Layout()
        self.frame.Show()

    def partI(self):  # Show Marked Image
        title = wx.StaticText(self.panel, label="一、人脸检测", pos=(150, 10))
        title.SetFont(self.title_font)

        marked = wx.Image("face/marked.png", wx.BITMAP_TYPE_ANY)  # 430 * 320
        wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(marked), pos=(20, 50))

    def partII(self):  # Show faces
        #title = wx.StaticText(self.panel, label="属性分析（仅分析上镜率最高的四个人）", pos=(400, 10))
        #title.SetFont(self.title_font)

        for i, (fp, attr) in enumerate(zip(self.fps, self.attrs)):
            if i == 1:
                break
            
            # The coordinates
            face_coor = (700 if i < 2 else 790, 60 if i == 0 or i == 2 else 220)
            text_coor = (face_coor[0] + 140, face_coor[1] - 5)

            face = wx.Image(fp, wx.BITMAP_TYPE_ANY)
            wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(face), pos=face_coor)

            text = wx.StaticText(self.panel, label=attr, pos=text_coor)
            text.SetFont(self.body_font)

    def partIII(self):  # Show DLGAN Results
        title = wx.StaticText(self.panel, label="应用三:引入高斯噪声", pos=(600, 10))
        title.SetFont(self.title_font)

        for i, (fp, zw, attr) in enumerate(zip(self.DLGAN_fps, self.DLGAN_zw, self.DLGAN_attrs)):
            # the coordinates
            if i < 3:
                zw_coor = (70 + i * 160, 10)
                face_coor = (70 + i * 160, 30)
                text_coor = (face_coor[0] + 10, face_coor[1] + 140)
            elif i < 6:
                j = i - 3
                zw_coor = (70 + j * 160, 240)
                face_coor = (70 + j * 160, 260)
                text_coor = (face_coor[0] + 10, face_coor[1] + 140)
            else:
                j = i - 6
                zw_coor = (70 + j * 160, 470)
                face_coor = (70 + j * 160, 490)
                text_coor = (face_coor[0] + 10, face_coor[1] + 140)

            zx = wx.StaticText(self.panel, label=zw, pos=zw_coor)
            zx.SetFont(self.body_font)

            face = wx.Image(fp, wx.BITMAP_TYPE_ANY)
            wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(face), pos=face_coor)

            text = wx.StaticText(self.panel, label=attr, pos=text_coor)
            text.SetFont(self.body_font)

    def Event_Close0(self, event):
        global flag
        flag = -1
        self.frame.Close(True)


class PhotoViewer_4(wx.App):
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
        self.frame = wx.Frame(None, title='史上最强Project', size=(1280, 720), pos=(0, 50))
        self.panel = wx.Panel(self.frame)

        # Define font
        self.title_font = wx.Font(22, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.body_font = wx.Font(15, wx.DECORATIVE, wx.NORMAL, wx.LIGHT)

        # Draw segmentation Line

#        segment2 = wx.StaticLine(self.panel, pos=(10, 230), size=(1220, 8), style=wx.LI_HORIZONTAL)
#        segment2.SetBackgroundColour(wx.BLACK)

        # self.partI()  # display Part I (marked picture)
        # self.partII()  # display Part II (top 4 biggest faces)
        self.partIII()  # display Part III (DLGAN)

        # the back botton

        self.btn0 = wx.Button(self.panel, label="Back", pos=(550, 665))
        self.Bind(wx.EVT_BUTTON, self.Event_Close0, self.btn0)

        # show
        self.panel.Layout()
        self.frame.Show()

    def partI(self):  # Show Marked Image
        title = wx.StaticText(self.panel, label="一、人脸检测", pos=(150, 10))
        title.SetFont(self.title_font)

        marked = wx.Image("face/marked.png", wx.BITMAP_TYPE_ANY)  # 430 * 320
        wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(marked), pos=(20, 50))

    def partII(self):  # Show faces
#        title = wx.StaticText(self.panel, label="属性分析（仅分析上镜率最高的四个人）", pos=(400, 10))
#        title.SetFont(self.title_font)
        title = wx.StaticText(self.panel, label="应用四：图片插值", pos=(500, 10))
        title.SetFont(self.title_font)

        for i, (fp, attr) in enumerate(zip(self.fps, self.attrs)):
            # The coordinates
            if i != 0:
                break
                # The coordinates
            face_coor = (800 if i < 2 else 790, 60 if i == 0 or i == 2 else 220)
            text_coor = (face_coor[0] + 140, face_coor[1] - 5)

            face = wx.Image(fp, wx.BITMAP_TYPE_ANY)
            wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(face), pos=face_coor)

            text = wx.StaticText(self.panel, label=attr, pos=text_coor)
            text.SetFont(self.body_font)

    def partIII(self):  # Show DLGAN Results
        title = wx.StaticText(self.panel, label="应用四：图片插值", pos=(500, 10))
        title.SetFont(self.title_font)
        for i, (fp, zw, attr) in enumerate(zip(self.DLGAN_fps, self.DLGAN_zw, self.DLGAN_attrs)):
            # the coordinates
            if i == 0:
                zw_coor = (10, 100)
                face_coor = (10, 120)
                text_coor = (face_coor[0] + 10, face_coor[1] + 140)
            elif i == 1:
                zw_coor = (1100, 100)
                face_coor = (1100, 120)
                text_coor = (face_coor[0] + 10, face_coor[1] + 140)
            elif i < 6:
                j = i - 2
                zw_coor = (220 + j * 230, 70)
                face_coor = (220 + j * 230, 90)
                text_coor = (face_coor[0] + 10, face_coor[1] + 140)
            elif i < 10:
                j = i - 6
                zw_coor = (220 + j * 230, 320)
                face_coor = (220 + j * 230, 340)
                text_coor = (face_coor[0] + 10, face_coor[1] + 140)
            else:
                break
            zx = wx.StaticText(self.panel, label=zw, pos=zw_coor)
            zx.SetFont(self.body_font)

            face = wx.Image(fp, wx.BITMAP_TYPE_ANY)
            wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(face), pos=face_coor)

            text = wx.StaticText(self.panel, label=attr, pos=text_coor)
            text.SetFont(self.body_font)

    def Event_Close0(self, event):
        global flag
        flag = -1
        self.frame.Close(True)
