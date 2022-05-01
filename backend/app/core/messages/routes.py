"""
The roseguarden project

Copyright (C) 2018-2020  Marcus Drobisch,

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__authors__ = ["Marcus Drobisch"]
__contact__ = "roseguarden@fabba.space"
__credits__ = []
__license__ = "GPLv3"

from core.messages import messages_bp
from core.messages import messageManager
from flask_jwt_extended import jwt_optional
from jinja2 import Template


@messages_bp.route('/api/v1/message/<int:id>', methods=['GET'])
@jwt_optional
def message(id):

    message = messageManager.message.query.filter_by(id=id).first()

    # Get File Content in String
    jinja2_template_string = open(message.template_path, 'r').read()

    # Create Template Object
    template = Template(jinja2_template_string)

    content = template.render(**message.data)
    return content, 200
