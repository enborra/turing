import os, platform


class MachineSystem(object):

    ENV_SIMULATED = 'SIMULATED'
    ENV_ONBOARD = 'ONBOARD'

    @classmethod
    def get_environment(cls):
        resp = None

        if platform.system().lower() == 'darwin':
            resp = cls.ENV_SIMULATED
        else:
            resp = cls.ENV_ONBOARD

        return resp

    @classmethod
    def is_simulated(cls):
        resp = False

        if cls.get_environment() == cls.ENV_SIMULATED:
            resp = True

        return resp

    @classmethod
    def is_onboard(cls):
        resp = False

        if cls.get_environment() == cls.ENV_ONBOARD:
            resp = True

        return resp
