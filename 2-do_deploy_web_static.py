#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers,
   using the function do_deploy
"""

from fabric.api import local, env, put, run
from datetime import datetime
import os

env.hosts = ['52.55.249.213', '54.157.32.137']
env.user = 'ubuntu'


def do_pack():
    """Generate a .tgz archive from the contents of the web_static folder."""
    try:
        if not os.path.exists("versions"):
            local("mkdir -p versions")
        date_format = "%Y%m%d%H%M%S"
        file_name = "web_static_" + datetime.now().strftime(date_format) + ".tgz"
        local("tar -cvzf versions/{} web_static".format(file_name))
        return "versions/{}".format(file_name)
    except Exception:
        return None


def do_deploy(archive_path):
    """Distribute an archive to your web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        file_no_extension = file_name.split(".")[0]
        path_no_extension = "/data/web_static/releases/" + file_no_extension

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path_no_extension))
        run("tar -xzf /tmp/{} -C {}/".format(file_name, path_no_extension))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}".format(path_no_extension, path_no_extension))
        run("rm -rf {}/web_static".format(path_no_extension))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path_no_extension))
        print("New version deployed!")
        return True
    except Exception:
        return False

