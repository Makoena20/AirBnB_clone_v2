#!/usr/bin/python3
"""
Module for file storage class.
"""

import json
from os import path
from models.base_model import BaseModel

class FileStorage:
    """File storage class."""
    __file_path = "file.json"
    __objects = {}
    classes = {
        'BaseModel': BaseModel
    }

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects the obj with key <obj class name>.id."""
        key = obj.__class__.__name__ + '.' + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        obj_dict = {}
        for key, value in FileStorage.__objects.items():
            obj_dict[key] = value.to_dict()
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as file:
            json.dump(obj_dict, file)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as file:
                obj_dict = json.load(file)
            for key, value in obj_dict.items():
                class_name, obj_id = key.split('.')
                self.__objects[key] = FileStorage.classes[class_name](**value)
        except FileNotFoundError:
            pass

