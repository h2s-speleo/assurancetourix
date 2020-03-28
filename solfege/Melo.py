#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import solfege as SF


class Melo:
    def __init__(self, **kwargs):
        self.parent = None
        self.tonal = None
        self.rythme = None

        self.reset(**kwargs)

    def reset(self, **kwargs):
        self.tonal = SF.Tonal(**kwargs)
        self.tonal.parent = self
