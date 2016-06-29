# -*- coding: utf-8 -*-

import math
import random
import re
from time import time
from tools import eprint


class Calculator:
    users = {}
    user_ids = None
    length = 0
    rating_formula_const = 400
    rating_diff_percent = 30

    def __init__(self):
        pass

    def read(self, file, start_rating, limit):
        i = 0
        for line in file:
            line = re.split('[^\d]', str(line).strip(), 2)
            if not line or len(line) != 2:
                continue
            i += 1
            uid, might = map(int, line)
            self.users[uid] = {
                'id': uid,
                'rating': start_rating,
                'might': might,
                'fights': 0,
            }
            if i >= limit:
                break
        file.close()
        self.user_ids = tuple(self.users.keys())
        self.length = len(self.user_ids)

    def process(self, fights):
        total = len(self.users) * fights
        i = 0
        process_start = time()
        for _ in range(fights):
            for user_id, user in self.users.items():
                i += 1
                process_finish = time()
                if process_finish - process_start > 5:
                    eprint('%.2f%% - duration: %.5f sec' % (100 * i / total, process_finish - process_start))
                    process_start = time()
                opponent = self.find_opponent(user)
                if not opponent:
                    continue
                diff = self.rating_formula(user['rating'], opponent['rating'])
                if not self.battle_formula(user['might'], opponent['might']):
                    diff *= -1
                user['rating'] += diff
                user['fights'] += 1

    def find_opponent(self, user):
        for _ in range(100):
            user_id = self.user_ids[random.randint(0, self.length - 1)]
            opponent = self.users[user_id]
            if self.check_restriction(user, opponent):
                return opponent
        return False

    def print(self):
        print('id,rating,might,fights')
        for _, user in self.users.items():
            print(','.join(map(str, [user['id'], user['rating'], user['might'], user['fights']])))

    @staticmethod
    def battle_formula(attacker_might, defender_might):
        return attacker_might > defender_might

    @staticmethod
    def rating_formula(attacker_rating, defender_rating):
        max_rating = max(attacker_rating, defender_rating)
        min_rating = min(attacker_rating, defender_rating)
        return math.floor(20 / (1 + math.exp((max_rating - min_rating) / Calculator.rating_formula_const)))

    @staticmethod
    def check_restriction(user, opponent):
        if user['id'] == opponent['id']:
            return False
        min_rating = max(0, user['rating'] - user['rating'] * Calculator.rating_diff_percent / 100)
        max_rating = user['rating'] + user['rating'] * Calculator.rating_diff_percent / 100

        return min_rating <= opponent['rating'] <= max_rating
