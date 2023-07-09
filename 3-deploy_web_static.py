#!/usr/bin/python3
'''
Fabric script for archiving and distributing files to web servers using the
deploy() function.
'''

import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once


env.hosts = ['54.236.26.181', '52.91.117.65']


@runs_once
def do_pack():
    """
    Archives the static files.

    Returns:
        str: The path of the created archive, or None if archiving fails.
    """
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )
    try:
        print("Creating archive: {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        archive_size = os.stat(output).st_size
        print("Archive created: {} -> {} Bytes".format(output, archive_size))
    except Exception:
        output = None
    return output


def do_deploy(archive_path):
    """
    Deploys the static files to the host servers.

    Args:
        archive_path (str): The path to the archived static files.

    Returns:
        bool: True if deployment succeeds, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version is now LIVE!')
        success = True
    except Exception:
        success = False
    return success


def deploy():
    """
    Archives and deploys the static files to the host servers.

    Returns:
        bool: True if deployment succeeds, False otherwise.
    """
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False
