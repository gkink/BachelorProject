import json
from collections import Counter
from numpy import uint64

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from sys import path

path.append('clib')
from hash_utils import HashList
path.append('film_data')
from film_index import film_index

# init
hash_lists = []
film_id_list = list(film_index.keys())
threshold = 11

for film_id in film_index:
	full_path_to_desc = film_index[film_id]
	hash_lists.append(HashList(full_path_to_desc))


def search_hashes(hashes):
	enough = len(hashes) // 2
	widespread  = len(hashes) * 3
	barrier = len(hashes) / 8
	num_films = len(film_index)
	counter = Counter(hashes)
	coins = [0] * num_films
	frame_nums = [[] for _ in range(num_films)]
	distances = [[] for _ in range(num_films)]
	spread = [0] * num_films
	
	for h,cnt in counter.most_common():
		for i in range(num_films):
			frame_num,distance = hash_lists[i].search(uint64(h), threshold)
			if frame_num != -1:
				distance_from_frames = max(spread[i], max([abs(x-frame_num) for x in frame_nums[i]] + [0]))
				if distance_from_frames < widespread:
					coins[i] += cnt
					spread[i] = distance_from_frames
					frame_nums[i].append(frame_num)
					distances[i].append(distances)
					if coins[i] >= enough:
						print("coins", coins)
						print("spread", spread)
						return film_id_list[i]
	
#	coins = [coins[i] for i in range(num_films) if spread[i] < widespread]

	if coins:
		max_coins = max(coins)
		max_coins_idx = coins.index(max_coins)
		second_max_coins = max(coins[:max_coins_idx] + coins[max_coins_idx+1:])
		if max_coins >= barrier and max_coins >= 1.2 * second_max_coins:
			print("coins", coins)
			print("spread", spread)
			return film_id_list[coins.index(max(coins))]
	print("coins", coins)
	print("spread", spread)
	return 'not_found'


@csrf_exempt
def index(request):
	if request.method == 'GET':
		return HttpResponse("GET\n")
	elif request.method == 'POST':
		print(request.body.decode('ascii'))
		json_data = json.loads(request.body.decode('ascii'))
		film_id = search_hashes(json_data['frame_hashes'])
		print(film_id)
		return HttpResponse(json.dumps({'film_id':film_id}), content_type="application/json")
