import bpy

from ..config import __addon_name__
from ..operators.AddonOperators import ExampleOperator, AddtextfragOperator, CleartextfragOperator, RemovetextfragOperator, ImportSRTFileOperator, SetExtraTimeToAllOperator, SorttextfragOperator, AddStringFlowOperator, RemoveStringFlowOperator, SwitchStringFlowOperator, LoadPresetOperator, SetLanguageOperator, StaticTextOperator, TestOperator, HideCubeOperator, StaticSingleTextOperator
from ....common.i18n.i18n import i18n
from ....common.types.framework import reg_order


class BasePanel(object):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Character Flow"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

class StringflowList(bpy.types.UIList):
    bl_label = "Character Flow List"
    bl_idname = "SCENE_UL_String_flow_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index):
        if item.is_enabled:
            layout.label(text= item.name + " (Enabled)", icon="KEYTYPE_EXTREME_VEC")
        else:
            layout.label(text= item.name + " (Disabled)", icon="KEYTYPE_JITTER_VEC")




class textfragList(bpy.types.UIList):
    bl_label = "String Fragment Bpy"

    bl_idname = "SCENE_UL_String_fragment_bpy"

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index):
        enter_time = item.enter_time
        exit_time = item.exit_time
        extra_time = item.extra_time
        text = item.text
        flow = context.scene.CharacterFlow_list[context.scene.CharacterFlow_index]
        final_string = f"{enter_time:.1f}-> {exit_time + extra_time:.1f} : {text}"
        current_time = bpy.context.scene.frame_current / bpy.context.scene.render.fps
        # print(f"current_time: {current_time}, enter_time: {enter_time}, exit_time: {exit_time}, extra_time: {extra_time}")

        if enter_time < current_time and exit_time + extra_time > current_time:
            layout.label(text=final_string, icon="KEYTYPE_EXTREME_VEC")
        # elif enter_time < current_time:
        #     layout.label(text=final_string, icon="KEYTYPE_GENERATED_VEC")
        else:
            layout.label(text=final_string, icon="KEYTYPE_JITTER_VEC")
        # layout.prop(item, "fragment_text")

