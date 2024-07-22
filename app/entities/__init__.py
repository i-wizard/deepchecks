from abc import ABCMeta
from abc import abstractmethod

from pydantic.dataclasses import dataclass


@dataclass
class BaseEntity(metaclass=ABCMeta):

    @abstractmethod
    def to_dict(self):
        ...

    @classmethod
    @abstractmethod
    def get_collection(cls):
        ...
