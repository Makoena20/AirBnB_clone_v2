#!/usr/bin/python3
"""
Module for the command interpreter.
"""

import cmd
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import shlex

class HBNBCommand(cmd.Cmd):
    """Command interpreter class."""
    prompt = '(hbnb) '
    file = None

    def do_create(self, arg):
        """Create a new instance of BaseModel, save it to JSON file."""
        args = shlex.split(arg)
        if len(args) < 1:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in FileStorage.classes:
            print("** class doesn't exist **")
            return
        params = {}
        for arg in args[1:]:
            if '=' in arg:
                key, value = arg.split('=')
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace('_', ' ').replace('\\"', '"')
                elif '.' in value:
                    try:
                        value = float(value)
                    except ValueError:
                        continue
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                params[key] = value
        new_instance = FileStorage.classes[class_name](**params)
        new_instance.save()
        print(new_instance.id)

    def do_EOF(self, line):
        """End of file"""
        print()
        return True

    def emptyline(self):
        """Handle empty line."""
        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()

