# Blender addon for driving character

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![stars](https://img.shields.io/github/stars/yanch2116/CDBA.svg?style=flat)
![GitHub repo size](https://img.shields.io/github/repo-size/yanch2116/CDBA.svg)

This addon has two parts. The first part helps you get a 3D character that can be drived by ROMP. The second part is to drive a 3D character in Blender using ROMP based on image, video or webcam.

## Demo

- Use a video to drive a 3D character.
![image](demo/offline_animation.gif)

- Use webcam to drive a 3D character on a linux computer with GPU 1070.
![image](demo/webcam_linux_local.gif)

- Use webcam to drive a 3D character on a Macbook Pro connected to a linux server with GPU 1070.
![image](demo/webcam_mac_server.gif)

- Use webcam to drive a 3D character on a Macbook Pro with CPU.
![image](demo/webcam_mac_local.gif)

## Installation

### For Blender Addon
- Download [CharacterDriven-BlenderAddon]()
- Install the addon in Blender
- Check your 3d view and there should be two new menu item called CDBA and CATS
- Install opencv in Blender python

```Shell
# If your Blender python doesn't have pip, install pip first
/path/to/blender/python -m pip install opencv-python
```

### For Simple ROMP

```Shell
# If you want to use GPU, you need to install pytorch-gpu and cuda first.
pip install --upgrade setuptools numpy cython
pip install --upgrade simple-romp

# Test if romp run successfully.
romp --mode=video --show_largest -i=/path/to/video.mp4 -o=/path/to/results # For GPU
romp --mode=video --show_largest --onnx -i=/path/to/video.mp4 -o=/path/to/results # For CPU
```

## How To Use

A video tutorial is available [here]().

### Panel

![image](demo/ui.png)

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

### Make Your 3D Character Compatible with ROMP

- Use [mixamo auto-rigger](https://www.mixamo.com/#/) to rig your 3D character. Remember to select no fingers (25).
- Import the rigged 3D character to Blender.
- If your character is T-pose, skip this step. If your character is A-pose, 
   - install the [cats-blender-plugin](https://github.com/absolute-quantum/cats-blender-plugin) in Blender;
   - select your character and go to `Pose Mode`;
   - click the `CATS` tab, then click the `Apply as Rest Pose` button;
> All mixamo rigged characters are T-pose in Object Mode. You need to check whether your character's rest pose is A-pose or T-pose in Edit Mode.
- Click the `CDBA` tab, then click `Fix Bones` to make your character compatible with ROMP.
### Drive Your 3D Character

- Start Simple ROMP.
```Shell
python romp_server.py [port]
```
- Make sure the settings are correct in Blender CDBA Panel
   - Make sure your character object's and armature's name is same with the one in Common Panel.
   - Make sure you can connect to the romp_server using the IP and Port in Common Panel.
   - Other settings are optional, the default is fine.
- Click Offline Animation to use image or video to drive your character.
- Click Webcam Animation to use webcam to drive your character.

> The Blender and romp_server is not necessary to be in the same computer. You can install romp_server on a linux server and use port forwarding to make the romp_server can be accessed from your local computer. A simple method is to use VS Code to set up port forwarding as I do in the video tutorial.

If you are familiar with Blender and want to use your own model, you should make sure it's armature is SMPL's skeleton. The armature should name Armature and each bone has the same name as the bones in [demo model](blender/Alpha.fbx)(Only the 24 bones of SMPL skeleton are needed, and the fingers don't need to change their names).

- [ROMP](https://github.com/Arthur151/ROMP)
- [neuron_mocap_live-blender](https://github.com/pnmocap/neuron_mocap_live-blender)
- [QuickMocap-BlenderAddon](https://github.com/vltmedia/QuickMocap-BlenderAddon)
- [Mixamo](https://www.mixamo.com/#/)
- [模之屋](https://www.aplaybox.com/u/680828836)
- [cats-blender-plugin](https://github.com/absolute-quantum/cats-blender-plugin)
