from loguru import logger
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
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

    numProtocols = 0

    def buildProtocol(self, addr):
        return Echo(self)


endpoint = TCP4ServerEndpoint(reactor, 8080)
endpoint.listen(EchoFactory())
reactor.run()
