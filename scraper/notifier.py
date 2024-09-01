from abc import ABC, abstractmethod

class NotifierStrategy(ABC):
    @abstractmethod
    def notify(self, message: str):
        pass

# console based notification
class ConsoleNotifier(NotifierStrategy):
    def notify(self, message: str):
        print(message)

# file based notification
class FileNotifier(NotifierStrategy):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def notify(self, message: str):
        with open(self.file_path, 'a') as file_instance:
            file_instance.write(message + '\n')
