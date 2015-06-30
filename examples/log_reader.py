import sys

sys.path.insert(0, '/mnt/data/Labs/Python/circuits.journald')
print(sys.path)

from circuits.journald.poller import JournalPoller

class Reader(JournalPoller):

    def read(self, line):
        print(line['_HOSTNAME'])


Reader().run()