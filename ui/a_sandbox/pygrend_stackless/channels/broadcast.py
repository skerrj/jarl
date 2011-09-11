import stackless

class BroadcastChannel(stackless.channel):
    def send(self, value, wait=False):
        result = None
        for idx in range(0, self.balance, -1):
            # there are tasklets waiting to receive
            result = stackless.channel.send(self, value)
        return result
    def send_exception(self, exc, value, wait=False):
        result = None
        for idx in range(0, self.balance, -1):
            # there are tasklets waiting to receive
            result = stackless.channel.send_exception(self, exc, value)
        return result