@reg_order(0)
class StringMachineStatus(BasePanel, bpy.types.Panel):
    bl_label = "Character Flow Controller"
    bl_idname = "SCENE_PT_sample0"

    def draw(self, context: bpy.types.Context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        layout = self.layout
        # 获取当前语言设置
        current_language = bpy.app.translations.locale

        # layout.operator(ExampleOperator.bl_idname, depress=True, text="Text Auto Update is Enabled")
        # layout.operator(LoadPresetOperator.bl_idname, depress=True, text="Load Presets")

        row = layout.row()
        row.template_list("SCENE_UL_String_flow_list", "CharacterFlow_list", context.scene, "CharacterFlow_list", context.scene, "CharacterFlow_index")
        col = row.column(align=True)
        col.operator(AddStringFlowOperator.bl_idname, icon="ADD",text="")
        col.operator(RemoveStringFlowOperator.bl_idname, icon="REMOVE",text="")
        col.operator(ExampleOperator.bl_idname, icon="SYSTEM",text="")

        row = layout.row()
        if (len(context.scene.CharacterFlow_list) > 0):
            temp = context.scene.CharacterFlow_list[context.scene.CharacterFlow_index]
            if current_language == "zh_CN" or current_language == "zh_HANS":
                if (temp.is_enabled):
                    row.operator(SwitchStringFlowOperator.bl_idname, depress=True, text = temp.name + " 当前启用动态预览")
                else:
                    row.operator(SwitchStringFlowOperator.bl_idname, depress=False, text = temp.name + " 当前未启用动态预览")
            else:
                if (temp.is_enabled):
                    row.operator(SwitchStringFlowOperator.bl_idname, depress=True, text = temp.name + " Is Enable Dynamic Preview")
                else:
                    row.operator(SwitchStringFlowOperator.bl_idname, depress=False, text = temp.name + " Is Disable Dynamic Preview")
            # row = layout.row()
            # row.label(icon="WARNING_LARGE",text="不推荐在渲染时启用动态预览，尽量将字符流转化为静态对象再渲染")
            # row = layout.row()
            # row.label(text="如果启用动态字符流功能，在渲染时请将[渲染]->[锁定界面]开启")
        else:
            layout.label(text="Empty, please create a Character Flow instance first")

        # row = layout.row()
        # row.operator(HideCubeOperator.bl_idname, icon="SYSTEM",text="Hide Cube")
        row = layout.row()
        row.operator(StaticTextOperator.bl_idname,text="Spawn Static Character Flow")

        box = layout.box()
        box.label(icon="WARNING_LARGE",text="About Dynamic Preview and Static Objects")
        row = box.row()
        row.label(text="Dynamic Preview is only available in View Mode, it is recommended to convert the character flow to static objects before rendering")
        row = box.row()
        row.label(text="If you want to use dynamic preview in rendering, please enable [Render]->[Lock Interface]")
        # row = layout.row()
        # if any(handler.__name__ == 'UpdateAll' for handler in bpy.app.handlers.frame_change_post):
        #     row.operator(ExampleOperator.bl_idname, icon="SYSTEM", depress=True, text="Update by frame is Enabled Click to Modify")
        # else:
        #     row.operator(ExampleOperator.bl_idname, icon="SYSTEM",text="Update by frame is Disabled Click to Modify")


        # if context.scene.is_String_machine_enabled:


        #     layout.operator(ExampleOperator.bl_idname, depress=True, text="Text Auto Update is Enabled")
        # else:
        #     layout.operator(ExampleOperator.bl_idname, text="Text Auto Update is Disabled")

        # print(len(ExampleOperator.get_controller().char_objects))
        # layout.label(text="Current Chars number in Scene : " + str(len(ExampleOperator.get_controller().char_objects)))
        
    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True
    
@reg_order(1)
class StyleEditor(BasePanel, bpy.types.Panel):
    bl_label = "Style Editor"
    bl_idname = "SCENE_PT_sample1"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context: bpy.types.Context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        layout = self.layout
        # layout.label(text="文本将会自动生成在此物体的位置上")
        # row = layout.split(factor=0.25)
        # row.label(text="文本原点:")
        
        # row.prop_search(context.scene, "dummy", bpy.data, "objects", text="")

        # layout.separator()
        
        # layout.label(text="文本将在生成之后跟随这个物体运动")
        # row = layout.split(factor=0.25)
        # row.label(text="跟随物体:")
        # row.prop_search(context.scene, "String_follow_object", bpy.data, "objects", text="")

        # layout.separator()

        if len(context.scene.CharacterFlow_list) <= 0:
            layout.label(text="Please create a Character Flow instance first")
            return

        current_flow = context.scene.CharacterFlow_list[context.scene.CharacterFlow_index]

        # layout.label(text="文本将使用这个文本物体作为文字模板")
        row = layout.split(factor=0.25)
        row.label(text="Char Template:")
        row.prop_search(current_flow, "style", bpy.data, "fonts", text="")

        

        row = layout.split(factor=0.25)
        row.label(text="Char Anchor:")
        
        row.prop_search(current_flow, "anchor", bpy.data, "objects", text="")

        # row = layout.split(factor=0.25)
        # row.label(text="Metrics Font:")
        # row.prop_search(current_flow, "metrics_font", bpy.data, "fonts", text="")

        row = layout.row()
        row.prop(current_flow, "is_follow_anchor", text="Text will continue to follow the anchor point after generation")

        layout.separator()

        row = layout.row()
        row.prop(current_flow, "use_global_extra_time", text="use global extra time")

        # # row = layout.split(factor=0.25)
        # col = layout.column(align=True)
        # grid = col.grid_flow(row_major=True)
        # row = grid.row(align=False)
        # row.prop(current_flow, "use_global_extra_time", text="Use Global Extra Time")
        col = layout.column(align=True)
        col.enabled = current_flow.use_global_extra_time
        col.prop(current_flow, "extra_time",text="Global Extra Time")

        # row = layout.row()
        # row.prop(current_flow, "use_global_offset_time", text="是否使用全局偏移时间")

        # row = layout.row()
        # row.enabled = current_flow.use_global_offset_time
        # row.prop(current_flow, "offset_time",text="全局偏移时间")

        row = layout.row()
        row.prop(current_flow, "use_switch_line", text="use automatic line switching signal")


        row = layout.row()
        row.enabled = current_flow.use_switch_line
        row.prop(current_flow, "switch_line_scale",text="When the sum of the width of the characters in the current line exceeds this value, the line number will automatically +1")

        layout.separator()

        row = layout.row()
        if current_flow.Auto_Arrange:
            row.prop(current_flow, "Auto_Arrange", text="Auto Arrange Text")
        else:
            row.prop(current_flow, "Auto_Arrange", text="Auto Arrange Text (You can also manually control the text arrangement using the geometry node)")



        col = layout.column(align=True)  # 使用align=True来紧密排列
        col.enabled = current_flow.Auto_Arrange
        col.prop(current_flow, "text_gap_scale", text="Column Gap Scale")
        col.prop(current_flow, "row_gap_scale", text="Row Gap Scale")


        layout.separator()

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

@reg_order(2)
class ContentEditor(BasePanel, bpy.types.Panel):
    bl_label = "Content Editor"
    bl_idname = "SCENE_PT_sample2"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context: bpy.types.Context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        layout = self.layout

        if len(context.scene.CharacterFlow_list) <= 0:
            layout.label(text="Please create a Character Flow instance first!")
            return

        # layout.operator(ImportSRTFileOperator.bl_idname, icon="FILE_TICK",text="从.srt文件导入文本")
        layout.operator(CleartextfragOperator.bl_idname, icon="X",text="Clear All Existing Texts")
        layout.operator(SorttextfragOperator.bl_idname, icon="SORTTIME",text="Sort Texts by Enter Time")
        # layout.operator(StaticTextOperator.bl_idname, icon="MESH_CUBE",text="Spawn Static Text For Selected Text")
        layout.operator(StaticSingleTextOperator.bl_idname, icon="MESH_CUBE",text="Spawn Static Text For Selected Text")
        layout.separator()

        current_flow = context.scene.CharacterFlow_list[context.scene.CharacterFlow_index]

        row = layout.row()
        row.template_list("SCENE_UL_String_fragment_bpy", "text_list", 
                        current_flow, "text_list", 
                        current_flow, "textfrag_index")

        col = row.column(align=True)
        col.operator(AddtextfragOperator.bl_idname, icon="ADD",text="")
        col.operator(RemovetextfragOperator.bl_idname, icon="REMOVE",text="")


        row = layout.row()
        if len(current_flow.text_list) > 0 and current_flow.textfrag_index >= 0:
            # row = layout.row()
            # # row.alignment = "CENTER"
            # split = row.split(factor=0.75)
            # group1 = split.row(align=True)
            # group1.label(text="String Text")
            # group1.label(text="Enter Time")

            # group2 = split.row(align=True)
            # group2.label(text="Extra Time")
            if current_flow.textfrag_index >= len(current_flow.text_list):
                return
            current_textfrag = current_flow.text_list[current_flow.textfrag_index]
            col = layout.column(align=True)
            grid = col.grid_flow(row_major=True)
            row = grid.row(align=False)
            row.prop(current_textfrag, "enter_time", icon="TEXT",text="Enter Time")

            row = grid.row(align=False)
            row.prop(current_textfrag, "exit_time", icon="TEXT",text="Exit Time")

            row = grid.row(align=False)
            row.prop(current_textfrag, "extra_time", icon="TEXT",text="Extra Time")


            layout.prop(current_textfrag, "text", icon="GREASEPENCIL")
            # layout.label(text="Assign Settings Below, Will Override Global Setting")

            # col = layout.column(align=True)
            # col.prop(current_textfrag, "font", icon="FILE_FONT",text="")
            # col.prop(current_textfrag, "geometryNode", icon="NODE",text="")
            # col.prop(current_textfrag, "material", icon="MATERIAL",text="")
        else:
            col = layout.column()
            col.label(text="No String Can Be Edit")


    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True


# # This panel will be drawn after ExampleAddonPanel since it has a higher order value
# @reg_order(1)
# class ExampleAddonPanel2(BasePanel, bpy.types.Panel):
#     bl_label = "Example Addon Side Bar Panel"
#     bl_idname = "SCENE_PT_sample2"

#     def draw(self, context: bpy.types.Context):
#         layout = self.layout
#         layout.label(text="Second Panel")
#         layout.operator(ExampleOperator.bl_idname)

@reg_order(0)
class SRTFileImport(BasePanel, bpy.types.Panel):
    bl_label = "Import .srt File"
    bl_idname = "SCENE_PT_srt_file_import"
    bl_parent_id = "SCENE_PT_sample2"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 0

    def draw(self, context: bpy.types.Context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        layout = self.layout
        if len(context.scene.CharacterFlow_list) <= 0:
            layout.label(text="Please create a Character Flow instance first!")
            return
        current_flow = context.scene.CharacterFlow_list[context.scene.CharacterFlow_index]

        row = layout.row()
        left_col = row.column()
        left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
        left_col.label(text="")
        box = row.box()

        row = box.row()
        row.prop(current_flow, "is_srt_use_html",text="Import HTML Tags")
        row.prop(current_flow, "is_srt_use_line_switch",text="Import Line Switch")

        row = box.row()
        row.label(text=".srt file path")
        row.prop(current_flow, "srt_file_path",text="")

        row = box.row()
        row.label(text="Time Offset Seconds")
        row.prop(current_flow, "srt_time_offset",text="Time Offset Seconds")

        # row = layout.row()
        box.operator(ImportSRTFileOperator.bl_idname, icon="FILE_TICK",text="Import Text From .srt File")

        

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True


@reg_order(3)
class Tutorial(BasePanel, bpy.types.Panel):
    bl_label = "Tutorial"
    bl_idname = "SCENE_PT_tutorial"

    def draw(self, context: bpy.types.Context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        layout = self.layout
        # row = layout.row()
        # left_col = row.column()
        # left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
        # left_col.label(text="")
        # box = row.box()
        # box.label(text="语言选择/Language Selection", icon='SETTINGS')
        # row = box.row(align=True)
        # if context.scene.StringFlow_language == "zh-CN":
        #     row.operator(SetLanguageOperator.bl_idname, text="简体中文", depress=True).language = "zh-CN"
        #     row.operator(SetLanguageOperator.bl_idname, text="English").language = "en-US"
        # else:
        #     row.operator(SetLanguageOperator.bl_idname, text="简体中文").language = "zh-CN"
        #     row.operator(SetLanguageOperator.bl_idname, text="English", depress=True).language = "en-US"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

@reg_order(0)
class FirstUse(BasePanel, bpy.types.Panel):
    
    bl_label = "Quick Start"
    bl_idname = "SCENE_PT_first_use"
    bl_parent_id = "SCENE_PT_tutorial"
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context: bpy.types.Context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        language = bpy.app.translations.locale
        if language == "zh_CN" or language == "zh_HANS":
            layout = self.layout

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="基础配置", icon='SETTINGS')
            col = box.column()

            col.label(text="你需要最少3步即可完成最基础的配置！")

            box2 = col.box()
            box2.label(text="1.你需要创建至少一个字符流实例。点击最上方[字符流]面板的+按钮来创建一个新的字符流。")
            box2 = box.box()
            box2.label(text="2.你需要为你的字符流在[样式编辑器]面板中设置文字模板。文字模板通常是一个文本物体。")
            box2.label(text="你可以直接在场景中新建一个文本物体，设置你喜欢的字体与几何形状，然后使用吸管工具选择它作为文字模板。" ,icon="EVENT_A")
            row = box2.row()
            row = row.split(factor=0.6)
            row.label(text="或者你也可以使用这个已经准备好的文本打字机文字模板例程。", icon="EVENT_B")
            row.operator(LoadPresetOperator.bl_idname, text="点击获取打字机例程").preset_name = "TypeWriter"
            box2 = box.box()
            box2.label(text="3.你需要为你的字符流添加文本段落。点击[内容编辑器]面板的+按钮来添加你想要的文本段落。")
            box.separator()
            box2 = box.box()
            box2.label(text = "对效果满意之后，可以点击[字符流控制器]面板的[生成静态物体]按钮来生成静态物体。")
            box2.label(icon= "WARNING_LARGE", text="[在你完成了这一切之后，你可以试着拖动时间轴，查看实时生成的文字效果。]")
        else:
            layout = self.layout

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15
            left_col.label(text="")
            box = row.box()
            box.label(text="Quick Start", icon='SETTINGS')
            col = box.column()

            col.label(text="Complete these 3 steps to start:")

            box2 = col.box()
            box2.label(text="1. Create a Character Flow: Click + in [Character Flow] panel")
            box2 = box.box()
            box2.label(text="2. Set text template: Choose a text object in [Style Editor]")
            box2.label(text="Create a text object, style it, then pick it as template", icon="EVENT_A")
            row = box2.row()
            row = row.split(factor=0.6)
            row.label(text="Or use our pre-made typewriter template", icon="EVENT_B")
            row.operator(LoadPresetOperator.bl_idname, text="Get Typewriter").preset_name = "TypeWriter"
            box2 = box.box()
            box2.label(text="3. Add text: Click + in [Content Editor] to add text")
            box.separator()
            box2 = box.box()
            box2.label(text = "then, click the [Character Flow Controller] panel's [Generate Static Object] to generate static object.")
            box2.label(icon="WARNING_LARGE", text="[Now try timeline scrubbing to see text effects]")

@reg_order(1)
class FunctionIntroduction(BasePanel, bpy.types.Panel):
    bl_label = "Panel Introduction"
    bl_idname = "SCENE_PT_function_introduction"
    bl_parent_id = "SCENE_PT_tutorial"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context: bpy.types.Context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        language = bpy.app.translations.locale
        if language == "zh_CN" or language == "zh_HANS":
            layout = self.layout

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="字符流控制器使用简介", icon='SYSTEM')
            col = box.column()

            box2 = col.box()
            box2.label(text="字符流实例表格:  显示场景中的所有字符流实例，你可以在这里创建，删除，以及编辑字符流实例")
            box2 = col.box()
            box2.label(text="启用动态预览:  启用后，字符流实例将根据时间轴自动更新")
            box2 = col.box()
            box2.label(text="生成静态物体:  根据字符流实例生成静态物体，永久保留于场景中")

            layout.separator()

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="样式编辑器使用简介", icon='FONTPREVIEW')
            col = box.column()

            box2 = col.box()
            box2.label(text="字符模板:  填入一个物体，这个物体将决定字符流的样式")
            box2 = col.box()
            box2.label(text="字符锚点:  填入一个物体，字符将在这个物体的位置上生成，也可以使生成后的字符跟随其运动")
            box2 = col.box()
            box2.label(text="全局额外时间:  填入一个秒数，如果选择启用，这个时间将作为所有文本段落的额外时间秒数")
            box2 = col.box()
            box2.label(text="自动换行信号:  当前行的字符宽度之和超过这个值时，行数自动+1")
            box2 = col.box()
            box2.label(text="自动排列文字:  如果启用，将根据其行列位置自动设置字符物体的位置")
            box2 = col.box()
            box2.label(text="字符间距缩放:  填入一个缩放系数，这个缩放系数将决定字符的间距")

            layout.separator()

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="内容编辑器使用简介", icon='TEXT')
            col = box.column()

            box2 = col.box()
            box2.label(text="从srt文件导入:  点击这个按钮，你可以导入一个srt文件来添加文本段落。")
            box2 = col.box()
            box2.label(text="清除所有文本段落:  点击这个按钮，你可以清除所有已经存在的文本段落。")
            box2 = col.box()
            box2.label(text="排序文本段落:  点击这个按钮，你可以根据文本段落的进入时间对文本段落进行排序。")
            box2 = col.box()
            box2.label(text="生成静态物体:  点击这个按钮，你可以为选中的文本段落生成一个静态物体。")
            box2 = col.box()
            box2.label(text="文本段落表格:  这个表格包含了所有文本段落，你可以在这里编辑每个文本段落的文本内容以及时间信息")
            box2 = col.box()
            box2.label(text="进入时间:  这个时间决定了文本段落开始显示的时间。")
            box2 = col.box()
            box2.label(text="退出时间:  这个时间决定了文本段落结束显示的时间。")
            box2 = col.box()
            box2.label(text="额外时间:  文本段落结束显示后，已生成的文本物体继续显示的时间。(退出时间+额外时间=文本物体清除时间)")
            box2.label(icon= "WARNING_LARGE",text="[为什么要加入额外时间的设定? 这是给一些特定动画效果准备的，允许你创建更加有趣的文本消逝效果]")
        else:
            layout = self.layout

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15
            left_col.label(text="")
            box = row.box()
            box.label(text="Flow Controller Guide", icon='SYSTEM')
            col = box.column()

            box2 = col.box()
            box2.label(text="Flow List: Shows all Character Flows. Create, delete and edit flows here")

            box2 = col.box()
            box2.label(text="Enable Dynamic Preview:  Enabled, the flow will update automatically according to the timeline")
            box2 = col.box()
            box2.label(text="Generate Static Object:  Generate a static object based on the flow, permanently retained in the scene")

            layout.separator()

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15
            left_col.label(text="")
            box = row.box()
            box.label(text="Style Editor Guide", icon='FONTPREVIEW')
            col = box.column()

            box2 = col.box()
            box2.label(text="Char Template: Object that defines the flow style")
            box2 = col.box()
            box2.label(text="Char Anchor: Object where chars spawn and can follow")
            box2 = col.box()
            box2.label(text="Global Extra Time: Extra time applied to all text fragments")
            box2 = col.box()
            box2.label(text="Auto Line Break: Break line when width exceeds value")
            box2 = col.box()
            box2.label(text="Auto Arrange: Auto position chars by row/column")
            box2 = col.box()
            box2.label(text="Spacing Scale: Scale factor for char spacing")

            layout.separator()

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15
            left_col.label(text="")
            box = row.box()
            box.label(text="Content Editor Guide", icon='TEXT')
            col = box.column()

            box2 = col.box()
            box2.label(text="Import SRT: Import text fragments from .srt file")
            box2 = col.box()
            box2.label(text="Clear All: Remove all existing text fragments")
            box2 = col.box()
            box2.label(text="Sort: Sort fragments by enter time")
            box2 = col.box()
            box2.label(text="Spawn Static Text: Spawn a static text Object for selected text")
            box2 = col.box()
            box2.label(text="Fragment List: Edit text content and timing here")
            box2 = col.box()
            box2.label(text="Enter Time: When fragment starts showing")
            box2 = col.box()
            box2.label(text="Exit Time: When fragment stops showing")
            box2 = col.box()
            box2.label(text="Extra Time: Additional display time after exit")
            box2.label(icon="WARNING_LARGE",text="[Why Extra Time? For special effects and fancy text transitions]")

