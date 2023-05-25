# Mono Pose Animator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![GitHub repo size](https://img.shields.io/github/repo-size/yanchxx/CDBA.svg)

This addon helps you drive a 3D character in Blender using ROMP based on image, video or webcam and get a 3D character that can be drived by ROMP.

## Demo

- Use webcam to drive a 3D character on a linux computer with GPU 1070.

![webcam_linux_local](https://i.imgur.com/BGKjDkr.gif)

- Use webcam to drive a 3D character on a Macbook Pro connected to a linux server with GPU 1070. (Due to the network latency and program limitation in Blender python, the driving is not fluent.)

![webcam_mac_server](https://i.imgur.com/f8ZykuP.gif)  

- Use a video to drive 3D characters.

<https://user-images.githubusercontent.com/38496769/187074564-621cd40e-6da4-4d17-839a-42bb676578d4.mp4>

<https://user-images.githubusercontent.com/38496769/187074566-96d89b59-4721-4ccd-9a6d-c13d4b146f71.mp4>

## Installation

### For Blender Addon

- Download the [addon.zip](https://github.com/yanchxx/CDBA/releases/download/v1.0/addon.zip).
- Install the addon in Blender.
- Check your 3d view and there should be a new menu item called CDBA.
- Install opencv in Blender python.

```Shell
# if your Blender python doesn't have pip, install pip first
/path/to/blender/python -m pip install opencv-python
```

### For Simple ROMP

```Shell
# create a conda environment separate from blender python
conda create -n simple_romp python=3.8 -y
conda install pytorch torchvision cudatoolkit -c pytorch # if you don't have GPU, don't execute this command
pip install --upgrade setuptools numpy cython
pip install --upgrade simple-romp

# test if romp run successfully
romp --mode=video --show_largest -i=/path/to/video.mp4 -o=/path/to/results # for GPU
romp --mode=video --show_largest --onnx -i=/path/to/video.mp4 -o=/path/to/results # for CPU
```

## How To Use

### Panel

![panel](https://i.imgur.com/LQGtecn.png)

Common

- Character: The character's object name.
- Armature: The character's armature name.
- IP: The IP address of the romp_server.
- Port: The port of the romp_server.
- Use GPU: Whether to use GPU.
- Use Translation: Whether to use estimated global translation.
- Insert Keyframes: Whether to insert keyframes.
- Insert Interval: The interval of inserted keyframes.
- Compression: The transferred image's compression quality.
- Fix Bones: Make mixamo rigged character compatible with ROMP.

Image or Video

- Offline Animation: Select your image or video file to drive your character.

Webcam

- FPS: The frame rate of the webcam.
- Width: The width of the webcam.
- Height: The height of the webcam.
- Webcam Animation: Open your webcam to drive your character.

### Drive Your 3D Character

- Import the rigged 3D character and use [test_data.zip](https://github.com/yanchxx/CDBA/releases/download/v1.0/test_data.zip) for test.
- Start [romp_server.py](romp_server.py).

```Shell
python romp_server.py [port]
```

- Open Blender using command line.

```Shell
# if you start the software by clicking on its icon
# it will crash when using webcam animation
blender 
```

- Make sure the settings are correct in Blender CDBA Panel
  - Make sure your character object's and armature's name is same with the one in Common Panel.
  - Make sure you can connect to the romp_server using the IP and Port in Common Panel.
  - Other settings are optional, the default is fine.
- Set the number in the red box to specify the starting point for keyframe insertion.
![frame_start](https://i.imgur.com/s5fd1U3.png)
- Click `Offline Animation` to use image or video to drive your character.
- Click `Webcam Animation` to use webcam to drive your character.

> The Blender and romp_server.py is not necessary to be in the same computer. You can run romp_server.py on a linux server and use port forwarding to make the romp_server can be accessed from your local computer. A simple method is to use VS Code to set up port forwarding.

### Make Your 3D Character Compatible with ROMP

- Use [mixamo auto-rigger](https://www.mixamo.com/#/) to rig your 3D character. Remember to select no fingers (25).
- Import the rigged 3D character to Blender.
- If your character is T-pose, skip this step. If your character is A-pose,
  - install the [cats-blender-plugin](https://github.com/absolute-quantum/cats-blender-plugin) in Blender;
  - select your character and go to `Pose Mode`;
  - click the `CATS` tab, then click the `Apply as Rest Pose` button.

> All mixamo rigged characters are T-pose in Object Mode. You need to check whether your character's rest pose is A-pose or T-pose in Edit Mode.

- Click the `CDBA` tab, then click `Fix Bones` to make your character compatible with ROMP.

## Acknowledgement

- [模之屋](https://www.aplaybox.com/u/680828836)
- [ROMP](https://github.com/Arthur151/ROMP)
- [Mixamo](https://www.mixamo.com/#/)
- [cats-blender-plugin](https://github.com/absolute-quantum/cats-blender-plugin)
- [neuron_mocap_live-blender](https://github.com/pnmocap/neuron_mocap_live-blender)
- [QuickMocap-BlenderAddon](https://github.com/vltmedia/QuickMocap-BlenderAddon)
