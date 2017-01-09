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

# serial 8

AC_DEFUN([AC_PYTHON_REQUIREMENTS], [
	PYTHON_NAME=`basename $PYTHON`
	AC_MSG_CHECKING(for $PYTHON_NAME requirements)
	$PYTHON -c "import pkg_resources; f = open('requirements.txt', 'r'); pkg_resources.require(f.readlines()); f.close()"
	if test $? -eq 0; then
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
		AC_MSG_ERROR(failed to find all the $PYTHON_NAME requirements)
	fi
])