@reg_order(2)
class InstanceExample(BasePanel, bpy.types.Panel):
    bl_label = "Some Char Template Examples"
    bl_idname = "SCENE_PT_instance_example"
    bl_parent_id = "SCENE_PT_tutorial"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context: bpy.types.Context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        language = bpy.app.translations.locale
        if language == "zh_CN" or language == "zh_HANS":
            layout = self.layout

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="打字机", icon='MESH_CUBE')
            box2 = box.box()
            col = box2.column()
            # col.label(text="a simple typewriter effect, character will appear one by one")
            row = col.row()
            row = row.split(factor=0.6)
            row.label(text="字符会一个接一个地出现")
            row.operator(LoadPresetOperator.bl_idname, text="点击获取打字机例程").preset_name = "TypeWriter"

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="渐变现身", icon='MESH_CUBE')
            box2 = box.box()
            col = box2.column()
            # col.label(text="a simple typewriter effect, character will appear one by one")
            row = col.row()
            row = row.split(factor=0.6)
            row.label(text="字符会慢慢从透明开始出现")
            row.operator(LoadPresetOperator.bl_idname, text="点击获取渐变现身例程").preset_name = "FadeIn"

            layout.separator()
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="居中打字机", icon='MESH_CUBE')
            box2 = box.box()
            col = box2.column()
            # col.label(text="a simple typewriter effect, character will appear one by one")
            row = col.row()
            row.label(text="字符会一个接一个地出现")
            row = col.row()
            row = row.split(factor=0.6)
            row.label(text="但与此同时也会自动居中")
            row.operator(LoadPresetOperator.bl_idname, text="点击获取居中打字机例程").preset_name = "CenterTypeWriter"

            layout.separator()
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="米塔", icon='MESH_CUBE')
            box2 = box.box()
            col = box2.column()
            # col.label(text="a simple typewriter effect, character will appear one by one")
            row = col.row()
            row.label(text="灵感来源于游戏'米塔'中的文字效果")
            row = col.row()
            row.label(text="由于Blender 4.3 的API变化，更旧版本中使用可能会需要手动修复")
            row = col.row()
            row = row.split(factor=0.6)
            row.label(text="你需要添加extra time来查看所有效果")
            row.operator(LoadPresetOperator.bl_idname, text="点击获取米塔例程").preset_name = "MiSide"

            layout.separator()
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="对话栏", icon='MESH_CUBE')
            box2 = box.box()
            col = box2.column()
            # col.label(text="a simple typewriter effect, character will appear one by one")
            row = col.row()
            row.label(text="灵感来源于经典RPG游戏中的对话栏")
            row = col.row()
            row = row.split(factor=0.6)
            row.label(text="物体 \"Dialog Text\" 是你应当选择的物体")
            row.operator(LoadPresetOperator.bl_idname, text="点击获取对话栏例程").preset_name = "Dialog_Box"

            layout.separator()
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="卡牌摇晃", icon='MESH_CUBE')
            box2 = box.box()
            col = box2.column()
            # col.label(text="a simple typewriter effect, character will appear one by one")
            row = col.row()
            row.label(text="一个在桌面展开牌堆的动画")
            row = col.row()
            row.label(text="由于Blender 4.3 的API变化，更旧版本中使用可能会需要手动修复")
            row = col.row()
            row = row.split(factor=0.6)
            row.label(text="一个在几何节点中完成的华丽动画,请关闭[自动排列文字]")
            row.operator(LoadPresetOperator.bl_idname, text="点击获取卡牌摇晃例程").preset_name = "CardShake"

            # layout.separator()
            # row = layout.row()
            # left_col = row.column()
            # left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            # left_col.label(text="")
            # box = row.box()
            # box.label(text="刚体字符", icon='MESH_CUBE')
            # box2 = box.box()
            # col = box2.column()
            # # col.label(text="a simple typewriter effect, character will appear one by one")
            # row = col.row()
            # row.label(text="为字符添加刚体效果")
            # row = col.row()
            # row.label(text="你可以看到，字符不是父级物体，而是一个带有Collider的网格！")
            # row = col.row()
            # row = row.split(factor=0.6)
            # row.label(text="it just works!")
            # row.operator(LoadPresetOperator.bl_idname, text="点击获取刚体字符例程").preset_name = "Rigidbody"

            layout.separator()
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="HTML标签示例", icon='MESH_CUBE')
            box2 = box.box()
            col = box2.column()
            # col.label(text="a simple typewriter effect, character will appear one by one")
            # row = col.row()
            # row.label(text="You can use this test custom HTML property")
            row = col.row()
            row.label(text="试试这个：\"my mind is racing with <shake><color = #FF2F2F>endless fears</color></shake>\"")
            row = col.row()
            row = row.split(factor=0.6)
            row.label(text="你可以使用这个测试自定义的HTML属性")
            row.operator(LoadPresetOperator.bl_idname, text="点击获取HTML标签示例例程").preset_name = "HTML_Example"
        
        else:
            layout = self.layout

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="Typewriter", icon='MESH_CUBE')
            box2 = box.box()
            col = box2.column()
            # col.label(text="a simple typewriter effect, character will appear one by one")
            row = col.row()
            row = row.split(factor=0.6)
            row.label(text="Characters will appear one by one")
            row.operator(LoadPresetOperator.bl_idname, text="Click get Typewriter preset").preset_name = "TypeWriter"

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="FadeIn", icon='MESH_CUBE')
            box2 = box.box()
            col = box2.column()
            # col.label(text="a simple typewriter effect, character will appear one by one")
            row = col.row()
            row = row.split(factor=0.6)
            row.label(text="Characters will slowly appear from transparent")
            row.operator(LoadPresetOperator.bl_idname, text="Click get FadeIn preset").preset_name = "FadeIn"

            layout.separator()
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="Center Typewriter", icon='MESH_CUBE')
            box2 = box.box()
            col = box2.column()
            # col.label(text="a simple typewriter effect, character will appear one by one")
            row = col.row()
            row.label(text="Characters will appear one by one")
            row = col.row()
            row = row.split(factor=0.6)
            row.label(text="But also auto align to the center")
            row.operator(LoadPresetOperator.bl_idname, text="Click get CenterTypewriter preset").preset_name = "CenterTypewriter"

            layout.separator()
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="Miside", icon='MESH_CUBE')
            box2 = box.box()
            col = box2.column()
            # col.label(text="a simple typewriter effect, character will appear one by one")
            row = col.row()
            row.label(text="Effect inspired by the video game 'MiSide'")
            row = col.row()
            row.label(text="Issue may occur when Blender is lower than 4.3 due to API changes in Geometry Nodes")
            row = col.row()
            row = row.split(factor=0.6)
            row.label(text="You need to add extra time to view all effects")
            row.operator(LoadPresetOperator.bl_idname, text="Click get Miside preset").preset_name = "MiSide"

            layout.separator()
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="Dialog Bar", icon='MESH_CUBE')
            box2 = box.box()
            col = box2.column()
            # col.label(text="a simple typewriter effect, character will appear one by one")
            row = col.row()
            row.label(text="Dialog Bar similar to classic RPG games")
            row = col.row()
            row = row.split(factor=0.6)
            row.label(text="the \"Dialog Text\" is the correct object")
            row.operator(LoadPresetOperator.bl_idname, text="Click get Dialog_Box preset").preset_name = "Dialog_Box"

            layout.separator()
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="CardShake", icon='MESH_CUBE')
            box2 = box.box()
            col = box2.column()
            # col.label(text="a simple typewriter effect, character will appear one by one")
            row = col.row()
            row.label(text="Shake cards on the table")
            row = col.row()
            row.label(text="Issue may occur when Blender is lower than 4.3 due to API changes in Geometry Nodes")
            row = col.row()
            row = row.split(factor=0.6)
            row.label(text="Fancy animation done in Geometry Nodes")
            row.operator(LoadPresetOperator.bl_idname, text="Click get CardShake preset").preset_name = "CardShake"

            # layout.separator()
            # row = layout.row()
            # left_col = row.column()
            # left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            # left_col.label(text="")
            # box = row.box()
            # box.label(text="Rigidbody", icon='MESH_CUBE')
            # box2 = box.box()
            # col = box2.column()
            # # col.label(text="a simple typewriter effect, character will appear one by one")
            # row = col.row()
            # row.label(text="Add rigidbody Effect to the Character")
            # row = col.row()
            # row.label(text="As you can see, the text is not the parent object, Mesh Collider is!")
            # row = col.row()
            # row = row.split(factor=0.6)
            # row.label(text="It just work!")
            # row.operator(LoadPresetOperator.bl_idname, text="Click get Rigidbody preset").preset_name = "Rigidbody"

            layout.separator()
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="HTML_Example", icon='MESH_CUBE')
            box2 = box.box()
            col = box2.column()
            # col.label(text="a simple typewriter effect, character will appear one by one")
            # row = col.row()
            # row.label(text="You can use this test custom HTML property")
            row = col.row()
            row.label(text="Try this: \"my mind is racing with <shake><color = #FF2F2F>endless fears</color></shake>\"")
            row = col.row()
            row = row.split(factor=0.6)
            row.label(text="You can use this test custom HTML property")
            row.operator(LoadPresetOperator.bl_idname, text="Click get HTML_Example preset").preset_name = "HTML_Example"


