# AI Introduction - Term Project

Given a raw image, this program can find all the faces of the given raw image, and select one of them, then display the results of DLGAN.

## To-Do List

- [ ] 看懂代码 XD
- [ ] 减少服务器延时，现在运行一遍程序需要16s
- [ ] 实现DLGAN的Application 2、3、4

## Folders

- ./raw : store the raw images which could be used as "test data set". **Please feel free to add more images**.

- ./face : when you run 'find_faces.py' or 'Main.py', this folder would store all the faces of input images. **Please read 'find_faces.py' for more detailed information**.

- ./camera : Our program supports capturing images from computer camera, this folder stores the images captured from camera.

- ./DLGAN : store the results of DLGAN (**12 images assigned different labels**)


## Files

- ./Main.py : The main program. You can choose whether use camera or not.

- ./find_faces.py : This file contains the function 'Find_faces_and_mark_them', which can find all the faces, and save them as file 'face/face0.png', 'face/face1.png'. **You can directly run this file(if \_\_name\_\_ == '\_\_main\_\_')**

- ./get_attributes.py : This file contains the function 'Attribute', which translates the attributes of the face(generated by Face++) into **natural language**.

- ./graphic_interface.py : this file contains a class 'PhotoViewer', which can display the marked images, the top 4 biggest faces, and the DLGAN results. 

- ./camera.py : thie file used for calling the computer camera. **If the user presses 's' in the keyborad, the images would be saved.** Main.py would call this function.

- ./client.py : **because the DLGAN models are stored in the server**, this file is used to communicate with the server. The input is the file path of the face, and the outputs are DLGAN results(12 images assigned different labels).

- ./util.py : this file contains the necessary tools which are used in ./client.py

- ./facepp_API.py : This file contains the function 'connect_to_facepp', which can connect to 'Face++' website (a free CV paltform) and get the attributes(json format) of the given face, like age, gender. **Please see [Face++](https://console.faceplusplus.com.cn/documents/4888373) for more details**.

## Usage

1. If you just want to find all faces of the raw image, please run 'find_faces.py'

2. If you want to display the results of DLGAN, please run 'Main.py'.
    - **Before you run 'Main.py', please change the ssh port to go through the firewall**
    
        - > The command is in our WeChat Group
    
    - **Before you run 'Main.py', please login server and run these commands**
        - > source /home/haodong/Workspace/env3/bin/activate
        - > cd /raid/zhaoyihao/code3/ILGAN/ILGAN-16/
        - > python server.py
        
        - > The server account and password is in our WeChat Group
        
    - **You should use this command 'pythonw Main.py' to support graphic interface**
