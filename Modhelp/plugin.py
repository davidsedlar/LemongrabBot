###
# Copyright (c) 2012, Pooh Bear
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs


class Modhelp(callbacks.Plugin):
    def modhelp(self, irc, msg, args, text):
        """Internal message for notifying all the #channel,ops in a channel of a given situation."""
        alert = 'ALERT TO ALL OPS: '
        alert = ircutils.bold(ircutils.mircColor(alert, 'red'))
        if not text:
        	text="No message, but something is probably up."
        	text = format('%s %s', alert, text)
        	text += format(' (from %s)', msg.nick)
        	irc.reply(text, to='#tamods', notice=True)
        	#irc.reply('The mods have been alerted and will be with you shortly.', private=True, notice=True)
        else:
        	text = format('%s %s', alert, text)
        	text += format(' (from %s)', msg.nick)
        	irc.reply(text, to='#tamods', notice=True)
        	#irc.reply('The mods have been alerted and will be with you shortly.', private=True, notice=True)
    modhelp = wrap(modhelp,[additional('text')])

    threaded = True

Class = Modhelp


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
