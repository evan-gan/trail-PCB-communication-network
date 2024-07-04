import lib.utils as utils
import uasyncio


class vCanvas:
    def __init__(self, width, height, renderCb):
        self.display_width = width
        self.display_height = height
        self.renderCb = renderCb
        self.components = {}

        # Dirty = Has the component been changed since last render?
        # Analogy:
        # Think of it like a whiteboard. If someone makes a small change, you don't erase and redraw the entire board immediately.
        # You might wait until a few changes have accumulated(the board gets "dirty") before cleaning it and redrawing everything.
        self.dirty = False

    def remove(self, key):
        if key in self.components:
            del self.components[key]
            self._trigger_render()

    def update(self, key, data):
        self.components[key] = data
        self._trigger_render()

    def _trigger_render(self):
        if not self.dirty:
            self.dirty = True
            uasyncio.create_task(self._render())

    async def _render(self):
        await uasyncio.sleep(0)  # Yield to allow other tasks to run
        if self.dirty:
            self.renderCb(self.components)
            self.dirty = False


class UIComponent:
    def __init__(self, container, **kwargs):
        self.key = utils.random_string(8)
        self.container = container
        self.children = {}
        self.properties = {
            "class_name": self.__class__.__name__,
            "x": 0, "y": 0, "ax": 0, "ay": 0,
            "visible": True,
            "position_type": "offset"
        }
        self.update_properties(kwargs)

    def __getattr__(self, name):
        if name in self.properties:
            return self.properties[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name in ['key', 'container', 'children', 'properties']:
            super().__setattr__(name, value)
        else:
            self.update_property(name, value)

    def update_property(self, name, value):
        if self.properties.get(name) != value:
            self.properties[name] = value
            self.update_container()

    def update_properties(self, new_properties):
        changed = False
        for key, value in new_properties.items():
            if self.properties.get(key) != value:
                self.properties[key] = value
                changed = True
        if changed:
            self.update_container()

    def update(self, key, data):
        if self.children.get(key) != data:
            self.children[key] = data
            self.update_container()

    def destroy(self):
        self.children = {}
        self.container.remove(self.key)

    def update_container(self):
        data = self.properties.copy()
        data["position"] = {
            "x": data.pop("x"),
            "y": data.pop("y"),
            "ax": data.pop("ax"),
            "ay": data.pop("ay"),
            "type": data.pop("position_type"),
        }
        if "width" in data and "height" in data:
            data["size"] = {
                "x": data.pop("width"),
                "y": data.pop("height"),
                "type": data.pop("size_type", "offset"),
            }
        if self.children:
            data["children"] = self.children
        self.container.update(self.key, data)


class Group(UIComponent):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)


class Frame(UIComponent):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        self.properties.update({
            "size_type": "offset",
            "width": 10,
            "height": 10,
            "fill": False
        })
        self.update_properties(kwargs)


class TextLabel(UIComponent):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        self.properties.update({
            "text": "",
            "text_size": 1,
            "text_color": 1
        })
        self.update_properties(kwargs)


class TextBox(UIComponent):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        self.properties.update({
            "text": "",
            "editable": True,
            "text_size": 1,
            "text_color": 1,
            "onEnter": None
        })
        self.update_properties(kwargs)
