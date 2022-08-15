import os
import cv2
import bpy
import json
import socket
import numpy as np
from math import radians
from base64 import b64encode
from bpy.types import Operator
from bpy.props import StringProperty
from mathutils import Vector, Quaternion

from bpy_extras.io_utils import ImportHelper

def encodeImg(img_array):
    # Use OpenCV to compress the image
    img_encode = cv2.imencode('.jpg', img_array,[cv2.IMWRITE_JPEG_QUALITY, bpy.context.scene.quality])[1]
    img_bytes = np.array(img_encode).tobytes()
    img_string = b64encode(img_bytes).decode('utf-8')
    print(len(img_string))
    return img_string

def packData(data):
    length = str(len(data))
    length = length.zfill(8)
    return length.encode('utf-8') + data

def driveCharacter(rotations, translation):
    try:
        scene = bpy.context.scene
        character = bpy.data.objects[scene.character_name]
        armature = bpy.data.armatures[scene.armature_name]
        pelvis_bone = armature.bones['Pelvis']
        pelvis_position = Vector(pelvis_bone.head)
        bones = character.pose.bones
        bones_name = ['Pelvis','L_Hip','R_Hip','Spine1','L_Knee','R_Knee','Spine2','L_Ankle','R_Ankle','Spine3','L_Foot','R_Foot','Neck','L_Collar','R_Collar','Head','L_Shoulder','R_Shoulder','L_Elbow','R_Elbow','L_Wrist','R_Wrist']

        rotations = np.array(rotations)
        translation = np.array(translation)

        scene.frame_current += scene.insert_interval
        if scene.translation:
            bones['Pelvis'].location = Vector((100 * translation[0], -100 * translation[1], -100 * translation[2]))
        else:
            bones['Pelvis'].location = Vector((0, 0, 0))

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
        return True
    except:
        return False

class OfflineAnimation(Operator, ImportHelper):
    bl_idname = 'ops.offline_animation'
    bl_label = 'Offline Animation'

    filter_glob: StringProperty( default='*.jpg;*.jpeg;*.png;*.mp4;*.avi;', options={'HIDDEN'} )

    def execute(self, ctx):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ctx.scene.ip, int(ctx.scene.port)))
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
            self.client.send(packData(init))

            img_array = cv2.imread(self.filepath)
            img_string = encodeImg(img_array)
            image = json.dumps(
                {
                    'type': 'image',
                    'content': img_string,
                }
            ).encode('utf-8')
            img_package = packData(image)
            self.client.send(img_package)
            data = self.client.recv(4096).decode('utf-8')

            if data != 'none':
                data = json.loads(data)
                if not driveCharacter(data['poses'], data['trans']):
                    self.report({"ERROR"}, "The armature/character's name is not found or the bones is not fixed")

            done = json.dumps(
                {
                    'type':'done'
                }
            ).encode('utf-8')
            print('transfer done')
            self.client.send(packData(done))
            self.client.close()
            return {'FINISHED'}
        
        if extension in video_extensions:
            init = json.dumps(
                {
                    'type': 'init',
                    'gpu': str(ctx.scene.gpu),
                    'mode': 'video',
                }
            ).encode('utf-8')
            self.client.send(packData(init))
            self.video = cv2.VideoCapture(self.filepath)
            self._timer = ctx.window_manager.event_timer_add(1 / ctx.scene.fps, window=ctx.window)
            ctx.window_manager.modal_handler_add(self)

            return {'RUNNING_MODAL'}

    def modal(self, ctx, evt):
        if evt.type == 'TIMER':
            ret, frame = self.video.read()
            if ret:
                cv2.imshow('frame', frame)
                cv2.waitKey(1)
                img_string = encodeImg(frame)
                image = json.dumps(
                    {
                        'type': 'image',
                        'content': img_string,
                    }
                ).encode('utf-8')
                img_package = packData(image)
                self.client.send(img_package)

                data = self.client.recv(4096).decode('utf-8')
                if data != 'none':
                    data = json.loads(data)
                    if not driveCharacter(data['poses'], data['trans']):
                        self.report({"ERROR"}, "The armature/character's name is not found or the bones is not fixed")
                        self.close(ctx)
                        return {'FINISHED'}
            else:
                self.close(ctx)
                return {'FINISHED'}

        if evt.type == 'ESC':
            self.close(ctx)
            return {'FINISHED'}

        return {'RUNNING_MODAL'}
    
    def close(self, ctx):
        done = json.dumps(
            {
                'type':'done'
            }
        ).encode('utf-8')
        print('transfer done')
        self.client.send(packData(done))
        self.client.close()
        cv2.destroyAllWindows()
        self.video.release()
        ctx.window_manager.event_timer_remove(self._timer)

class WebcamAnimation(Operator):
    bl_idname = 'ops.webcam_animation'
    bl_label = 'Webcam Animation'

    def execute(self, ctx):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ctx.scene.ip, int(ctx.scene.port)))
        ctx.scene.frame_start = ctx.scene.frame_current
        self.webcam = cv2.VideoCapture(0)
        self.webcam.set(3, ctx.scene.width)
        self.webcam.set(4, ctx.scene.height)
        cv2.namedWindow("frame")
        cv2.resizeWindow("frame",320, 240)

        init = json.dumps(
            {
                'type': 'init',
                'gpu': str(ctx.scene.gpu),
                'mode': 'webcam',
            }
        ).encode('utf-8')
        self.client.send(packData(init))

        self._timer= ctx.window_manager.event_timer_add(1 / ctx.scene.fps, window=ctx.window)
        ctx.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}
    
    def modal(self, ctx, evt):
        if evt.type == 'TIMER':
            ret, frame = self.webcam.read()
            while not ret:
                ret, frame = self.webcam.read()
            print(frame.shape)
            cv2.imshow('frame', frame)
            cv2.waitKey(1)
            img_string = encodeImg(frame)
            image = json.dumps(
                {
                    'type': 'image',
                    'content': img_string,
                }
            ).encode('utf-8')
            img_package = packData(image)
            self.client.send(img_package)
            data = self.client.recv(4096).decode('utf-8')
            if data != 'none':
                data = json.loads(data)
                if not driveCharacter(data['poses'], data['trans']):
                    self.report({"ERROR"}, "The armature/character's name is not found or the bones is not fixed")
                    self.close(ctx)
                    return {'FINISHED'}

        if evt.type == 'ESC':
            self.close(ctx)
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def close(self, ctx):
        done = json.dumps(
            {
                'type':'done'
            }
        ).encode('utf-8')
        print('transfer done')
        self.client.send(packData(done))
        self.client.close()
        cv2.destroyAllWindows()
        self.webcam.release()
        ctx.window_manager.event_timer_remove(self._timer)

