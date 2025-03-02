import bpy
import math
from ..freetype import freetype
import numpy as np
# import freetype
import sys
import ctypes
import random
from ctypes import wintypes
import os
import platform
from .Struct import StringText, CharObject


class DynamicText:
    last_frame : int = 0
    tempString : str = "hellllallwda"
    char_objects : list = []
    parent_objects : list = []

    def __init__(self):
        self.reset()
    
    def reset(self):
        self.char_objects = []
        self.parent_objects = []

    def GenerateSingleStaticText(self):
        self.char_objects.clear()
        print("GenerateStaticText")
        index = bpy.context.scene.CharacterFlow_index
        flow = bpy.context.scene.CharacterFlow_list[index]
        textfrag = flow.text_list[flow.textfrag_index]
        self.generate_String(flow, StringText(textfrag.text, 0, 0, 0), None)

        for staticTextObject in self.char_objects:
            self.update_static_text_object(staticTextObject)
        
    def GenerateAllStaticText(self, single_text : bool = False):
        self.char_objects.clear()
        if len(bpy.context.scene.CharacterFlow_list) == 0:
            return "请先创建一个字符流实例"
        index = bpy.context.scene.CharacterFlow_index
        flow = bpy.context.scene.CharacterFlow_list[index]

        if not flow.style:
            return "请先选择一个字符模板"

        collection_name = flow.name + "_Static"
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)
        current_frame = bpy.context.scene.frame_current

        # # 遍历flow.text_list, 生成字符集
        # unique_chars = set()
        # for text_frag in flow.text_list:
        #     # 假设textfrag对象有一个text属性或方法来获取文本内容
        #     text_content = text_frag.text  # 或者可能是 str(text_frag)，具体取决于textfrag对象的实现
        #     unique_chars.update(text_content)
        # chars = ''.join(sorted(unique_chars))  # 转换回字符串并排序，使结果稳定
        # atlas, char_info = self.create_font_atlas(font_path="C:\\Windows\\Fonts\\simhei.ttf", chars=chars)
        # 存储UV坐标
        # char_info[char] = {
        #     'uv_coords': [
        #         (x / image_size, y / image_size),               # 左下
        #         ((x + 256) / image_size, y / image_size),      # 右下
        #         (x / image_size, (y + 256) / image_size),      # 左上
        #         ((x + 256) / image_size, (y + 256) / image_size)# 右上
        #     ]
        # }
        # self.atlas_to_texture(atlas)

        if single_text:
            textfrag = flow.text_list[flow.textfrag_index]
            self.generate_String(flow, StringText(textfrag.text, 0, 0, 0), collection, 0)
        else:
            for i ,textfrag in enumerate(flow.text_list):
                print(f"textfrag {i} : {textfrag.text}")
                if flow.use_global_extra_time:
                    extra_time = flow.extra_time
                else:
                    extra_time = textfrag.extra_time
                parent = self.generate_String(flow, StringText(textfrag.text, textfrag.enter_time, textfrag.exit_time, extra_time), collection, i)

        bpy.context.scene.frame_set(current_frame)

        for staticTextObject in self.char_objects:
            self.update_static_text_object(staticTextObject)
        return "生成成功"

    def clear(self):
        print("clear")
        for char_object in self.char_objects:
            try:
                bpy.data.objects.remove(char_object.blender_object, do_unlink=True)
            except:
                pass
        for parent_object in self.parent_objects:
            try:
                bpy.data.objects.remove(parent_object, do_unlink=True)
            except:
                pass
        self.reset()


    def UpdateAll(self, scene=None, depsgraph=None):
        for flow in scene.CharacterFlow_list:
            if flow.is_enabled:
                self.UpdateString(scene, depsgraph, flow)


    def UpdateString(self, scene=None, depsgraph=None, flow=None):
        # 获取当前帧
        current_frame = scene.frame_current
        # 获取帧率
        fps : float = scene.render.fps

        # 计算当前时间(秒)
        current_time = current_frame / fps
        
        # 遍历parent_objects 如果parent_object没有任何子物体，删除
        parent_objects_to_remove = []
        for parent_object in self.parent_objects:
            try:
                if len(parent_object.children) == 0:
                    bpy.data.objects.remove(parent_object, do_unlink=True)
                    parent_objects_to_remove.append(parent_object)
            except:
                parent_objects_to_remove.append(parent_object)

        for parent_object in parent_objects_to_remove:
            self.parent_objects.remove(parent_object)
        

        # 遍历scene.text_list生成String
        for textfrag in flow.text_list:
            # if flow.use_global_offset_time:
            #     enter_time : float = textfrag.enter_time + flow.offset_time
            #     exit_time : float = textfrag.exit_time + flow.offset_time
            #     extra_time : float = textfrag.extra_time
            # else:
            enter_time : float = textfrag.enter_time
            exit_time : float = textfrag.exit_time
            extra_time : float = textfrag.extra_time

            if enter_time < current_time and exit_time + extra_time > current_time:
                if textfrag.is_active == False:
                    textfrag.is_active = True
                    self.generate_String(flow, StringText(textfrag.text, enter_time, exit_time, extra_time), None, 0)
                    for staticTextObject in self.char_objects:
                        self.update_static_text_object(staticTextObject)
            else:
                textfrag.is_active = False



        # 遍历char_objects 删除过期字符
        char_objects_to_remove = []
        for char_object in self.char_objects:
            extra_time : float = flow.extra_time if flow.use_global_extra_time else char_object.extra_time
            if not (char_object.enter_time < current_time and char_object.exit_time + extra_time > current_time):
                # print(f"char_object.enter_time: {char_object.enter_time}, exit_time: {char_object.exit_time + extra_time}, current_time: {current_time}")
                
                try:
                    # 确保blender_object存在且有效
                    if (char_object.blender_object and 
                        char_object.blender_object.name in bpy.data.objects):
                        
                        # 获取所有子物体的列表副本
                        children = list(char_object.blender_object.children)
                        
                        # 删除子物体
                        for child in children:
                            if child.name in bpy.data.objects:
                                bpy.data.objects.remove(child, do_unlink=True)
                        
                        # 删除主物体
                        if char_object.blender_object.name in bpy.data.objects:
                            bpy.data.objects.remove(char_object.blender_object, do_unlink=True)
                except ReferenceError:
                    print(f"Object already removed")
                except Exception as e:
                    print(f"Error removing object: {str(e)}")
                
                char_objects_to_remove.append(char_object)
        
        
        # 从列表中移除已删除的对象
        for char_object in char_objects_to_remove:
            if char_object in self.char_objects:
                self.char_objects.remove(char_object)
        
        
        # 遍历char_objects 更新每个blender_object的属性
        # for char_object in self.char_objects:
        #     try:
        #         if char_object.blender_object.name not in bpy.data.objects:
        #             self.char_objects.remove(char_object)
        #             continue
        #     except ReferenceError:
        #         self.char_objects.remove(char_object) 
        #         continue
            
        #     blender_object = char_object.blender_object
            
        #     # 计算属性值
        #     properties = {
        #         "age": current_time - char_object.enter_time,          # 已存在时间
        #         "life": char_object.exit_time - current_time,         # 剩余时间
        #         "span": char_object.exit_time - char_object.enter_time, # 总时长
        #         "extra": char_object.extra_time,                       # 额外时间
        #         "youth": (current_time - char_object.enter_time) / (char_object.exit_time - char_object.enter_time), # 生命进度
        #         "idx": char_object.char_index,                        # 字符索引
        #         "ridx": char_object.text_count - char_object.char_index - 1,  # 反向索引
        #         "i_ratio": char_object.char_index / char_object.text_count,   # 索引比例
        #         "count": char_object.text_count,                      # 总字符数
        #         "width": char_object.text_width,                      # 文本宽度
        #         "run": char_object.run,                              # 当前位置
        #         "col": char_object.col,                              # 列号
        #         "row": char_object.row,                              # 行号
        #         "cols": char_object.col_count,                       # 总列数
        #         "rows": char_object.row_count,                       # 总行数
        #         "c_ratio": char_object.col / char_object.col_count,  # 列比例
        #         "r_ratio": char_object.row / char_object.row_count,   # 行比例
        #         "rand": random.Random(char_object.char_index + hash(char_object.char)).random()
        #     }

        #     # 更新自定义属性
        #     if isinstance(char_object.custom_properties, dict):
        #         properties.update(char_object.custom_properties)
        #     elif isinstance(char_object.custom_properties, list):
        #         # 如果是列表，则将所有属性合并
        #         for prop_dict in char_object.custom_properties:
        #             if isinstance(prop_dict, dict):
        #                 properties.update(prop_dict)

        #     # 更新主物体属性
        #     self.update_object_properties(blender_object, properties)
            
        #     # 更新文本类型的子物体属性
        #     for child in blender_object.children:

        #         self.update_object_properties(child, properties)
        #         # if child.type == 'FONT':
        #         #     self.update_object_properties(child, properties)

        # 这上面的循环到这里结束了
        print(f"time -> {current_time:.2f} frame -> {current_frame}")
        self.last_frame = current_frame
    
    def get_char_metrics(self, char, path: str, face: freetype.Face, sys_face: freetype.Face):
        """获取字符的度量信息"""
        try:
            # 将Blender字体大小转换为合适的freetype大小

            # Blender的字体大小单位是米，需要转换为点数
            font_size = int(1.0 * 72)  # 转换为点数
            face.set_char_size(width=0, height=font_size*64, hres=72, vres=72)
            
            # 加载字形
            face.load_char(char, freetype.FT_LOAD_NO_BITMAP)

            # 如果face.glyph.metrics.width == 0，则使用系统字体
            if face.glyph.metrics.width == 0:
                face = sys_face
                face.set_char_size(width=0, height=font_size*64, hres=72, vres=72)
                face.load_char(char, freetype.FT_LOAD_NO_BITMAP)

            # 获取度量信息并转换回Blender单位
            scale_factor = 1.0 / font_size  # 转换比例
            metrics = {
                'width': face.glyph.metrics.width * scale_factor / 64.0,
                'advance': face.glyph.metrics.horiAdvance * scale_factor / 64.0,
                'bearing_x': face.glyph.metrics.horiBearingX * scale_factor / 64.0
            }

            return metrics
            
        except Exception as e:
            print(f"获取字符度量信息时出错: {str(e)}")
            # 返回默认值
            return {'width': 1.0 * 0.5, 'advance': 1.0 * 0.6, 'bearing_x': 0}
    
    def UnwarpLineSwitch(self, text: str):
        """
        解析text中的行切换
        输入: 包含'||'的字符串，如"hello||world"
        输出: (纯文本字符串, 换行计数数组)
        示例:
            输入: "ab||cdef||g"
            输出: ("abcdefg", [0, 0, 1, 0, 0, 0, 1])
            
            输入: "hello||||world"
            输出: ("helloworld", [0, 0, 0, 0, 0, 2, 0, 0, 0, 0])
        """
        result_text = ""
        line_switches = []
        pending_line_count = 0
        
        i = 0
        while i < len(text):
            if i + 1 < len(text) and text[i:i+2] == '||':
                # 计算连续的换行符数量
                line_count = 1
                next_pos = i + 2
                while next_pos + 1 < len(text) and text[next_pos:next_pos+2] == '||':
                    line_count += 1
                    next_pos += 2
                
                pending_line_count = line_count
                i = next_pos
            else:
                result_text += text[i]
                line_switches.append(pending_line_count)
                pending_line_count = 0
                i += 1
        
        if pending_line_count > 0:
            result_text += " "
            line_switches.append(pending_line_count)
                
        return result_text, line_switches
    
    
    def UnwarpCustomProperty(self, text: str):
        """

        灵活的属性解析系统，根据值的格式自动判断数据类型
        
        支持的格式：
        1. 布尔值：
        <foo></foo> -> {'foo': True}
        
        2. 元组/向量：
        <abc = (1.0, 3.3, -9.0)> -> {'abc': (1.0, 3.3, -9.0)}
        
        3. 数值：
        <test = 1.0> -> {'test': 1.0}
        <test2 = 1> -> {'test2': 1}
        
        4. 字符串：
        <str = "hello world"> -> {'str': "hello world"}
        <str2 = 'hello'> -> {'str2': "hello"}
        
        5. 颜色：
        <color = #ff9393> -> {'color': (1.0, 0.576, 0.576)}
        """
        result = ""
        properties = []
        current_props = {}
        tag_stack = []
        i = 0
        
        def parse_value(value: str):
            """智能解析值的类型"""
            value = value.strip()
            value_lower = value.lower()

            if value_lower == "true":
                return True
            elif value_lower == "false":
                return False
            
            # 处理颜色值 #RRGGBB 或 #RRGGBBAA 或 col = '#RRGGBB'
            if value.startswith('#') or (value.startswith("'#") and value.endswith("'")) or (value.startswith('"#') and value.endswith('"')):
                try:
                    # 如果值被引号包围，去除引号和#号
                    if value.startswith(("'#", '"#')):
                        color_value = value[2:-1]
                    else:
                        color_value = value[1:]  # 去除#号
                        
                    if len(color_value) == 6:  # RGB格式 RRGGBB
                        r = int(color_value[0:2], 16) / 255
                        g = int(color_value[2:4], 16) / 255
                        b = int(color_value[4:6], 16) / 255
                        return (r, g, b)
                    elif len(color_value) == 8:  # RGBA格式 RRGGBBAA
                        r = int(color_value[0:2], 16) / 255
                        g = int(color_value[2:4], 16) / 255
                        b = int(color_value[4:6], 16) / 255
                        a = int(color_value[6:8], 16) / 255
                        return (r, g, b, a)
                except ValueError:
                    pass
            
            # 处理元组/向量 (x, y, z)
            if value.startswith('(') and value.endswith(')'):
                try:
                    # 移除括号并分割
                    items = value[1:-1].split(',')
                    # 尝试转换为浮点数元组
                    return tuple(float(item.strip()) for item in items)
                except ValueError:
                    pass
            
            # 处理带引号的字符串
            if (value.startswith('"') and value.endswith('"')) or \
                (value.startswith("'") and value.endswith("'")):
                return value[1:-1]
            
            # 处理整数
            try:
                if '.' not in value:
                    return int(value)
            except ValueError:
                pass
            
            # 处理浮点数
            try:
                if '.' in value:
                    return float(value)
            except ValueError:
                pass
            
            # 如果都不是，返回原始字符串
            return value
        
        while i < len(text):
            if text[i] == '<':
                end_pos = text.find('>', i)
                if end_pos != -1:
                    tag_content = text[i+1:end_pos].strip()
                    
                    # 处理结束标签
                    if tag_content.startswith('/'):
                        tag_name = tag_content[1:]
                        if tag_stack and tag_stack[-1][0] == tag_name:
                            tag_stack.pop()
                            # 重建当前属性
                            current_props = {}
                            for _, props in tag_stack:
                                current_props.update(props)
                    else:
                        # 处理开始标签
                        tag_props = {}
                        
                        # 处理带值的标签
                        if '=' in tag_content:
                            tag_name, value = tag_content.split('=', 1)
                            tag_name = tag_name.strip()
                            parsed_value = parse_value(value)
                            tag_props[tag_name] = parsed_value
                        # 处理布尔标签
                        else:
                            tag_name = tag_content.strip()
                            tag_props[tag_name] = True
                        
                        current_props.update(tag_props)
                        tag_stack.append((tag_name, tag_props))
                    
                    i = end_pos + 1
                    continue
            
            if i < len(text):
                # if text[i] != '\n':
                result += text[i]
                properties.append(current_props.copy())
            
            i += 1
    
        return result, properties


    def generate_String(self, flow, String_text : StringText, collection : bpy.types.Collection, index : int):
        text : str = String_text.text
        enter_time : float = String_text.enter_time
        exit_time : float = String_text.exit_time
        extra_time : float = String_text.extra_time

        # 查找参考样式物体
        style_object = flow.style
        if not style_object:
            raise Exception("未找到字幕样式参考物体")

        # 查找dummy文本物体
        dummy = flow.anchor
        # if not dummy:
        #     raise Exception("未找到名为'dummy'的参考文本物体")
        # 创建空物体
        parent = bpy.data.objects.new(str(index) + "_" + text, None)  # None 表示这是一个空物体
        if collection is not None:
            # 首先从所有集合中移除物体
            for coll in parent.users_collection:
                coll.objects.unlink(parent)
            # 然后添加到指定集合中
            collection.objects.link(parent)
        else:
            bpy.context.scene.collection.objects.link(parent)
        # # 设置位置和旋转
        # parent.location = dummy.location.copy()
        # parent.rotation_euler = dummy.rotation_euler.copy()
        # 设置位置和旋转为初始值0
        if dummy:
            if flow.is_follow_anchor:
                parent.parent = dummy
                parent.location = (0, 0, 0)
                parent.rotation_euler = (0, 0, 0)
            else:
                parent.location = dummy.location.copy()
                parent.rotation_euler = dummy.rotation_euler.copy()
        else:
            parent.location = (0, 0, 0)
            parent.rotation_euler = (0, 0, 0)

        self.parent_objects.append(parent)

        char_width_scale = flow.text_gap_scale
        char_width_offset = -0.0
        run = 0.0
        col = 0
        line = 0

        # 解析text中的自定义属性
        text, custom_properties = self.UnwarpCustomProperty(text)

        text, line_switches = self.UnwarpLineSwitch(text)

        # 提前计算所有字符的metrics
        metrics_table = {}
        total_width = 0
        font_path = ""
        sys_fonts_path = ""

        if style_object.type == 'FONT':
            if style_object.data.font.filepath == "<builtin>" or style_object.data.font.filepath == "":
                font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "presets", "Bfont.ttf")
            else:
                font_path = style_object.data.font.filepath
        else:
            font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "presets", "Bfont.ttf")
        
        # if flow.metrics_font:
        #     font_path = flow.metrics_font.filepath
        # else:
        #     font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "presets", "Bfont.ttf")

        face = freetype.Face(font_path)

        # 优先使用Windows系统的黑体字体，否则使用插件自带的Bfont字体
        default_font = "C:\\Windows\\Fonts\\simhei.ttf" if platform.system() == "Windows" else None
        addon_font = os.path.join(os.path.dirname(os.path.dirname(__file__)), "presets", "Bfont.ttf")
        
        sys_fonts_path = default_font if default_font and os.path.exists(default_font) else addon_font

        sys_face = freetype.Face(sys_fonts_path)

        for char in text:
            if char not in metrics_table:
                metrics_table[char] = self.get_char_metrics(char, font_path, face, sys_face)
            total_width += metrics_table[char]['advance'] * char_width_scale + char_width_offset

        Max_line = 0
        Max_col = []
        line_width = []
        temp_list = []

        # 为每个字符创建文本物体

        for i, char in enumerate(text):

            # print(bpy.app.is_rendering)
            # 复制样式物体
            char_object = style_object.copy()
            char_object.data = style_object.data.copy()
            bpy.context.scene.collection.objects.link(char_object)

            new_metrics = {}

            # 自定义设置字体
            if custom_properties[i].get("_Font"):
                font_name = custom_properties[i]["_Font"]
                if font_name in bpy.data.fonts:
                    char_object.data.font = bpy.data.fonts[font_name]
                    face = freetype.Face(char_object.data.font.filepath)
                    new_metrics = self.get_char_metrics(char, char_object.data.font.filepath, face, sys_face)
                else:
                    print(f"警告: 未找到字体 '{font_name}'")
            else:
                new_metrics = metrics_table[char]

            # 如果is_static为True，则自动K可见性关键帧
            if collection is not None:
                self.set_visibility_keyframes(char_object, enter_time, exit_time, extra_time)
                
                # 首先从所有集合中移除物体
                for coll in char_object.users_collection:
                    print(coll.name)
                    if "RigidBody" not in coll.name:  # 跳过包含Rigidbody的集合
                        coll.objects.unlink(char_object)
                
                # 然后添加到指定集合中
                collection.objects.link(char_object)
            

            # 复制所有子物体（如果存在的话）
            if style_object.children:
                for child in style_object.children:
                    child_copy = child.copy()
                    # 检查child.data是否存在
                    if child.data:
                        child_copy.data = child.data.copy()
                    bpy.context.scene.collection.objects.link(child_copy)
                    # 设置父子关系
                    child_copy.parent = char_object
                    # 保持相对变换
                    child_copy.matrix_parent_inverse = child.matrix_parent_inverse.copy()
                    
                    if collection is not None:
                        self.set_visibility_keyframes(child_copy, enter_time, exit_time, extra_time)
                        # 将物体添加到集合中
                        for coll in child_copy.users_collection:
                            if "RigidBody" not in coll.name:  # 跳过包含Rigidbody的集合
                                coll.objects.unlink(child_copy)

                        collection.objects.link(child_copy)

                    # 如果子物体是文本物体，同步文本内容
                    if child_copy.type == 'FONT':
                        child_copy.data.body = char
                        if custom_properties[i].get("_Font"):
                            child_copy.data.font = bpy.data.fonts[custom_properties[i]["_Font"]]
                        if custom_properties[i].get("_Size"):
                            child_copy.data.size = custom_properties[i]["_Size"]

            # 设置字符属性
            if style_object.type == 'FONT':
                char_object.data.body = char

            # 设置字体大小
            if custom_properties[i].get("_Size"):
                char_object.data.size = custom_properties[i]["_Size"]

            # # 自定义设置字体
            # if custom_properties[i].get("font"):
            #     font_name = custom_properties[i]["font"]
            #     if font_name in bpy.data.fonts:
            #         char_object.data.font = bpy.data.fonts[font_name]
            #         face = freetype.Face(char_object.data.font.filepath)
            #         new_metrics = self.get_char_metrics(char, char_object.data.font.filepath, face, sys_face)
            #     else:
            #         print(f"警告: 未找到字体 '{font_name}'")
            # else:
            #     new_metrics = metrics_table[char]

            # 从预计算的metrics表中获取字符度量信息
            metrics = new_metrics

            # 如果使用自动换行信号
            if flow.use_switch_line:
                if run > flow.switch_line_scale:
                    line += 1
                    line_width.append(run)
                    run = 0
                    Max_col.append(col)
                    col = 0

            # 如果line_switches[i]为True，则换行
            if line_switches[i] > 0:
                line += line_switches[i]
                for _ in range(line_switches[i]):
                    line_width.append(run)
                    run = 0
                    Max_col.append(col)
                    col = 0

            col += 1

            # 如果i是最后一个字符，则添加col
            if i == len(text) - 1:
                line_width.append(run)
                Max_col.append(col)

            _run = run

            # 使用实际字符宽度设置位置
            if flow.Auto_Arrange:
                char_object.location.x = run
                char_object.location.y = line * -1.0 * flow.row_gap_scale
                size_scale_num = 1.0
                if custom_properties[i].get("_Size"):
                    size_scale_num = custom_properties[i]["_Size"]
                run += metrics['advance'] * char_width_scale * size_scale_num
            else:
                size_scale_num = 1.0
                if custom_properties[i].get("_Size"):
                    size_scale_num = custom_properties[i]["_Size"]
                run += metrics['advance'] * size_scale_num


            # 设置父物体
            char_object.parent = parent
            
            # 命名
            char_object.name = f"{i}_{char}"

            # 创建CharObject
            # char_object_ = CharObject(char_object, char, metrics, custom_properties[i], i, len(text), total_width, enter_time, exit_time, extra_time)
            char_object_ = CharObject()
            char_object_.blender_object = char_object
            char_object_.char = char
            char_object_.order = index
            char_object_.metrics = metrics
            char_object_.custom_properties = custom_properties[i]

            char_object_.run = _run

            char_object_.char_index = i
            char_object_.text_count = len(text)
            # char_object_.text_width = total_width

            char_object_.col = col
            char_object_.row = line

            char_object_.enter_time = enter_time
            char_object_.exit_time = exit_time
            char_object_.extra_time = extra_time
            
            temp_list.append(char_object_)
            Max_line = max(Max_line, line)

        
        for i, chr in enumerate(temp_list):
            # print(len(Max_col))
            chr.col_count = Max_col[chr.row]
            chr.row_count = Max_line + 1
            chr.text_width = line_width[chr.row]
            self.char_objects.append(chr)

        return parent


    def update_object_properties(self, obj, properties):
        # 设置自定义属性
        for key, value in properties.items():
            obj[key] = value

        # 更新所有几何节点修改器的属性
        for modifier in obj.modifiers:
            # 检查是否是几何节点修改器
            if modifier.type == 'NODES' and modifier.node_group:
                node_group = modifier.node_group
                input_node = next((node for node in node_group.nodes if node.type == 'GROUP_INPUT'), None)

                if input_node:
                    # 遍历所有几何节点输入接口
                    for socket in input_node.outputs:
                        # 获取接口名称（支持中英文）
                        socket_names = socket.name.split('|')
                        socket_names = [name.strip() for name in socket_names]
                        
                        # 检查properties中是否存在对应的键
                        for key, value in properties.items():
                            # 如果属性名匹配任意一个接口名
                            if key in socket_names:
                                try:
                                    modifier[socket.identifier] = value
                                except:
                                    print(f"无法设置属性 {key} = {value}")

        # 触发更新
        obj.update_tag(refresh={'OBJECT', 'DATA', 'TIME'})

    def set_visibility_keyframes(self, obj, enter_time: float, exit_time: float, extra_time: float = 0):
        """
        为指定物体设置可见性关键帧（优化版本）
        """
        # 确保有动画数据
        if not obj.animation_data:
            obj.animation_data_create()
        
        # 获取场景帧率并转换时间
        fps = bpy.context.scene.render.fps
        enter_frame = int(enter_time * fps)
        exit_frame = int(exit_time * fps)
        extra_frames = int(extra_time * fps)
        
        # 获取动画数据
        action = obj.animation_data.action
        if not action:
            action = bpy.data.actions.new(name=f"Visibility_{obj.name}")
            obj.animation_data.action = action
        
        # 创建FCurves（如果不存在）
        hide_viewport_fc = action.fcurves.find('hide_viewport')
        hide_render_fc = action.fcurves.find('hide_render')
        
        if not hide_viewport_fc:
            hide_viewport_fc = action.fcurves.new('hide_viewport')
        if not hide_render_fc:
            hide_render_fc = action.fcurves.new('hide_render')
        
        # 直接添加关键点
        frames = [enter_frame - 1, enter_frame, exit_frame + extra_frames]
        values = [1.0, 0.0, 1.0]  # True = 1.0, False = 0.0
        
        # 清除现有关键点
        hide_viewport_fc.keyframe_points.clear()
        hide_render_fc.keyframe_points.clear()
        
        # 批量添加关键点
        for fc in (hide_viewport_fc, hide_render_fc):
            for frame, value in zip(frames, values):
                keyframe = fc.keyframe_points.insert(frame, value)
                keyframe.interpolation = 'CONSTANT'


    def create_font_atlas(self, font_path: str, chars: str):
        """
        创建固定大小(256x256)的字符图集
        
        参数:
            font_path: 字体文件路径
            chars: 要渲染的字符集
        """
        # 加载字体
        face = freetype.Face(font_path)
        face.set_pixel_sizes(0, 256)  # 设置字体大小为256像素
        
        # 计算图集大小
        chars_count = len(chars)
        atlas_size = 1
        while (atlas_size * atlas_size) < chars_count:
            atlas_size *= 2
        
        # 创建图集图像
        image_size = atlas_size * 256  # 每个字符256x256
        atlas = np.zeros((image_size, image_size), dtype=np.uint8)
        
        # 字符信息字典
        char_info = {}
        
        # 渲染每个字符
        for i, char in enumerate(chars):
            print(f"渲染字符: {char}")
            # 计算字符在图集中的位置
            x = (i % atlas_size) * 256
            y = (i // atlas_size) * 256
            
            # 渲染字符
            face.load_char(char, freetype.FT_LOAD_RENDER)
            bitmap = face.glyph.bitmap
            
            # 计算偏移，使文字对齐到基线
            baseline_y = y + 192  # 将基线设置在256像素格子的3/4处
            x_offset = x + (256 - bitmap.width) // 2  # 水平居中
            y_offset = baseline_y - face.glyph.bitmap_top  # 从基线减去字形顶部到基线的距离
            
            # 将字符位图复制到图集中
            bitmap_array = np.array(bitmap.buffer).reshape(bitmap.rows, bitmap.width)
            atlas[y_offset:y_offset+bitmap.rows, x_offset:x_offset+bitmap.width] = bitmap_array
            
            # 存储UV信息为位置和缩放格式，调整Y坐标以匹配翻转后的图像
            y_flipped = image_size - (y + 256)  # 翻转Y坐标
            char_info[char] = {
                'position': (x / image_size, y_flipped / image_size),  # 左下角位置（origin）
                'scale': (256 / image_size, 256 / image_size)  # x和y方向的缩放比例
            }
        
        return atlas, char_info

    def atlas_to_texture(self, atlas: np.ndarray):
        # 将atlas转换为纹理
        image_name = "FontAtlas"
        height, width = atlas.shape
        
        # 创建或获取已存在的图像
        image = bpy.data.images.get(image_name)
        if image is not None:
            bpy.data.images.remove(image)  # 删除已存在的图像以确保尺寸正确
        image = bpy.data.images.new(image_name, width, height, alpha=False)
        
        # 在转换为像素之前先上下翻转图像
        atlas = np.flipud(atlas)
        
        # 将numpy数组转换为适合blender的格式
        # Blender期望的是RGBA格式，所以我们需要将灰度图扩展为RGBA
        pixels = np.repeat(atlas.flatten(), 4)  # 重复每个值4次来创建RGBA
        pixels[3::4] = 255  # 设置alpha通道为255
        
        # 更新图像像素
        image.pixels = pixels.astype(np.float32) / 255.0  # Blender期望0-1范围的浮点数
        
        # 创建纹理并链接到图像
        texture = bpy.data.textures.new(name=image_name, type='IMAGE')
        texture.image = image
        
        return texture

    def update_static_text_object(self, staticTextObject):
        """更新单个静态文本对象及其属性
        
        Args:
            staticTextObject: 静态文本对象
            
        Returns:
            bool: 是否成功更新
        """
        # 检查对象是否有效
        try:
            if staticTextObject.blender_object.name not in bpy.data.objects:
                self.char_objects.remove(staticTextObject)
                return False
        except ReferenceError:
            self.char_objects.remove(staticTextObject)
            return False
        
        blender_object = staticTextObject.blender_object
        
        # 计算基础属性
        properties = {
            "enter": staticTextObject.enter_time,
            "exit": staticTextObject.exit_time,
            "extra": staticTextObject.extra_time,
            "char": staticTextObject.char,
            "order": staticTextObject.order,
            "span": staticTextObject.exit_time - staticTextObject.enter_time,
            "idx": staticTextObject.char_index,
            "ridx": staticTextObject.text_count - staticTextObject.char_index - 1,
            "i_ratio": staticTextObject.char_index / staticTextObject.text_count,
            "count": staticTextObject.text_count,
            "width": staticTextObject.text_width,
            "run": staticTextObject.run,
            "col": staticTextObject.col,
            "row": staticTextObject.row,
            "cols": staticTextObject.col_count,
            "rows": staticTextObject.row_count,
            "rand": random.Random(staticTextObject.char_index + hash(staticTextObject.char)).random()
        }
        
        # 合并自定义属性
        self._merge_custom_properties(staticTextObject, properties)
        
        # 更新主物体和子物体的属性
        self.update_object_properties(blender_object, properties)
        for child in blender_object.children:
            self.update_object_properties(child, properties)
            
        return True
    
    def _merge_custom_properties(self, staticTextObject, properties):
        """合并自定义属性到属性字典中
        
        Args:
            staticTextObject: 静态文本对象
            properties: 要更新的属性字典
        """
        if isinstance(staticTextObject.custom_properties, dict):
            properties.update(staticTextObject.custom_properties)
        elif isinstance(staticTextObject.custom_properties, list):
            for prop_dict in staticTextObject.custom_properties:
                if isinstance(prop_dict, dict):
                    properties.update(prop_dict)

    # 原循环改为
    def update_all_static_text_objects(self):
        """更新所有静态文本对象"""
        for staticTextObject in self.char_objects:
            self.update_static_text_object(staticTextObject)

# .SRT文件 -> StringText[] -> CharObject[] -> render -> finish

# class DynamicTextController:
#     DynamicTexts : list = []
#     def __init__(self):
#         self.DynamicTexts = []
    
#     def add_text(self, text : DynamicText):
#         self.DynamicTexts.append(text)

#     def remove_text(self, text : DynamicText):
#         self.DynamicTexts.remove(text)