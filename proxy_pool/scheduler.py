#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:huchong

import time
from multiprocessing import Process
from proxy_pool.getter import Getter
from proxy_pool.setting import GETTER_CYCLE, GETTER_ENABLED


class Scheduler(object):
    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def run(self):
        print('代理池开始运行')

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()


if __name__ == '__main__':
    pass
