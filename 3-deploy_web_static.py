#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py) that creates and distributes an archive to your web servers
"""
from fabric.api import env, local, put, run
from os import path
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder
    """
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        file_path = "versions/web_static_{}.tgz".format(now)
        local("tar -cvzf {} web_static".format(file_path))
        return file_path
    except:
        return None


def do_deploy(archive_path):
    """
    Distribute an archive to your web servers
    """
    if not path.exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        file_no_ext = file_name.split(".")[0]
        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}/".format(file_no_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(file_name, file_no_ext))
        run("rm /tmp/{}".format(file_name))
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/"
            .format(file_no_ext, file_no_ext))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(file_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ "
            "/data/web_static/current"
            .format(file_no_ext))
        return True
    except:
        return False


def deploy():
    """
    Deploy new version on servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()

