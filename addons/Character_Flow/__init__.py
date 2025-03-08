import bpy
import time

from .config import __addon_name__
from .i18n.dictionary import dictionary
from ...common.class_loader import auto_load
from ...common.class_loader.auto_load import add_properties, remove_properties
from ...common.i18n.dictionary import common_dictionary
from ...common.i18n.i18n import load_dictionary
from .operators.Struct import textfrag, StringFlow
from bpy.app.handlers import persistent

# Add-on info
bl_info = {
    "name": "Character Flow",
    "author": "ycutr",
    "blender": (4, 3, 2),
    "version": (0, 1, 1),
    "description": "Procedure Character&Text Animation Tool",
    "warning": "",
    "doc_url": "https://github.com/3c0tr/CharacterFlow",
    "support": "COMMUNITY",
    "category": "Animation"
}

_addon_properties = {
    bpy.types.Scene: {
        "CharacterFlow_list": bpy.props.CollectionProperty(type=StringFlow),
        "CharacterFlow_index": bpy.props.IntProperty(default=0),
    }
}


# You may declare properties like following, framework will automatically add and remove them.
# Do not define your own property group class in the __init__.py file. Define it in a separate file and import it here.
# 注意不要在__init__.py文件中自定义PropertyGroup类。请在单独的文件中定义它们并在此处导入。
# _addon_properties = {
#     bpy.types.Scene: {
#         "property_name": bpy.props.StringProperty(name="property_name"),
#     },
# }


@persistent
def init_addon(dummy = None):
    print(str(time.time()) + " callback function is called.")
    if any(handler.__name__ == 'UpdateAll' for handler in bpy.app.handlers.frame_change_post):
        return None
    else:
        try:
            bpy.ops.object.example_ops()
        except:
            print("error")
            pass
        return 1.0


def register():
    # Register classes
    auto_load.init()
    auto_load.register()
    add_properties(_addon_properties)
    # Internationalization
    load_dictionary(dictionary)
    bpy.app.translations.register(__addon_name__, common_dictionary)
    
    # 添加初始化处理器
    bpy.app.handlers.load_post.append(init_addon)

    bpy.app.timers.register(init_addon, first_interval=1.0)

    print("{} addon is installed.".format(__addon_name__))




def unregister():
    # Internationalization
    bpy.app.translations.unregister(__addon_name__)
    
    # 移除初始化处理器
    bpy.app.handlers.load_post.remove(init_addon)

    try:
        for handler in bpy.app.handlers.frame_change_post:
            print(f"- {handler.__name__}")
            if handler.__name__ == "UpdateAll":
                bpy.app.handlers.frame_change_post.remove(handler)
                print("handler is removed")
    except:
        print("remove error")
        pass
    
    auto_load.unregister()
    remove_properties(_addon_properties)
    print("{} addon is uninstalled.".format(__addon_name__))


