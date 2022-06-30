from rqalpha.core.events import EVENT
from rqalpha.interface import AbstractMod
from .minute_data_source import MinuteDataSource


class MinuteTradeMod(AbstractMod):

    def __init__(self):
        self._env = None
        self._data_source = None

    def start_up(self, env, mod_config):
        self._env = env
        if env.config.base.frequency != '1m':
            return

        self._data_source = MinuteDataSource(env, env.config.base.data_bundle_path)
        env.set_data_source(self._data_source)
        env.event_bus.add_listener(EVENT.POST_USER_INIT, self._load_store)

    def tear_down(self, code, exception=None):
        pass

    def _load_store(self, _):
        self._data_source.load_store()
 