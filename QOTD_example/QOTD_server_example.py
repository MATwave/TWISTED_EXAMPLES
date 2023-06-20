from loguru import logger
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory


class QOTD(Protocol):
    '''QOTD (Quote of the Day)'''

    def connectionMade(self):
        logger.info(f'Подключился клиент')
        self.transport.write("Вы кто такие? Я вас не звал! Идите нахуй!\r\n".encode())
        self.transport.loseConnection()


class QOTDFactory(Factory):
    def buildProtocol(self, addr):
        return QOTD()


reactor.listenTCP(8080, QOTDFactory())
reactor.run()
