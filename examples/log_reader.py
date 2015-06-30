from circuits.journald.poller import JournalPoller

class Reader(JournalPoller):

    def read(self, line):
        print(line['_HOSTNAME'])


Reader().run()