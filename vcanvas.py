"""
vCanvas.py - Virtual Canvas for UI Rendering

This module implements a virtual canvas system for efficient UI rendering in embedded systems.
It provides a framework for managing UI components, handling updates, and triggering renders
only when necessary.

Key concepts:
- vCanvas: The main class that manages the overall UI state and rendering process.
- UIComponent: Base class for all UI elements, handling property management and updates.
- Dirty flag: Used to track whether the UI needs redrawing, optimizing render calls.
- Asynchronous rendering: Utilizes uasyncio for non-blocking UI updates.

The system supports various UI components like Frame, TextLabel, TextBox, and Group, allowing
for flexible UI construction. Properties of these components can be updated dynamically,
automatically triggering re-renders when necessary.

Usage:
1. Create a vCanvas instance with a render callback.
2. Create UI components and add them to the canvas.
3. Update component properties as needed; renders will be triggered automatically.

This system is designed to be efficient for embedded systems, minimizing unnecessary redraws
and allowing for responsive UI updates without blocking other operations.
"""

import lib.utils as utils
import uasyncio


class vCanvas:
    def __init__(self, width, height, renderCb):
        """
        Initialize the virtual canvas.

        :param width: Width of the display in pixels.
        :param height: Height of the display in pixels.
        :param renderCb: Callback function that handles the actual rendering on the physical display.
        """
        self.display_width = width
        self.display_height = height

        # This callback is called when it's time to update the physical display
        self.renderCb = renderCb

        # Dictionary to store all UI components, keyed by their unique identifiers
        self.components = {}

        # References to all active components
        self.componentsList = {}

        self.dirty = False  # Flag to indicate if the canvas needs redrawing

    def destroy(self, key):
        # def remove(self, key):
        """
        Remove a component from the canvas.

        :param key: Unique identifier of the component to remove.
        """
        # We can either do recursion to find the component and del it
        # or we can build a minimal tree of the components
        # then search the location like id1.id2.id3 then  we can del  it like
        # del self.components["id1"]["id2"]["id3"]
        # then we can trigger a render
        # self._trigger_render()

    def update(self, key, data):
        """
        Update a component's data on the canvas.

        :param key: Unique identifier of the component to update.
        :param data: New data for the component.
        """
        self.components[key] = data

        self._trigger_render()  # Mark canvas as dirty and schedule a render

    def _trigger_render(self):
        # def _trigger_render(self):
        """
        Schedule a render if one is not already pending.
        This method uses the dirty flag to prevent multiple render calls in quick succession.
        """
        if not self.dirty:
            self.dirty = True
            # Create an asynchronous task for rendering
            # uasyncio.create_task(self._render())
            self._render()

    def _render(self):
        # async def _render(self):
        """
        Asynchronous method to perform the actual render.
        This method yields control briefly to allow other tasks to run, then calls the render callback.
        """
        # await uasyncio.sleep(0)  # Yield control to allow other tasks to run
        if self.dirty:
            # Call the render callback with the current state of all components
            self.renderCb(self.components)
            self.dirty = False  # Mark the canvas as clean after rendering


class UIComponent:
    def __init__(self, container, **kwargs):
        """
        Initialize a UI component.

        :param container: The parent container (usually vCanvas) this component belongs to.
        :param kwargs: Initial property values for the component.
        """
        self.key = utils.random_string(
            8)  # Generate a unique key for this component

        self.container = container  # Reference to the parent container

        self.children = {}  # Dictionary to store child components if this is a container
        self.properties = {
            "class_name": self.__class__.__name__,
            "x": 0, "y": 0, "ax": 0, "ay": 0,
            "visible": True,
            "position_type": "offset"
        }

        # Set initial properties based on kwargs
        self.update_properties(kwargs)

    def __getattr__(self, name):
        """
        Allow attribute-style access to properties.

        :param name: Name of the attribute being accessed.
        :return: Value of the property if it exists.
        :raises AttributeError: If the property doesn't exist.
        """
        if name in self.properties:
            return self.properties[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """
        Handle property updates via attribute assignment.

        :param name: Name of the attribute being set.
        :param value: New value for the attribute.
        """
        if name in ['key', 'container', 'children', 'properties']:
            super().__setattr__(name, value)  # Use default behavior for these attributes
        else:
            # Treat other attributes as updateable properties
            self.update_property(name, value)

    def update_property(self, name, value):
        """
        Update a single property and trigger container update if changed.

        :param name: Name of the property to update.
        :param value: New value for the property.
        """

        if self.properties.get(name) != value:
            self.properties[name] = value
            self.update_container()  # Notify the container of the change

    def update_properties(self, new_properties):
        """
        Update multiple properties at once, triggering only one container update.

        :param new_properties: Dictionary of property names and their new values.
        """
        changed = False

        for key, value in new_properties.items():
            if self.properties.get(key) != value:
                self.properties[key] = value
                changed = True

        if changed:
            self.update_container()  # Notify the container of the changes

    def update(self, key, data):
        """
        Update a child component.

        :param key: Unique identifier of the child component.
        :param data: New data for the child component.
        """

        if self.children.get(key) != data:
            self.children[key] = data
            self.update_container()  # Notify the container of the change

    def destroy(self, key=None):
        """
        Remove this component from its container.
        """

        self.container.destroy(self.key if key is None else key)

    def update_container(self):
        """
        Prepare component data and update the container.
        This method is called whenever the component's state changes.
        """
        data = self.properties.copy()

        # Format position data
        data["position"] = {
            "x": data.pop("x"),
            "y": data.pop("y"),
            "ax": data.pop("ax"),
            "ay": data.pop("ay"),
            "type": data.pop("position_type"),
        }

        # Format size data if present
        if "width" in data and "height" in data:
            data["size"] = {
                "x": data.pop("width"),
                "y": data.pop("height"),
                "type": data.pop("size_type", "offset"),
            }

        # Include children if any
        if self.children:
            data["children"] = self.children

        # Update the container with the new data
        self.container.update(self.key, data)


class Group(UIComponent):
    """
    A Group is a basic container with no additional properties.
    It's used to logically group other components together.
    """

    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)


class Frame(UIComponent):
    def __init__(self, container, **kwargs):
        """
        Initialize a Frame component.

        :param container: The parent container this frame belongs to.
        :param kwargs: Additional properties for the frame.
        """
        super().__init__(container, **kwargs)

        self.properties.update({
            "size_type": "offset",
            "width": 10,
            "height": 10,
            "fill": False
        })

        # Apply any frame-specific properties passed in kwargs
        self.update_properties(kwargs)


class TextLabel(UIComponent):
    def __init__(self, container, **kwargs):
        """
        Initialize a TextLabel component.

        :param container: The parent container this label belongs to.
        :param kwargs: Additional properties for the text label.
        """
        super().__init__(container, **kwargs)

        self.properties.update({
            "text": "",
            "text_size": 1,
            "text_color": 1
        })

        # Apply any label-specific properties passed in kwargs
        self.update_properties(kwargs)


class TextBox(UIComponent):
    def __init__(self, container, **kwargs):
        """
        Initialize a TextBox component.

        :param container: The parent container this text box belongs to.
        :param kwargs: Additional properties for the text box.
        """
        super().__init__(container, **kwargs)

        self.properties.update({
            "text": "",
            "editable": True,
            "text_size": 1,
            "text_color": 1,
            "onEnter": None  # Callback function to be called when Enter is pressed
        })

        # Apply any text box-specific properties passed in kwargs
        self.update_properties(kwargs)


# - root
#    - group1
#        -label1
#         -label2
#         -group2
#            -label3
#             -label4
#     - group3
#         -label5
#         -label6
