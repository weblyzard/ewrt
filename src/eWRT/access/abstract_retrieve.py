#!/usr/bin/env python

import abc


class AbstractRetriever(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def set_up(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def tear_down(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def open(self):
        pass
