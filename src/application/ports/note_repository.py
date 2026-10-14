from abc import ABC, abstractmethod


class NoteRepository(ABC):
    @abstractmethod
    def create(self, note):
        ...

    @abstractmethod
    def find_all(self):
        ...

    @abstractmethod
    def find_by_id(self, note_id):
        ...

    @abstractmethod
    def update(self, note):
        ...

    @abstractmethod
    def delete(self, note_id):
        ...
