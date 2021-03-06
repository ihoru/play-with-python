# -*- coding: utf-8 -*-

import math
import random
import re
from time import time
from tools import eprint


class Calculator:
    rating_formula_const = 400

    def __init__(self, percent, default_rating, limit):
        self._default_rating = default_rating
        self._rating_diff_percent = percent
        self._limit = limit
        self._users = {}
        self._user_ids = None
        self._length = 0

    def read(self, file):
        i = 0
        for line in file:
            line = re.split('[^\d]', str(line).strip(), 2)
            if not line or len(line) != 2:
                continue
            i += 1
            uid, might = map(int, line)
            self._users[uid] = {
                'id': uid,
                'rating': self._default_rating,
                'might': might,
                'fights': 0,
            }
            if i >= self._limit:
                break
        file.close()
        self._user_ids = tuple(self._users.keys())
        self._length = len(self._user_ids)

    def process(self, fights):
        total = len(self._users) * fights
        i = 0
        process_start = time()
        for _ in range(fights):
            for user_id, user in self._users.items():
                i += 1
                process_finish = time()
                if process_finish - process_start > 5:
                    eprint('%.2f%% - duration: %.5f sec' % (100 * i / total, process_finish - process_start))
                    process_start = time()
                if user['rating'] < 0:
                    continue
                opponent = self.find_opponent(user)
                if not opponent:
                    continue
                diff = self.rating_formula(user['rating'], opponent['rating'])
                if not self.battle_formula(user['might'], opponent['might']):
                    diff *= -1
                user['rating'] += diff
                user['fights'] += 1

    def find_opponent(self, user):
        for _ in range(max(100, math.ceil(self._length / 100))):
            user_id = self._user_ids[random.randint(0, self._length - 1)]
            opponent = self._users[user_id]
            if self.check_restriction(user, opponent):
                return opponent
        min_rating, max_rating = self.get_rating_limits(user)
        fits = [user_id for user_id, op in self._users.items() if
                user_id != user['id'] and min_rating <= op['rating'] <= max_rating]
        length = len(fits)
        if length > 0:
            user_id = fits[random.randint(0, length - 1)]
            return self._users[user_id]
        return False

    def print(self):
        print('id,rating,might,fights')
        for _, user in self._users.items():
            print(','.join(map(str, [user['id'], user['rating'], user['might'], user['fights']])))
        eprint('Fights: %d' % sum(u['fights'] for _, u in self._users.items()))

    @staticmethod
    def battle_formula(attacker_might, defender_might):
        return attacker_might > defender_might

    @staticmethod
    def rating_formula(attacker_rating, defender_rating):
        max_rating = max(attacker_rating, defender_rating)
        min_rating = min(attacker_rating, defender_rating)
        return math.floor(20 / (1 + math.exp((max_rating - min_rating) / Calculator.rating_formula_const)))

    def check_restriction(self, user, opponent):
        if user['id'] == opponent['id']:
            return False
        min_rating, max_rating = self.get_rating_limits(user)

        return min_rating <= opponent['rating'] <= max_rating

    def get_rating_limits(self, user):
        min_rating = max(0, user['rating'] - user['rating'] * self._rating_diff_percent / 100)
        max_rating = user['rating'] + abs(user['rating']) * self._rating_diff_percent / 100

        return min_rating, max_rating
