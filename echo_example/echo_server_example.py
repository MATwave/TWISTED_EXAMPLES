from loguru import logger
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory


class Echo(Protocol):
    def dataReceived(self, data):
        logger.info(f'Получено от клиента:\n> {data.decode()}')
        self.transport.write(data)


class EchoFactory(Factory):
    def buildProtocol(self, addr):
        return Echo()


reactor.listenTCP(8080, EchoFactory())
reactor.run()
