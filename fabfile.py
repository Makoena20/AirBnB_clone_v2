#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that distributes an archive to your web servers.
"""

from fabric import task
import os

env_hosts = ['xx-web-01', 'xx-web-02']  # replace with your actual server IPs

@task
def do_deploy(c, archive_path):
    """
    Distributes an archive to the web servers.
    Args:
        c (Connection): The connection object to use for remote operations.
        archive_path (str): The path to the archive file.
    Returns:
        bool: True if all operations have been done correctly, otherwise False.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_file = archive_path.split("/")[-1]
        no_ext = archive_file.split(".")[0]
        release_dir = f"/data/web_static/releases/{no_ext}/"

        # Upload the archive to the /tmp/ directory of the web server
        c.put(archive_path, f"/tmp/{archive_file}")

        # Create the directory where the archive will be uncompressed
        c.run(f"mkdir -p {release_dir}")

        # Uncompress the archive to the folder
        c.run(f"tar -xzf /tmp/{archive_file} -C {release_dir}")

        # Delete the archive from the web server
        c.run(f"rm /tmp/{archive_file}")

        # Move the contents of the archive to the proper directory
        c.run(f"mv {release_dir}web_static/* {release_dir}")

        # Remove the now-empty directory
        c.run(f"rm -rf {release_dir}web_static")

        # Delete the symbolic link /data/web_static/current from the web server
        c.run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web server
        c.run(f"ln -s {release_dir} /data/web_static/current")

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

