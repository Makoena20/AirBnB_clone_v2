#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import env, run, local
from fabric.operations import put, sudo
from datetime import datetime
import os

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    number = int(number)
    if number < 2:
        number = 1
    else:
        number += 1

    archives = sorted(os.listdir("versions"))
    archives_to_keep = archives[-number:]

    with cd("/data/web_static/releases"):
        run("ls -t").split('\n')
        archives_releases = run("ls -t").split('\n')

    archives_releases = [archive.split()[-1] for archive in archives_releases]
    archives_releases_to_keep = archives_releases[:number]

    for archive in archives:
        if archive not in archives_to_keep:
            local("rm -f versions/{}".format(archive))

    for release in archives_releases:
        if release not in archives_releases_to_keep:
            sudo("rm -rf /data/web_static/releases/{}".format(release))

