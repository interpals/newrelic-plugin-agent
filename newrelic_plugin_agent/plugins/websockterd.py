"""
WebSocketerD

"""
import logging
import requests

from newrelic_plugin_agent.plugins import base

LOGGER = logging.getLogger(__name__)

class WebSocketerD(base.JSONStatsPlugin):

    DEFAULT_HOST = 'localhost'
    DEFAULT_PATH = '/v1/ws/stats'
    GUID = 'net.interpals.newrelic_websocketerd_node_agent'

    def fetch_data(self):
        response = self.http_get(self.stats_url)

        if response.status_code == 200:
            data = response.json()

            self.add_gauge_value('Stats/Connection', 'count', data.get('connections', 0))

            memory = data.get('memory')

            self.add_gauge_value('Stats/Memory/Alloc', 'bytes', memory.get("alloc"))
            self.add_gauge_value('Stats/Memory/HeapAlloc', 'bytes', memory.get("heap-alloc"))
            self.add_gauge_value('Stats/Memory/HeapSys', 'bytes', memory.get("heap-sys"))
            self.add_gauge_value('Stats/Memory/TotalAlloc', 'bytes', memory.get("total-alloc"))

            pubsub = data.get('pubsub')

            self.add_gauge_value('Stats/PubSub/Channels', 'count', pubsub.get('channels', 0))
            self.add_gauge_value('Stats/PubSub/Clients', 'count', pubsub.get('clients', 0))

        else:
            LOGGER.error('Error collecting cluster stats (%s): %s',
                         response.status_code, response.content)
