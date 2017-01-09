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

import setuptools

setuptools.setup(
    name="firefox-flatpak-oracle-jre-installer",
    summary="Graphical instller for Oracle JRE, made for Firefox flatpak",
    author="Michal Rostecki",
    author_email="michal@kinvolk.io",
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ],
    packages=[
        "ff_oracle_jre_installer"
    ],
    entry_points={
        "console_scripts": [
            "ff-oracle-jre-installer = ff_oracle_jre_installer.app:main"
        ]
    }
)
