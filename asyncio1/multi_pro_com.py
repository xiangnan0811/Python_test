#!/usr/bin/env python
"""
@author: weibo
@contact: weibo@yadingdata.com
@time: 2022/5/1 14:29
@file: multi_pro_com.py
@desc:
"""
import asyncio
from random import random


class MultiProducerConsumer:

    def __init__(self):
        self.task_queue = asyncio.Queue()
        self.result_queue = asyncio.Queue()

    async def task_producer(self, n):
        product = []
        for i in range(n):
            await asyncio.sleep(1)
            product.append(random() * 3)
        self.task_queue.put_nowait(product)
        print(f'put task: {product} to task queue successfully')

    async def task_consumer_and_res_producer(self):
        while True:
            tasks = await self.task_queue.get()
            print(f'get task: {tasks} from task queue successfully')
            for task in tasks:
                print(f'in task_consumer_and_res_producer for loop: {task}')
                await asyncio.sleep(task)
                res = random()
                self.result_queue.put_nowait(res)
                print(f'put result: {res} to result queue successfully')
            self.task_queue.task_done()

    async def res_consumer(self):
        while True:
            res = await self.result_queue.get()
            print(f'get result: {res} from result queue successfully')
            await asyncio.sleep(res)
            print(f'consumer result: {res} successfully')
            self.result_queue.task_done()

    async def run(self):
        t_tasks = [asyncio.create_task(self.task_producer(i)) for i in range(5)]
        ts_tasks = [asyncio.create_task(self.task_consumer_and_res_producer()) for _ in range(10)]
        r_tasks = [asyncio.create_task(self.res_consumer()) for _ in range(10)]

        await asyncio.gather(*t_tasks, return_exceptions=True)
        await self.task_queue.join()
        for t in ts_tasks:
            t.cancel()

        await asyncio.gather(*ts_tasks, return_exceptions=True)
        await self.result_queue.join()
        for t in r_tasks:
            t.cancel()

        await asyncio.gather(*r_tasks, return_exceptions=True)

        print('all tasks completed')


if __name__ == '__main__':
    m = MultiProducerConsumer()
    asyncio.run(m.run())
