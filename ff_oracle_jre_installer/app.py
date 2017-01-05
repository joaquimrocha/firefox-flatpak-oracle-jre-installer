# Copyright © 2016 Kinvolk GmbH
#
# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import sys
import tarfile
import urllib
import urllib.request
import ssl

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import progressbar


ORACLE_JRE_URL = ("http://download.oracle.com/otn-pub/java/jdk/8u112-b15/"
                  "jre-8u112-linux-x64.tar.gz")
ORACLE_JRE_FILENAME = "jre-8u112-linux-x64.tar.gz"
ORACLE_JRE_TARBALL_DIR = "jre1.8.0_112"
ORACLE_LICENSE_COOKIE = ("gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; "
                         "oraclelicense=accept-securebackup-cookie")


def check_connectivity():
    nm_client = NMClient.Client.new()
    connectivity = nm_client.get_connectivity()
    state = nm_client.get_state()

    return (connectivity == NetworkManager.ConnectivityState.FULL and
            state == NetworkManager.State.CONNECTED_GLOBAL)


def download():
    f = open(ORACLE_JRE_FILENAME, "wb")

    req = urllib.request.Request(ORACLE_JRE_URL, headers={
        "Cookie": ORACLE_LICENSE_COOKIE
    })
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        resp = urllib.request.urlopen(req, context=ctx)
    except urllib.URLError:
        logging.error("No internet connection")
        sys.exit(1)
    total_size = int(resp.info().get("Content-Length"))
    already_downloaded = 0

    widgets = [ORACLE_JRE_FILENAME,
               progressbar.Percentage(),
               ' ',
               progressbar.Bar(),
               ' ',
               progressbar.ETA(),
               ' ',
               progressbar.FileTransferSpeed()]
    pbar = progressbar.ProgressBar(widgets=widgets)
    pbar.maxval = total_size
    pbar.start()

    while True:
        buf = resp.read(1024)

        if not buf:
            break

        f.write(buf)
        f.flush()

        already_downloaded += len(buf)
        fraction = (already_downloaded / total_size) * 100
        pbar.update(fraction)

    pbar.finish()
    f.close()


def install():
    destdir = os.path.expanduser("~/.flatpak_extras/firefox")
    try:
        os.makedirs(destdir)
    except FileExistsError:
        pass

    tarball = tarfile.open(ORACLE_JRE_FILENAME, 'r|gz')
    for directory in ['bin', 'lib', 'man', 'plugin']:
        member = os.path.join(ORACLE_JRE_TARBALL_DIR, directory)
        dest = os.path.join(destdir, directory)
        tarball.extract(member, path=dest)


def show_dialog():
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                               Gtk.ButtonsType.OK,
                               "Oracle JRE plugin installed")
    dialog.format_secondary_text(
        "Please restart Firefox to be able to browse websites with Java "
        "applets.")
    dialog.run()


def main():
    download()
    install()
    show_dialog()


if __name__ == '__main__':
    main()