@reg_order(3)
class CustomStyle(BasePanel, bpy.types.Panel):
    bl_label = "How To Make Char Template"
    bl_idname = "SCENE_PT_custom_style"
    bl_parent_id = "SCENE_PT_tutorial"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context: bpy.types.Context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        language = bpy.app.translations.locale
        if language == "zh_CN" or language == "zh_HANS":
            layout = self.layout

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="每一个字符都是一个单独的物体", icon='MESH_CUBE')
            box2 = box.box()
            col = box2.column()
            col.label(text="这个插件的工作原理是这样的:")
            col.label(icon="EVENT_A",text="插件会为文本段落中的每个字符按照时间创建一个独立的字符物体。")
            col.label(icon="EVENT_B",text="字符模板一般来说是一个文本物体，插件会自动将这个字符物体的内容设置为文本段落中的内容。")
            col.label(icon="EVENT_C",text="如果字符模板拥有子物体，那么这些子物体也会被自动创建。")
            col.label(icon="EVENT_D",text="会自动为字符模板及其子物体添加额外的属性数据接口，这些接口可以被几何节点与着色器节点使用")

            box2 = box.box()
            col = box2.column()
            col.label(icon='WARNING_LARGE', text="你可以发挥想象力为你的文字物体添加各种各样的组件与子物体！")
            # row = col.row()
            # row = row.split(factor=0.6)
            # row.label(text="这里有一个准备好了的文字描边的例程，带有两个子物体，试试看吧")
            # row.operator(LoadPresetOperator.bl_idname, text="点击获取文本描边例程").preset_name = "asd"


            layout.separator()
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="使用几何节点制作动画", icon='GEOMETRY_NODES')
            box.label(text="你可以把几何节点添加到文字模板上，以及文字模板上的子物体上，来制作动画效果")
            box.label(text="本插件提供的属性数据接口，接口详情请参考下方的[属性数据接口]，要想在几何节点中获取它们，请参考以下的操作流程")
            box.label(icon="EVENT_NDOF_BUTTON_1",text="进入几何节点编辑器，找到右侧的[群组]面板(如果你找不到，可以试着按下N键)")
            box.label(icon="EVENT_NDOF_BUTTON_2",text="在[群组]面板中，找到[数组接口]面板，点击[新建条目]添加一个新的输入接口")
            box.label(icon="EVENT_NDOF_BUTTON_3",text="将刚刚创建的接口的名称修改为你打算获取的属性名称，比如“enter”,“idx”等...")

            layout.separator()
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="使用着色器节点制作动画", icon='NODE_MATERIAL')
            box.label(text="你可以把着色器节点添加到文字模板上，以及文字模板上的子物体上，来制作动画效果")
            box.label(text="本插件提供的属性数据接口，接口详情请参考下方的[属性数据接口]，要想在着色器节点中获取它们，请参考以下的操作流程")
            box.label(icon="EVENT_NDOF_BUTTON_1",text="进入着色器节点编辑器，创建一个新的属性节点(添加->输入->属性)")
            box.label(icon="EVENT_NDOF_BUTTON_2",text="将属性节点中的名称修改为你打算获取的属性名称，比如“enter”,“idx”等...类型修改为[物体]")
        else:
            layout = self.layout

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # Set fixed width (in UI units)
            left_col.label(text="")
            box = row.box()
            box.label(text="Each Character is an Individual Object", icon='MESH_CUBE')
            box2 = box.box()
            col = box2.column()
            col.label(text="Here's how this addon works:")
            col.label(icon="EVENT_A",text="The addon creates an independent character object for each character in the text paragraph based on timing.")
            col.label(icon="EVENT_B",text="The character template is typically a text object, and the addon will automatically set its content to match the text paragraph.")
            col.label(icon="EVENT_C",text="If the character template has child objects, these will also be automatically created.")
            col.label(icon="EVENT_D",text="Additional property data interfaces are automatically added to the character template and its child objects, which can be used by geometry nodes and shader nodes")

            box2 = box.box()
            col = box2.column()
            col.label(icon='WARNING_LARGE', text="You can use your imagination to add various components and child objects to your text objects!")

            layout.separator()
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # Set fixed width (in UI units)
            left_col.label(text="")
            box = row.box()
            box.label(text="Creating Animations with Geometry Nodes", icon='GEOMETRY_NODES')
            box.label(text="You can add geometry nodes to the text template and its child objects to create animation effects")
            box.label(text="For the additional data interfaces provided by this addon, see [Property Data Interface] below. To access them in geometry nodes, follow these steps:")
            box.label(icon="EVENT_NDOF_BUTTON_1",text="Enter the geometry node editor, find the [Group] panel on the right (if not visible, press N key)")
            box.label(icon="EVENT_NDOF_BUTTON_2",text="In the [Group] panel, find the [Input] panel, click [New Item] to add a new input interface")
            box.label(icon="EVENT_NDOF_BUTTON_3",text="Change the name of the newly created interface to the property name you want to access, such as 'enter', 'idx', etc...")

            layout.separator()
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # Set fixed width (in UI units)
            left_col.label(text="")
            box = row.box()
            box.label(text="Creating Animations with Shader Nodes", icon='NODE_MATERIAL')
            box.label(text="You can add shader nodes to the text template and its child objects to create animation effects")
            box.label(text="For the additional data interfaces provided by this addon, see [Property Data Interface] below. To access them in shader nodes, follow these steps:")
            box.label(icon="EVENT_NDOF_BUTTON_1",text="Enter the shader node editor, create a new attribute node (Add->Input->Attribute)")
            box.label(icon="EVENT_NDOF_BUTTON_2",text="Change the name in the attribute node to the property name you want to access, such as 'enter', 'idx', etc... and set type to [Object]")


