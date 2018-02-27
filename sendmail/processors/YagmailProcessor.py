"""Sendmail YagmailProcessor module.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""


import inspect
import yagmail
from email.message import Message
from sendmail.processors.abstractprocessor import AbstractProcessor


__author__ = "Brian Johnson"
__copyright__ = "Copyright 2018, Mobius Works, LLC"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "bj@mobiusworks.com"
__status__ = "Production"


class YagmailProcessor(AbstractProcessor):
    """Sends messages using the Yagmail Python library.

    This gives us OAuth2 support for GMail"""

    to_address = None
    conf = {}

    def __init__(self, conf=None):
        """Creates new instance and initializes it according to specified configuration.

        :param conf: Processor configuration.
        :return: New processor instance.
        """

        yag_args = inspect.getargspec(yagmail.SMTP).args
        for key in conf.keys():
            if key in yag_args:
                self.conf[key] = conf[key]

        super(YagmailProcessor, self).__init__(conf)

    def process(self, message):
        """Sends specified message via SMTP server.

        :param message: Message to send.
        """

        print("  - {}: {}.process()".format(self.name, self.__class__.__name__))

        with yagmail.SMTP(**self.conf) as yag:
            yag.send(
                to=self.to_address,
                subject=message.get('subject'),
                contents = message.get_payload(),
                headers = message,
                )
