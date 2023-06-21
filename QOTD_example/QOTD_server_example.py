from loguru import logger
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Protocol, Factory


class QOTD(Protocol):
    '''QOTD (Quote of the Day)'''

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        '''
        В событии connectionMade обычно происходит установка объекта соединения,
        а также любые начальные приветствия
        '''
        self.factory.numProtocols = self.factory.numProtocols + 1
        logger.info(f"Сейчас {self.factory.numProtocols} открытых соединений.\n")
        self.transport.write("Вы кто такие? Я вас не звал! Идите нахуй!\r\n".encode())
        self.transport.loseConnection()


class QOTDFactory(Factory):

    numProtocols = 0

    def buildProtocol(self, addr):
        return QOTD(self)


endpoint = TCP4ServerEndpoint(reactor, 8080)
endpoint.listen(QOTDFactory())
reactor.run()
