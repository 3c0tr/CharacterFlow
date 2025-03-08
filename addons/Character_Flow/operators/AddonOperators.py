import bpy
import random
import math
from mathutils import Vector
from bpy_extras.view3d_utils import region_2d_to_vector_3d, region_2d_to_location_3d
import os
from bpy_extras.io_utils import ExportHelper

from ..config import __addon_name__
from ..preference.AddonPreferences import ExampleAddonPreferences
from .DynamicText import DynamicText

# This Example Operator will scale up the selected object
class ExampleOperator(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.example_ops"
    bl_label = "ExampleOperator"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    # 使用类变量存储静态数据
    _controller = None
    _is_enabled = False  # 这已经是类变量（静态变量）了

    @classmethod
    def get_controller(cls):
        if cls._controller is None:
            cls._controller = DynamicText()
        return cls._controller

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

    def execute(self, context: bpy.types.Context):
        controller = self.get_controller()
        try:
            for handler in bpy.app.handlers.frame_change_post:
                print(f"- {handler.__name__}")
                if handler.__name__ == "UpdateAll":
                    bpy.app.handlers.frame_change_post.remove(handler)
                    print("handler is removed")
        except:
            print("remove error")
            pass
        print("handler is added")
        bpy.app.handlers.frame_change_post.append(controller.UpdateAll) 
        # for handler in bpy.app.handlers.frame_change_post:
        #     print(f"- {handler.__name__}")
        return {'FINISHED'}

class TestOperator(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.test_ops"
    bl_label = "TestOperator"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    # 添加类变量来存储控制器实例
    _controller = None

    @classmethod
    def get_controller(cls):
        if cls._controller is None:
            cls._controller = DynamicText()
        return cls._controller

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

    def execute(self, context: bpy.types.Context):
        pass
        return {'FINISHED'}

class StaticSingleTextOperator(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.static_single_text_ops"
    bl_label = "StaticSingleTextOperator"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    # 添加类变量来存储控制器实例
    _controller = None

    @classmethod
    def get_controller(cls):
        if cls._controller is None:
            cls._controller = DynamicText()
        return cls._controller

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

    def execute(self, context: bpy.types.Context):
        controller = self.get_controller()
        ret = controller.GenerateAllStaticText(True)
        if ret:
            self.report({'INFO'}, ret)
        return {'FINISHED'}

class StaticTextOperator(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.static_text_ops"
    bl_label = "StaticTextOperator"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    # 添加类变量来存储控制器实例
    _controller = None

    @classmethod
    def get_controller(cls):
        if cls._controller is None:
            cls._controller = DynamicText()
        return cls._controller

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

    def execute(self, context: bpy.types.Context):
        controller = self.get_controller()
        ret = controller.GenerateAllStaticText(False)
        if ret:
            self.report({'INFO'}, ret)
        return {'FINISHED'}


class AddStringFlowOperator(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.add_string_flow_ops"
    bl_label = "AddStringFlowOperator"

    phonetic_alphabet = [
        "Alice", "Basilisk", "Cipher", "Dragon", "Echo", "Frost", "Galaxy",
        "Halo", "Iron", "Jade", "Krama", "Leviathan", "Mercury", "Nebula",
        "Obsidian", "Phoenix", "Quartz", "Raven", "Sliver", "Thunder", "Undying",
        "Viper", "Wyvern", "Xenon", "You", "Zenith"
    ]

    def execute(self, context: bpy.types.Context):
        String_flow = context.scene.CharacterFlow_list.add()
        
        # 获取所有已存在的StringFlow名称
        existing_names = {flow.name for flow in context.scene.CharacterFlow_list[:-1]}
        
        # 从phonetic_alphabet中找到第一个未使用的名称
        for name in self.phonetic_alphabet:
            if name not in existing_names:
                String_flow.name = name
                break
        else:
            # 如果所有名称都被使用了，添加数字后缀
            base_name = self.phonetic_alphabet[0]
            counter = 1
            while f"{base_name}_{counter}" in existing_names:
                counter += 1
            String_flow.name = f"{base_name}_{counter}"
        
        new_textfrag = String_flow.text_list.add()
        new_textfrag.text = "this is a default text"
        new_textfrag.enter_time = 0
        new_textfrag.exit_time = 5
        new_textfrag.extra_time = 0
        
        return {'FINISHED'}

class RemoveStringFlowOperator(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.remove_string_flow_ops"
    bl_label = "RemoveStringFlowOperator"

    def execute(self, context: bpy.types.Context):
        context.scene.CharacterFlow_list.remove(context.scene.CharacterFlow_index)
        return {'FINISHED'}

class SwitchStringFlowOperator(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.switch_string_flow_ops"
    bl_label = "SwitchStringFlowOperator"

    def execute(self, context: bpy.types.Context):
        context.scene.CharacterFlow_list[context.scene.CharacterFlow_index].is_enabled = not context.scene.CharacterFlow_list[context.scene.CharacterFlow_index].is_enabled
        return {'FINISHED'}

class AddtextfragOperator(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.add_textfrag_ops"
    bl_label = "AddtextfragOperator"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}
    
    hints: list[str] = [
        "what a day",
        "potato is amazing",
        "revive me machine",
        "victory is yours! i submit!",
        "pineapple juice"
    ]

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

    def execute(self, context: bpy.types.Context):
        current_flow = context.scene.CharacterFlow_list[context.scene.CharacterFlow_index]
        # hint_count = context.scene.hint_count
        textfrag = current_flow.text_list.add()
        # textfrag.name = f"textfrag_{random.randint(0, 9999999999)}"
        roll = random.randint(0, 30)
        if roll != 7:

            textfrag.text = "new String text"
        else:
            second_roll = random.randint(0, len(self.hints) - 1)
            textfrag.text = self.hints[second_roll]
        return {'FINISHED'}
    
# class textfrag(bpy.types.PropertyGroup):
#     text: bpy.props.StringProperty(name="")
#     is_active: bpy.props.BoolProperty(name="is_active")
#     enter_time: bpy.props.FloatProperty(name="enter_time")
#     exit_time: bpy.props.FloatProperty(name="exit_time")
#     extra_time: bpy.props.FloatProperty(name="extra_time")
#     font: bpy.props.PointerProperty(type=bpy.types.VectorFont)
#     geometryNode: bpy.props.PointerProperty(type=bpy.types.NodeTree)
#     material: bpy.props.PointerProperty(type=bpy.types.Material)

class ImportSRTFileOperator(bpy.types.Operator):
    '''导入SRT字幕文件'''
    bl_idname = "object.import_srt_file_ops"
    bl_label = "ImportSRTFileOperator"

    def parse_time(self, time_str):
        # 解析时间字符串 "00:00:00,000" 转换为秒
        hours, minutes, seconds = time_str.replace(',', '.').split(':')
        total_seconds = float(hours) * 3600 + float(minutes) * 60 + float(seconds)
        # total_seconds = float(minutes) * 60 + float(seconds)
        return total_seconds

    def strip_html(self, text):
        # 简单移除HTML标签
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def execute(self, context: bpy.types.Context):
        current_flow = context.scene.CharacterFlow_list[context.scene.CharacterFlow_index]
        path = current_flow.srt_file_path
        if not path:
            self.report({'ERROR'}, "请先选择SRT文件路径")
            return {'CANCELLED'}

        
        # current_flow = context.scene.CharacterFlow_list[context.scene.CharacterFlow_index]

        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # 按空行分割字幕块
            Strings = content.strip().split('\n\n')
            
            for String in Strings:
                lines = String.strip().split('\n')
                if len(lines) >= 3:  # 确保至少有序号、时间和文本
                    # 解析时间行
                    time_line = lines[1]
                    start_time, end_time = time_line.split(' --> ')
                    
                    # 合并多行文本
                    if current_flow.is_srt_use_line_switch:
                        text = "||".join(lines[2:])
                    else:
                        text = ' '.join(lines[2:])
                    
                    # 创建新的textfrag
                    textfrag = current_flow.text_list.add()
                    if not current_flow.is_srt_use_html:
                        textfrag.text = self.strip_html(text)
                    else:
                        textfrag.text = text

                    textfrag.enter_time = self.parse_time(start_time) + current_flow.srt_time_offset
                    textfrag.exit_time = self.parse_time(end_time) + current_flow.srt_time_offset

            self.report({'INFO'}, f"成功导入 {len(Strings)} 条字幕")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"导入失败: {str(e)}")
            return {'CANCELLED'}

class RemovetextfragOperator(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.remove_textfrag_ops"
    bl_label = "RemovetextfragOperator"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

    def execute(self, context: bpy.types.Context):
        current_flow = context.scene.CharacterFlow_list[context.scene.CharacterFlow_index]
        current_flow.text_list.remove(current_flow.textfrag_index)
        return {'FINISHED'}


class SorttextfragOperator(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.sort_textfrag_ops"
    bl_label = "SorttextfragOperator"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

    def execute(self, context: bpy.types.Context):
        # 因为一些神奇的原因，我发现我最好使用冒泡排序对 text_list 进行排序
        current_flow = context.scene.CharacterFlow_list[context.scene.CharacterFlow_index]
        text_list = current_flow.text_list
        n = len(text_list)
        for i in range(n):

            swapped = False
            for j in range(0, n-i-1):
                if text_list[j].enter_time > text_list[j+1].enter_time:
                    text_list.move(j+1, j)
                    swapped = True
            if not swapped:
                break
        
        return {'FINISHED'}

class CleartextfragOperator(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.clear_textfrag_ops"
    bl_label = "CleartextfragOperator"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

    def execute(self, context: bpy.types.Context):
        current_flow = context.scene.CharacterFlow_list[context.scene.CharacterFlow_index]
        current_flow.text_list.clear()
        return {'FINISHED'}


class SetExtraTimeToAllOperator(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.set_extra_time_to_all_ops"
    bl_label = "SetExtraTimeToAllOperator"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

    def execute(self, context: bpy.types.Context):
        for textfrag in context.scene.text_list:
            textfrag.extra_time = context.preferences.addons[__addon_name__].preferences.extra_time
        return {'FINISHED'}


class AddCustomPropertySocketInGeometryNode(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.add_custom_property_socket_in_geometry_node_ops"
    bl_label = "AddCustomPropertySocketInGeometryNodeOperator"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

    def execute(self, context: bpy.types.Context):
        return {'FINISHED'}

class SetLanguageOperator(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.set_language_ops"
    bl_label = "SetLanguageOperator"

    language: bpy.props.StringProperty(name="language", default="zh-CN")

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

    def execute(self, context: bpy.types.Context):
        context.scene.StringFlow_language = self.language
        return {'FINISHED'}

class LoadPresetOperator(bpy.types.Operator):
    '''加载预设样式'''
    bl_idname = "object.load_preset_ops"
    bl_label = "加载预设样式"

    preset_name: bpy.props.StringProperty(name="preset_name", default="monkey", description="预设样式名称")   
    
    # PRESET_COLLECTION = "monkey"  # 预设集合的名称
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        preset_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "presets", "styles401.blend")
        print(f"尝试加载预设文件: {preset_file}")  # 添加这行来打印路径
        
        if not os.path.exists(preset_file):
            self.report({'ERROR'}, f"预设文件丢失: {preset_file}")
            return {'CANCELLED'}
            
        try:
            # 先检查文件中包含哪些集合
            with bpy.data.libraries.load(preset_file) as (data_from, _):
                print(f"文件中的集合: {data_from.collections}")  # 添加这行来查看可用的集合
            
            # 加载集合及其所有内容
            with bpy.data.libraries.load(preset_file, link=False, relative=True) as (data_from, data_to):
                if self.preset_name in data_from.collections:
                    data_to.collections = [self.preset_name]
                else:
                    self.report({'ERROR'}, f"找不到集合 '{self.preset_name}'")
                    return {'CANCELLED'}
            
            # 将集合链接到场景
            if len(data_to.collections) > 0 and data_to.collections[0] is not None:
                preset_collection = data_to.collections[0]
                context.scene.collection.children.link(preset_collection)
                
                # 选中集合中的主物体（如果需要）
                if len(preset_collection.objects) > 0:
                    main_obj = preset_collection.objects[0]
                    bpy.ops.object.select_all(action='DESELECT')
                    main_obj.select_set(True)
                    context.view_layer.objects.active = main_obj
                
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "加载预设失败")
                return {'CANCELLED'}
                
        except Exception as e:
            self.report({'ERROR'}, f"加载预设失败: {str(e)}")
            return {'CANCELLED'}

class HideCubeOperator(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.hide_cube_ops"
    bl_label = "HideCubeOperator"

    def execute(self, context: bpy.types.Context):
        # 寻找名为Cube的物体
        cube = bpy.data.objects.get("Cube")
        if cube:
            # 确保动画数据存在
            if not cube.animation_data:
                cube.animation_data_create()
            
            # 在第44帧设置为不可见
            context.scene.frame_set(44)
            cube.hide_viewport = True
            cube.hide_render = True
            cube.keyframe_insert(data_path="hide_viewport")
            cube.keyframe_insert(data_path="hide_render")
            
            # 在第45帧设置为可见
            context.scene.frame_set(45)
            cube.hide_viewport = False
            cube.hide_render = False
            cube.keyframe_insert(data_path="hide_viewport")
            cube.keyframe_insert(data_path="hide_render")
            
            # 在第60帧设置为可见
            context.scene.frame_set(60)
            cube.hide_viewport = False
            cube.hide_render = False
            cube.keyframe_insert(data_path="hide_viewport")
            cube.keyframe_insert(data_path="hide_render")
            
            # 在第61帧设置为不可见
            context.scene.frame_set(61)
            cube.hide_viewport = True
            cube.hide_render = True
            cube.keyframe_insert(data_path="hide_viewport")
            cube.keyframe_insert(data_path="hide_render")
            
        return {'FINISHED'}