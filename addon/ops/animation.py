import os
import cv2
import json
import socket
import numpy as np
from PIL import Image
from io import BytesIO
from math import radians
from base64 import b64encode
from bpy.types import Operator
from bpy.props import StringProperty
from mathutils import Vector, Quaternion
from multiprocessing import Process, Manager, Value
from bpy_extras.io_utils import ImportHelper

def encodeImg(img_array):
    img = Image.fromarray(img_array)
    mem = BytesIO()
    img.save(mem, format='jpeg', optimize=True, quality=bpy.context.scene.quality)
    img_string = b64encode(mem.getvalue()).decode('utf-8')
    return img_string

def packData(data):
    length = str(len(data))
    length = length.zfill(8)
    return length.encode('utf-8') + data

def driveCharacter(rotations, translation):
    import bpy
    scene = bpy.context.scene
    character = bpy.data.objects[scene.character_name]
    armature = bpy.data.armatures[scene.armature_name]
    pelvis_bone = armature.bones['Pelvis']
    pelvis_position = Vector(pelvis_bone.head)
    bones = character.pose.bones
    bones_name = ['Pelvis','L_Hip','R_Hip','Spine1','L_Knee','R_Knee','Spine2','L_Ankle','R_Ankle','Spine3','L_Foot','R_Foot','Neck','L_Collar','R_Collar','Head','L_Shoulder','R_Shoulder','L_Elbow','R_Elbow','L_Wrist','R_Wrist']

    rotations = np.array(rotations)
    translation = np.array(translation)

    scene.frame_current += 1

    if scene.translation:
        bones['Pelvis'].location = Vector((100 * translation[0], -100 * translation[1], -100 * translation[2]))
    else:
        bones['Pelvis'].location = pelvis_position

    if scene.insert_keyframe:
        bones['Pelvis'].keyframe_insert('location')

    for index in range(len(bones_name)):
        bone = bones[bones_name[index]]

        bone_rotation = Quaternion(Vector((rotations[4 * index], rotations[4 * index + 1], rotations[4 * index + 2])), rotations[4 * index + 3])
        quat_x_180_cw = Quaternion((1.0, 0.0, 0.0), radians(-180))

        if bones_name[index] == 'Pelvis':
            bone.rotation_quaternion = (quat_x_180_cw ) @ bone_rotation
        else:
            bone.rotation_quaternion = bone_rotation
        if scene.insert_keyframe:
            bone.keyframe_insert('rotation_quaternion', frame = scene.frame_current)

    scene.frame_end = scene.frame_current
    return

class OfflineAnimation(Operator, ImportHelper):
    bl_idname = 'ops.offline_animation'
    bl_label = 'Offline Animation'

    filter_glob: StringProperty( default='*.jpg;*.jpeg;*.png;*.mp4;*.avi;', options={'HIDDEN'} )

    def execute(self, ctx):
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ctx.scene.ip, int(ctx.scene.port)))
        ctx.scene.frame_start = ctx.scene.frame_current

        filename, extension = os.path.splitext(self.filepath)

        image_extensions = ['.jpg','.jpeg','.png']
        video_extensions = ['.mp4','.avi']

        print(self.filepath)

        if extension in image_extensions:
            init = json.dumps(
                {
                    'type': 'init',
                    'gpu': str(ctx.scene.gpu),
                    'mode': 'image',
                }
            ).encode('utf-8')
            client.send(packData(init))

            img_array = cv2.imread(self.filepath)
            img_string = encodeImg(img_array)
            image = json.dumps(
                {
                    'type': 'image',
                    'content': img_string,
                }
            ).encode('utf-8')
            img_package = packData(image)
            client.send(img_package)
            data = json.loads(client.recv(4096).decode('utf-8'))
            driveCharacter(data['poses'], data['trans'])
            done = json.dumps(
                {
                    'type':'done'
                }
            ).encode('utf-8')
            client.send(packData(done))
            client.close()

            return {'FINISHED'}
        
        if extension in video_extensions:
            init = json.dumps(
                {
                    'type': 'init',
                    'gpu': str(ctx.scene.gpu),
                    'mode': 'video',
                }
            ).encode('utf-8')
            client.send(packData(init))

            global video
            video = cv2.VideoCapture(self.filepath)

            self._timer = ctx.window_manager.event_timer_add(1/30, window=ctx.window)
            ctx.window_manager.modal_handler_add(self)

            return {'RUNNING_MODAL'}

    def modal(self, ctx, evt):
        if evt.type == 'TIMER':
            ret, frame = video.read()
            if ret:
                img_string = encodeImg(frame)
                image = json.dumps(
                    {
                        'type': 'image',
                        'content': img_string,
                    }
                ).encode('utf-8')
                img_package = packData(image)
                client.send(img_package)

                data = json.loads(client.recv(4096).decode('utf-8'))
                driveCharacter(data['poses'], data['trans'])
            else:
                done = json.dumps(
                    {
                        'type':'done'
                    }
                ).encode('utf-8')
                print('transfer done')
                client.send(packData(done))
                client.close()
                return {'FINISHED'}

        if evt.type == 'ESC':
            done = json.dumps(
                {
                    'type':'done'
                }
            ).encode('utf-8')
            print('transfer done')
            client.send(packData(done))
            client.close()
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

async def runWebcam():
    pass


class WebcamAnimation(Operator):
    bl_idname = 'ops.webcam_animation'
    bl_label = 'Webcam Animation'

    def execute(self, ctx):

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ctx.scene.ip, int(ctx.scene.port)))
        ctx.scene.frame_start = ctx.scene.frame_current

        init = json.dumps(
            {
                'type': 'init',
                'gpu': str(ctx.scene.gpu),
                'mode': 'webcam',
            }
        ).encode('utf-8')
        client.send(packData(init))

        webcam = cv2.VideoCapture(0)
        webcam.set(cv2.CAP_PROP_FRAME_WIDTH, ctx.scene.width)
        webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, ctx.scene.height)

        self._timer = ctx.window_manager.event_timer_add(1/30, window=ctx.window)
        ctx.window_manager.modal_handler_add(self)
        
        print('Webcam started')

        ret, frame = webcam.read()
        if frame is not None:
            cv2.imshow("webcam", frame)
            img_bytes = encodeImg(frame)
            sender.put(img_bytes)
            print('Put image to sender')
            cv2.waitKey(20)

        ctx.window_manager.modal_handler_add(self)
        ctx.window_manager.event_timer_add(1 / 5, window=ctx.window)

        return {'RUNNING_MODAL'}
    
    def modal(self, ctx, event):
        if event.type == 'TIMER':
            if not self.sender.empty():
                img_bytes = self.sender.get()
                print(len(img_bytes))
                self.client.send(img_bytes)
                data = self.client.recv(4096)

                if data:
                    data = json.loads(data.decode('utf-8'))
                    driveCharacter(data['poses'], data['trans'])
                while not self.sender.empty():
                    self.sender.get()

        if event.type == 'ESC':
            self.client.send('done'.encode('utf-8'))
            self.run.value = 0
            self.client.close()
            return {'FINISHED'}

        return {'RUNNING_MODAL'}