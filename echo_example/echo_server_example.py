from loguru import logger
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory


class Echo(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def dataReceived(self, data):
        logger.info(f'Получено от клиента:\n> {data.decode()}')
        self.transport.write(data)

    def connectionMade(self):
        self.factory.numProtocols = self.factory.numProtocols + 1
        logger.info(f"Сейчас {self.factory.numProtocols} открытых соединений.\n")

    def connectionLost(self, reason):
        self.factory.numProtocols = self.factory.numProtocols - 1


class EchoFactory(Factory):
    def buildProtocol(self, addr):
        return Echo()


reactor.listenTCP(8080, EchoFactory())
reactor.run()
