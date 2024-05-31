#!/usr/bin/python3
"""Defines the FileStorage class."""

import json
from models.base_model import BaseModel


class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file to instances."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file."""
        serialized = {}
        for key, value in FileStorage.__objects.items():
            serialized[key] = value.to_dict()
        with open(FileStorage.__file_path, mode='w', encoding='utf-8') as file:
            json.dump(serialized, file)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        try:
            with open(FileStorage.__file_path, mode='r', encoding='utf-8') as file:
                serialized = json.load(file)
                for key, value in serialized.items():
                    class_name, obj_id = key.split('.')
                    obj_dict = value
                    obj = eval(class_name)(**obj_dict)
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass

    def close(self):
        """Calls reload() method for deserializing the JSON file to objects."""
        self.reload()

