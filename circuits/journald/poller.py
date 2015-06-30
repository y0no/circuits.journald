from systemd import journal

from circuits.core.pollers import Poll, BasePoller
from circuits import BaseComponent, handler
from circuits.core.utils import findcmp
from circuits.io.events import ready, read

class JournalPoller(BaseComponent):
    channel = 'journalctl'

    def __init__(self, channel=channel):
        super(JournalPoller, self).__init__(channel=channel)
        self._poller = None
        self.journal = journal.Reader()
        self.journal.seek_tail()

    @handler("registered", "started", channel="*")
    def _on_registered_or_started(self, component, manager=None):
        if self._poller is None:
            if isinstance(component, BasePoller):
                self._poller = component
                self.fire(ready(self))
            else:
                if component is not self:
                    return
                component = findcmp(self.root, BasePoller)
                if component is not None:
                    self._poller = component
                    self.fire(ready(self))
                else:
                    self._poller = Poll().register(self)
                    self.fire(ready(self))

    @handler('ready')
    def __on_ready(self, comonent):
        self._poller.addReader(self, self.journal)

    @handler('_read', priority=1)
    def __on_read(self, fd):
        for line in self.journal:
            self.fire(read(line))
        self.journal.process()
