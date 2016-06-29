<?php

$count = $_SERVER['argv'][1] ?: 1;
$start_rating = 500;
$rating_formula_const = 400;
$percent = 30;
$slice = $_SERVER['argv'][2] ?: false;
$file = $dir.'users.txt';

function battle_formula($attacker_might, $defender_might) {
	return $attacker_might > $defender_might;
}

function rating_formula($attacker_rating, $defender_rating) {
	global $rating_formula_const;

	return 20 / (1 + exp((max($attacker_rating, $defender_rating) - min($attacker_rating, $defender_rating)) / $rating_formula_const));
}

function find_defender(array $user) {
	global $users;

	$user_ids = [];
	foreach ($users as $u) {
		if (check_restriction($user, $u)) {
			$user_ids[] = $u['uid'];
		}
	}

	return $user_ids ? $users[$user_ids[array_rand($user_ids)]] : false;
}

function check_restriction(array $user, array $defender) {
	global $percent;
	if ($user['uid'] == $defender['uid']) {
		return false;
	}
	$min_rating = max(0, $user['rating'] - $user['rating'] * $percent / 100);
	$max_rating = $user['rating'] + $user['rating'] * $percent / 100;

	return $defender['rating'] >= $min_rating && $defender['rating'] <= $max_rating;
}

$data = file($file, FILE_IGNORE_NEW_LINES);
if ($slice) {
	shuffle($data);
	$data = array_slice($data, 0, $slice);
}
$users = [];
foreach ($data as $line) {
	list($uid, $might) = array_values(array_filter(array_map('intval', preg_split('/\D+/', $line))));
	$users[$uid] = [
		'uid'    => $uid,
		'rating' => $start_rating,
		'might'  => $might,
		'fights' => 0,
	];
}
$i = 0;
$user_ids = array_keys($users);
$c = 0;
$total = count($user_ids) * $count;
while (++$i <= $count) {
//	shuffle($users);
//	$users = make_hash($users, 'uid');
	foreach ($users as $uid => $user) {
		$min_rating = max(0, $user['rating'] - $user['rating'] * $percent / 100);
		$max_rating = $user['rating'] + $user['rating'] * $percent / 100;
		$try = 0;
		do {
			++$try;
			if ($try >= 50) {
				break;
			}
			$defender = $users[$user_ids[array_rand($user_ids)]];
			if (!check_restriction($user, $defender)) {
				$defender = find_defender($user);
				if (!$defender) {
					break;
				}
			}
			$rating_change = rating_formula($user['rating'], $defender['rating']);
			if (!battle_formula($user['might'], $defender['might'])) {
				$rating_change *= -1;
			}
//			printf('%d against %d get %d (mights: %d against %d)', $user['rating'], $defender['rating'], $rating_change, $user['might'], $defender['might']);echo PHP_EOL;
			$user['rating'] += $rating_change;
			$users[$defender['uid']]['rating'] -= $rating_change;
			++$user['fights'];
			break;
		} while (true);
		++$c;
		if ($c % 10000 == 0) {
			file_put_contents('php://stderr', date(DATE_ISO8601).' '.$c.'/'.$total.'='.round($c / $total * 100, 2).'%'.PHP_EOL);
		}
		$users[$uid] = $user;
	}
}
foreach ($users as $user) {
	echo implode(',', [floor($user['rating']), $user['might'], $user['fights']]).PHP_EOL;
}
