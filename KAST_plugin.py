import redis
import threading
import os

from .kast.src.kast_runtime import KastRuntime
from onair.src.ai_components.ai_plugin_abstract.ai_plugin import AIPlugin        

class Plugin(AIPlugin):
    def __init__(self, name, headers):
        super().__init__(name, headers)
        self.runtime = KastRuntime(f'KAST/kast/config/gotg_config.ini')

        pool = redis.ConnectionPool(host="localhost", port=6379, password="")
        self.r = redis.Redis(connection_pool=pool, charset="utf-8", decode_responses=True)
        self.position_subscriber = self.r.pubsub()

        self.sub_key = 'mavlink_tlm_position_velocity_ned'
        self.position_subscriber.subscribe(self.sub_key)
        self.listening_thread = threading.Thread(target=self.message_listener)
        self.listening_thread.start()

    def message_listener(self):
        for message in self.position_subscriber.listen():
            if message['type'] != 'message':
                continue
            self.position_msg = message
        


    def update(self,low_level_data=[], high_level_data={}):
        """
        Given streamed data point, system should update internally
        """
        nonros_headers = [header[1:] for header in self.headers] # remove slash from topic names
        
        kast_input = dict(zip(nonros_headers, low_level_data)) 

        kast_input.update({'mavlink_tlm_position_velocity_ned': self.position_msg})

        spellbook = self.runtime.run_step(kast_input, io='both')
        self.knowledge = {}
        
        for key in spellbook.high_level_knowledge.keys():
            self.knowledge.update({key: spellbook.high_level_knowledge[key].value})



    def render_reasoning(self):
        """
        System should return its diagnosis
        """
        return self.knowledge
        
