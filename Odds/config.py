###
# Copyright (c) 2012, spline
# All rights reserved.
#
#
###

import supybot.conf as conf
import supybot.registry as registry

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Odds', True)


Odds = conf.registerPlugin('Odds')
conf.registerChannelValue(Odds, 'maximumOutput', registry.Integer(10, """Maximum amount of results to output when searching for events."""))


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
