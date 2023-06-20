from loguru import logger
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory


class EchoClient(Protocol):
    def connectionMade(self):
        message = input('Введи сообщение:\n')  # Сообщение для отправки
        self.transport.write(message.encode())  # Отправка сообщения в виде байтов

    def dataReceived(self, data):
        logger.info(f'Получено от эхо-сервера:\n> {data.decode()}')


class EchoClientFactory(ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()

    def clientConnectionFailed(self, connector, reason):
        logger.warning(f"Не удалось подключиться к эхо-серверу: причина -> {reason.getErrorMessage()}")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        logger.warning(f"Соединение с эхо-сервером потеряно: причина -> {reason.getErrorMessage()}")
        reactor.stop()


reactor.connectTCP("localhost", 8080, EchoClientFactory())
reactor.run()
