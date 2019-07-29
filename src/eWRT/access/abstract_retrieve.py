#!/usr/bin/env python

from builtins import object
import abc
from future.utils import with_metaclass


class AbstractRetriever(with_metaclass(abc.ABCMeta, object)):

    @abc.abstractmethod
    def set_up(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def tear_down(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def open(self):
        pass
