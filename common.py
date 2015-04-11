# coding: utf-8
from flask import Blueprint as BaseBlueprint


class Blueprint(BaseBlueprint):
    def make_setup_state(self, app, options, first_registration=False):
        state = super(Blueprint, self).make_setup_state(
            app, options, first_registration)
        self.config = app.config
        return state
