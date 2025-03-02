import bpy


class textfrag(bpy.types.PropertyGroup):
    text: bpy.props.StringProperty(name="")
    is_active: bpy.props.BoolProperty(name="is_active")
    enter_time: bpy.props.FloatProperty(name="enter_time", subtype="TIME")
    exit_time: bpy.props.FloatProperty(name="exit_time", subtype="TIME")
    extra_time: bpy.props.FloatProperty(name="extra_time", subtype="TIME")
    collection: bpy.props.PointerProperty(name="collection", type=bpy.types.Collection)
    

class StringText:
    text : str = ""
    enter_time : float = 0.0
    exit_time : float = 0.0
    extra_time : float = 0.0

    def __init__(self, text, enter_time, exit_time, extra_time):
        self.text = text
        self.enter_time = enter_time
        self.exit_time = exit_time
        self.extra_time = extra_time

class CharObject:
    blender_object : bpy.types.Object = None
    char : str = ""
    order: int = 0
    metrics : dict = {}
    custom_properties : dict = {}

    run : float = 0.0

    char_index : int = 0          # 所有字符的索引
    text_count : int = 0          # 所有字符的数量
    text_width : float = 0.0      # 所有字符的宽度
    
    col : int = 0                 # 当前字符的列
    col_count : int = 0           # 所有字符的列数
    col_width : float = 0.0       # 当前字符的列宽

    row : int = 0                 # 当前字符的行
    row_count : int = 0           # 所有字符的行数

    enter_time : float = 0.0      # 当前字符的进入时间
    exit_time : float = 0.0       # 当前字符的退出时间
    extra_time : float = 0.0      # 当前字符的额外时间

    def __init__(self):
        pass


    # def __init__(self, blender_object, char, metrics, custom_properties, char_index, text_count, text_width, enter_time, exit_time, extra_time):
    #     self.blender_object = blender_object
    #     self.char = char
    #     self.metrics = metrics
    #     self.custom_properties = custom_properties
    #     self.char_index = char_index
    #     self.text_count = text_count
    #     self.text_width = text_width
    #     self.enter_time = enter_time
    #     self.exit_time = exit_time
    #     self.extra_time = extra_time

class StringFlow(bpy.types.PropertyGroup):
    text_list: bpy.props.CollectionProperty(type=textfrag)
    textfrag_index: bpy.props.IntProperty(name="textfrag_index")
    is_enabled: bpy.props.BoolProperty(name="is_enabled", default=True)
    anchor: bpy.props.PointerProperty(name="anchor",type=bpy.types.Object)
    is_follow_anchor: bpy.props.BoolProperty(name="is_follow_anchor", default=True)
    metrics_font: bpy.props.PointerProperty(
        name="Metrics Font",
        type=bpy.types.VectorFont,
        description="用于获取文字度量信息的字体"
    )
    style: bpy.props.PointerProperty(name="style",type=bpy.types.Object)
    text_gap_scale: bpy.props.FloatProperty(name="text_gap_scale", default=1.0)
    row_gap_scale: bpy.props.FloatProperty(name="row_gap_scale", default=1.0)
    Auto_Arrange: bpy.props.BoolProperty(name="Auto_Arrange", default=True)
    use_global_extra_time: bpy.props.BoolProperty(name="use_global_extra_time", default=True)
    extra_time: bpy.props.FloatProperty(name="extra_time", default=0.0)
    use_global_offset_time: bpy.props.BoolProperty(name="use_global_offset_time", default=True)
    offset_time: bpy.props.FloatProperty(name="offset_time", default=0.0)
    use_switch_line: bpy.props.BoolProperty(name="use_switch_line", default=False)
    switch_line_scale: bpy.props.FloatProperty(name="switch_line_scale", default=40.0)

    srt_file_path: bpy.props.StringProperty(name="srt_file_path", default="", subtype="FILE_PATH")
    is_srt_use_html: bpy.props.BoolProperty(name="is_srt_use_html", default=False)
    is_srt_use_line_switch: bpy.props.BoolProperty(name="is_srt_use_line_switch", default=True)
    srt_time_offset: bpy.props.FloatProperty(name="srt_time_offset", default=0.0, subtype="TIME")
    # is_String_follow_object: bpy.props.BoolProperty(name="is_String_follow_object")
    # String_follow_object: bpy.props.PointerProperty(type=bpy.types.Object)