@reg_order(4)
class ExtraDataInterface(BasePanel, bpy.types.Panel):
    bl_label = "Property Data Interface"
    bl_idname = "SCENE_PT_extra_data_interface"
    bl_parent_id = "SCENE_PT_tutorial"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context: bpy.types.Context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        layout = self.layout
        language = bpy.app.translations.locale
        if language == "zh_CN" or language == "zh_HANS":    
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="这里有一些固定的额外的数据接口，可以在几何节点和着色器节点中按照名称使用它们", icon='CONSOLE')
            col = box.column()

            box2 = col.box()
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="enter")
            row.label(text="|  当前时间与文本段落开始时间的差值")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="exit")
            row.label(text="|  当前时间与文本段落结束时间的差值")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="extra")
            row.label(text="|  文本段落的额外时间")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="char")
            row.label(text="|  当前字符")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="order")
            row.label(text="|  当前句子在所有句子中的顺序")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="span")
            row.label(text="|  文本段落持续时间")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="idx")
            row.label(text="|  当前字符在文本段落中的索引")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="ridx")
            row.label(text="|  当前字符在文本段落中的反向索引")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="i_ratio")
            row.label(text="|  当前字符在文本段落中的索引比值")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="count")
            row.label(text="|  文本段落中的字符总数")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="width")
            row.label(text="|  当前行中的所有字符的宽度总和")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="run")
            row.label(text="|  当前字符在当前行中的X坐标位置")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="col")
            row.label(text="|  当前字符在文本段落中的列号")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="row")
            row.label(text="|  当前字符在文本段落中的行号")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="cols")
            row.label(text="|  当前行的总列数")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="rows")
            row.label(text="|  文本的总行数")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="rand")
            row.label(text="|  每个字符唯一的哈希随机数0~1")
        else:
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # Set fixed width (in UI units)
            left_col.label(text="")
            box = row.box()
            box.label(text="Here are some fixed additional data interfaces that can be used by name in geometry nodes and shader nodes", icon='CONSOLE')
            col = box.column()

            box2 = col.box()
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="enter")
            row.label(text="|  Difference between current time and paragraph start time")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="exit")
            row.label(text="|  Difference between current time and paragraph end time")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="extra")
            row.label(text="|  Extra time for the text paragraph")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="char")
            row.label(text="|  Current character")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="order")
            row.label(text="|  Order of current sentence among all sentences")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="span")
            row.label(text="|  Duration of text paragraph")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="idx")
            row.label(text="|  Index of current character in text paragraph")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="ridx")
            row.label(text="|  Reverse index of current character in text paragraph")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="i_ratio")
            row.label(text="|  Index ratio of current character in text paragraph")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="count")
            row.label(text="|  Total number of characters in text paragraph")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="width")
            row.label(text="|  Sum of widths of all characters in current line")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="run")
            row.label(text="|  X-coordinate position of current character in current line")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="col")
            row.label(text="|  Column number of current character in text paragraph")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="row")
            row.label(text="|  Row number of current character in text paragraph")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="cols")
            row.label(text="|  Total number of columns in current line")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="rows")
            row.label(text="|  Total number of rows in text")
            row = box2.row()
            row = row.split(factor=0.4)
            row.label(text="rand")
            row.label(text="|  Unique hash random number 0~1 for each character")


