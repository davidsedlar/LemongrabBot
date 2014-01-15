###
# Copyright (c) 2012, staticsafe
# All rights reserved.
#
#
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring
import random

_ = PluginInternationalization('Catfacts')

@internationalizeDocstring
class Catfacts(callbacks.Plugin):
    """Add the help for "@plugin help Catfacts" here
    This should describe *how* to use this plugin."""
    threaded = True

    def catfacts(self, irc, msg, args):
        """<catfacts>
        Shows a random catfact"""

        with open("plugins/Catfacts/catfacts.txt", "r") as text:
            facts = list(text)

        randomfact = random.choice(facts).encode("utf-8")

        irc.reply(randomfact.strip('\n'))


Class = Catfacts


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
