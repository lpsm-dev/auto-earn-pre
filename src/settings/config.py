# -*- coding: utf-8 -*-
from __future__ import annotations

from os import environ
from typing import Text


class Config:
    @staticmethod
    def get_env(env: Text) -> Text:
        try:
            return environ.get(env)
        except KeyError as error:
            print(f"KeyError: {error}")
