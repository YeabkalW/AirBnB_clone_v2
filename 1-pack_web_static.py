#!/usr/bin/python3
"""Fabric script to generate .tgz archive"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates .tgz archive from the contents of the web_static folder"""
    local("mkdir -p versions")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)
    result = local("tar -cvzf {} web_static".format(archive_path))

    if result.succeeded:
        print("web_static packed: {} -> {} Bytes".format(archive_path, result))
        return archive_path
    else:
        return None
