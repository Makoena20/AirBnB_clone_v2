#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive from the contents of the web_static folder
"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns the archive path if the archive has been correctly generated, otherwise returns None.
    """
    try:
        # Create versions directory if it doesn't exist
        if not os.path.exists("versions"):
            os.makedirs("versions")

        # Create the archive name
        now = datetime.now()
        archive_name = "versions/web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))

        # Create the archive
        local("tar -cvzf {} web_static".format(archive_name))

        # Check if the archive was created successfully
        if os.path.exists(archive_name):
            return archive_name
        else:
            return None
    except Exception as e:
        return None

