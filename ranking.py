import requests
from math import floor

API_URL = "https://aceptaelreto.com/ws/volume/"
HARD = 0.5
MEDIUM = 0.75

def fetch():

    volumes = requests.get(API_URL).json()
    vol_ids = []
    for vol in volumes['subcats']:
        vol_ids.append(vol['id'])

    problem_map = {}

    for vol_id in vol_ids:
        response = requests.get(API_URL + f"{vol_id}/problems").json()
        for problem in response['problem']:
            problem_id = problem['num']
            index = problem['dacu'] / problem['totalUsers']
            if index > MEDIUM:
                label = 'green'
            elif index > HARD:
                label = 'orange'
            else:
                label = 'red'
            problem_map[problem_id] = {'index': index, 'label': label}
    return problem_map

import matplotlib.pyplot as plt
def plot(problem_map: dict):
    # Convert the problem_map dictionary to two separate lists
    problem_ids = list(problem_map.keys())
    indices = [entry['index'] for entry in problem_map.values()]

    # Plot the distribution
    colors = [entry['label'] for entry in problem_map.values()]
    plt.bar(problem_ids, indices, color=colors)

    plt.xlabel('Problem ID')
    plt.ylabel('Index')
    # ('Number of users who solved the problem/Total number of users who attempted the problem')
    plt.title('Distribution of Problem Indices')

    # Draw horizontal dotted lines
    plt.axhline(y=HARD, color='gray', linestyle='dotted', label='Easy')
    plt.axhline(y=MEDIUM, color='gray', linestyle='dotted', label='Medium')

    plt.savefig('result.png')
    #plt.show()

def get_score(problem_number: int, problem_map: dict):
    if (problem_map is None):
        problem_map = fetch()
    if problem_number in problem_map:
        index = problem_map[problem_number]['index']
        score = index * 100
        return score
    else:
        return None

def list_hard_problems(problem_map: dict):
    red_labeled_problems = [problem_id for problem_id, entry in problem_map.items() if entry['label'] == 'red']
    volume_map = {}
    for problem_id in red_labeled_problems:
        volume = floor(problem_id / 100)
        if volume not in volume_map:
            volume_map[volume] = []
        volume_map[volume].append(problem_id)
    print("Hardest problems by volume:\n")
    for volume, problems in volume_map.items():
        print(f"Volume {volume}: {problems}")

if __name__ == '__main__':
    problem_map = fetch()
    list_hard_problems(problem_map)
    plot(problem_map)