@reg_order(5)
class AdvanceInterface(BasePanel, bpy.types.Panel):
    bl_label = "Advanced Interface"
    bl_idname = "SCENE_PT_advance_interface"
    bl_parent_id = "SCENE_PT_tutorial"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context: bpy.types.Context):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        layout = self.layout
        language = bpy.app.translations.locale
        if language == "zh_CN" or language == "zh_HANS":
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="在文本段落中HTML标签的属性也会被添加到字符物体上，使用方式与[属性数据接口]相同", icon='CON_TRANSFORM_CACHE')
            col = box.column()

            box2 = col.box()
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="<scale = 1.45>hello world</scale>")
            row.label(text="| 一个名为\"scale\"的浮点属性，值为1.45")
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="<xyz = (1.3,-0.5,0)>hello world</xyz>")
            row.label(text="| 一个名为\"xyz\"的矢量属性，值为(1.3,-0.5,0)")
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="<color = #FF00FF>hello world</color>")
            row.label(text="| 一个名为\"color\"的矢量属性，值为(1,0,1)")
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="<is_enable = false>hello world</is_enable>")
            row.label(text="| 一个名为\"is_enable\"的布尔属性，值为False")
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="<border>hello world</border>")
            row.label(text="| 一个名为\"border\"的布尔属性，值为True")
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="<awwdff = \"what\">hello world</awwdff>")
            row.label(text="| 一个名为\"awwdff\"的字符串属性，值为\"what\"")

            col.separator()

            box2 = col.box()
            row = box2.row()
            row.label(text="自定义属性的名字可以随意命名，因为属性的数据类型是根据等号右边的内容自动推断的")

            col.separator()

            box2 = col.box()
            row = box2.row()
            row = row.split(factor=0.6)
            row.label(text="你可以使用这个例程与下面的这段文字来试试这个功能")
            row.operator(LoadPresetOperator.bl_idname, text="点击获取html标签测试例程").preset_name = "HTML_Example"
            box2.label(text="my mind is racing with <shake><col = #FF0000>endless fears</col></shake>")

            layout.separator()

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="这里有一些魔法名称，允许你进行一些几何节点难以触及的操作", icon='EXPERIMENTAL')
            col = box.column()

            box2 = col.box()
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="<Font = \"Arial Black\">hello world</Font>")
            row.label(text="| 这个标签会自动将字符的字体覆盖为\"Arial Black\"")
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="<Size = 1.33>hello world</Size>")
            row.label(text="| 这个标签会自动将字符的大小缩放为原来的1.33倍")

            layout.separator()

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # 设置固定宽度（以UI单位为单位）
            left_col.label(text="")
            box = row.box()
            box.label(text="你可以在文本中连续插入两个'|'符号即\"||\"来手动创建一个换行信号", icon='EXPERIMENTAL')
            col = box.column()

            box2 = col.box()
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="hello ||world")
            row.label(text="| hello会在第1行，world会在第2行")
        else:
            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # Set fixed width (in UI units)
            left_col.label(text="")
            box = row.box()
            box.label(text="HTML tag attributes in text paragraphs are also added to character objects, used the same way as [Extra Data Interface]", icon='CON_TRANSFORM_CACHE')
            col = box.column()

            box2 = col.box()
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="<scale = 1.45>hello world</scale>")
            row.label(text="| A float attribute named \"scale\" with value 1.45")
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="<xyz = (1.3,-0.5,0)>hello world</xyz>")
            row.label(text="| A vector attribute named \"xyz\" with value (1.3,-0.5,0)")
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="<color = #FF00FF>hello world</color>")
            row.label(text="| A vector attribute named \"color\" with value (1,0,1)")
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="<is_enable = false>hello world</is_enable>")
            row.label(text="| A boolean attribute named \"is_enable\" with value False")
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="<border>hello world</border>")
            row.label(text="| A boolean attribute named \"border\" with value True")
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="<awwdff = \"what\">hello world</awwdff>")
            row.label(text="| A string attribute named \"awwdff\" with value \"what\"")

            col.separator()

            box2 = col.box()
            row = box2.row()
            row.label(text="Custom attribute names can be named arbitrarily, as the data type is automatically inferred from the content on the right side of the equal sign")

            col.separator()

            box2 = col.box()
            row = box2.row()
            row = row.split(factor=0.6)
            row.label(text="You can use this example and the text below to try this feature")
            row.operator(LoadPresetOperator.bl_idname, text="Click to get HTML tag test example").preset_name = "HTML_Example"
            box2.label(text="my mind is racing with <shake><color = #FF0000>endless fears</color></shake>")

            layout.separator()

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # Set fixed width (in UI units)
            left_col.label(text="")
            box = row.box()
            box.label(text="Here are some magic names that allow you to perform operations that are difficult to achieve with geometry nodes", icon='EXPERIMENTAL')
            col = box.column()

            box2 = col.box()
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="<Font = \"Arial Black\">hello world</Font>")
            row.label(text="| This tag will automatically override the character's font to \"Arial Black\"")
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="<Size = 1.33>hello world</Size>")
            row.label(text="| This tag will automatically scale the character's size to 1.33 times the original")

            layout.separator()

            row = layout.row()
            left_col = row.column()
            left_col.scale_x = 0.15  # Set fixed width (in UI units)
            left_col.label(text="")
            box = row.box()
            box.label(text="You can insert two consecutive '|' symbols, i.e., \"||\" in the text to manually create a line break signal", icon='EXPERIMENTAL')
            col = box.column()

            box2 = col.box()
            row = box2.row()
            row = row.split(factor=0.40)
            row.label(text="hello ||world")
            row.label(text="| hello will be on line 1, world will be on line 2")

        