from pathlib import Path

import pandas as pd


def search_crew(query, gw_num, by='name'):
    if gw_num < 41: raise Exception('Only available for GW 41 and onward')
    ROOT = Path()
    DATA_DIR = ROOT / 'data' / str(gw_num) / 'total' / 'crew'
    if not DATA_DIR.exists(): raise Exception('Incorrect GW number')
    points = []
    files = []
    for file_path in sorted(DATA_DIR.iterdir()):
        if '_crew_' not in file_path.name: continue
        files.append(file_path)
        df = pd.read_csv(file_path, sep='\t')
        if by == 'id': wanted_row = df[df['crew_id'] == query]
        if by == 'name': wanted_row = df[df.iloc[:, 2] == query]
        if len(wanted_row) == 0: return 'Not Found'
        points.append(wanted_row.iloc[:, 3].values[0])
    
    if len(files) == 5:
        obj = {
            'gw': None,
            'id': None,
            'name': None,
            'prelim': None,
            'day1': None,
            'day2': None,
            'day3': None,
            'day4': None,
            'total': None,
            'ranking': None
        }
        ranking = wanted_row['ranking_r4'].values[0]
        name = wanted_row.iloc[:, 2].values[0]
        id_ = wanted_row.iloc[:, 1].values[0]
        obj['gw'] = gw_num
        obj['id'] = id_
        obj['name'] = name
        obj['prelim'] = points[0]
        obj['day1'] = points[1] - points[0]
        obj['day2'] = points[2] - points[1]
        obj['day3'] = points[3] - points[2]
        obj['day4'] = points[4] - points[3]
        obj['total'] = max(points)
        obj['ranking'] = ranking
        
        print(f"GW:\t{obj['gw']}")
        print(f"Crew ID:\t{obj['id']}")
        print(f"Name:\t{obj['name']}")
        print(f"Ranking:\t{obj['ranking']:,}")
        print(f"Prelim:\t{obj['prelim']:,} points")
        print(f"Day 1:\t{obj['day1']:,} points")
        print(f"Day 2:\t{obj['day2']:,} points")
        print(f"Day 3:\t{obj['day3']:,} points")
        print(f"Day 4:\t{obj['day4']:,} points")
        print(f"Total:\t{obj['total']:,} points")

    elif len(files) < 5:
        obj = {
            'id': None,
            'name': None,
            'prelim': None,
            'day1': None,
            'day2': None,
            'day3': None,
            'day4': None,
            'total': None,
            'current_ranking': None
        }

        if len(files) >= 1: obj['prelim'] = points[0]
        if len(files) >= 2: obj['day1'] = points[1] - points[0]
        if len(files) >= 3: obj['day2'] = points[2] - points[1]
        if len(files) >= 4: obj['day3'] = points[3] - points[2]
        if len(files) >= 5: obj['day4'] = points[4] - points[3]

        obj['total'] = max(points)
        obj['current_ranking'] = wanted_row.iloc[:, 0].values[0]
        obj['name'] = wanted_row.iloc[:, 2].values[0]
        obj['id'] = wanted_row.iloc[:, 1].values[0]

        print(f'GW:\t{gw_num}')
        print(f"Crew ID:\t{obj['id']}")
        print(f"Name:\t{obj['name']}")
        print(f"Current ranking:\t{obj['current_ranking']:,}")
        print(f"Prelim:\t{obj['prelim']:,} points")
        try:
            print(f"Day 1:\t{obj['day1']:,} points")
        except:
            print(f"Day 1:")
        try:
            print(f"Day 2:\t{obj['day2']:,} points")
        except:
            print(f"Day 2:")
        try:
            print(f"Day 3:\t{obj['day3']:,} points")
        except:
            print(f"Day 3:")
        try:
            print(f"Day 4:\t{obj['day4']:,} points")
        except:
            print(f"Day 4:")
        print(f"Total:\t{obj['total']:,} points")

def search_indiv(query, gw_num, by='id'):
    ROOT = Path()
    DATA_DIR = ROOT / 'data' / str(gw_num) / 'total' / 'indiv'
    if not DATA_DIR.exists(): raise Exception('Incorrect GW number')

    files = []
    for file_path in sorted(DATA_DIR.iterdir()):
        if '_indiv_' not in file_path.name: continue
        files.append(file_path)
    # Switch interlude and prelim order
    if len(files) > 1: files[0], files[1] = files[1], files[0]
    
    points = []
    battles = []
    for file in files:
        df = pd.read_csv(file, sep='\t')
        if by == 'name': wanted_row = df[df.iloc[:, 3] == query]
        if by == 'id': wanted_row = df[df.iloc[:, 2] == query]
        try:
            points.append(wanted_row.iloc[:, 5].values[0])
            battles.append(wanted_row.iloc[:, 4].values[0])
        except:
            points.append(0)
            battles.append(0)
    
    id_ = wanted_row.iloc[:, 2].values[0]
    name = wanted_row.iloc[:, 3].values[0]
    ranking = wanted_row.iloc[:, 0].values[0]
    rank = wanted_row.iloc[:, 1].values[0]
    # prev gw case
    if len(files) == 6:
        prelim = points[0]
        if points[1] - prelim < 0: interlude = 0
        else: interlude = points[1] - prelim
        if points[1] == 0: day1 = points[2] - points[0]
        else: day1 = points[2] - points[1]
        if points[2] == 0: day2 = points[3] - points[1]
        else: day2 = points[3] - points[2]
        if points[3] == 0: day3 = points[4] - points[2]
        else: day3 = points[4] - points[3]
        if points[4] == 0: day4 = points[5] - points[3]
        else: day4 = points[5] - points[4]
        total = points[-1]

        print(f'ID:\t{id_}')
        print(f'Name:\t{name}')
        print(f'Rank:\t{rank}')
        print(f'GW:\t{gw_num}')
        print(f'Ranking:\t{ranking:,}')
        print(f'Prelim:\t{prelim:,}\tpoints')
        print(f'Interlude:\t{interlude:,}\tpoints')
        print(f'Day 1:\t{day1:,}\tpoints')
        print(f'Day 2:\t{day2:,}\tpoints')
        print(f'Day 3:\t{day3:,}\tpoints')
        print(f'Day 4:\t{day4:,}\tpoints')
        print(f'Total:\t{total:,}\tpoints')
        print(f'Total battles:\t{battles[-1]:,}')
    
    elif len(files) < 6:
        if len(files) >= 1: prelim = points[0]
        if len(files) >= 2:
            if points[1] - prelim < 0: interlude = 0
            else: interlude = points[1] - prelim
        if len(files) >= 3: 
            if points[1] == 0: day1 = points[2] - points[0]
            else: day1 = points[2] - points[1]
        if len(files) >= 4:
            if points[2] == 0: day2 = points[3] - points[1]
            else: day2 = points[3] - points[2]
        if len(files) >= 5:
            if points[3] == 0: day3 = points[4] - points[2]
            else: day3 = points[4] - points[3]    
        if len(files) >= 6:
            if points[4] == 0: day4 = points[5] - points[3]
            else: day4 = points[5] - points[4]

        print(f'ID:\t{id_}')
        print(f'Name:\t{name}')
        print(f'Rank:\t{rank}')
        print(f'GW:\t{gw_num}')
        print(f'Current Ranking:\t{ranking:,}')
        try: print(f'Prelim:\t{prelim:,}\tpoints')
        except: print(f'Prelim:')
        try: print(f'Interlude:\t{interlude:,}\tpoints')
        except: print(f'Interlude:')
        try: print(f'Day 1:\t{day1:,}\tpoints')
        except: print(f'Day 1:')
        try: print(f'Day 2:\t{day2:,}\tpoints')
        except: print(f'Day 2:')
        try: print(f'Day 3:\t{day3:,}\tpoints')
        except: print(f'Day 3:')
        try: print(f'Day 4:\t{day4:,}\tpoints')
        except: print(f'Day 4:')
        print(f'Total:\t{points[-1]:,}\tpoints')
        print(f'Total battles:\t{battles[-1]:,}')

        

def show_cumu(query, gw_num, day, search_by='name'):
    ROOT = os.getcwd()
    DATA_DIR = os.path.join(ROOT, 'data', str(gw_num), 'speed', 'day{}'.format(day))
    files = [file for file in os.listdir(DATA_DIR) if not file.startswith('.')]
    points = []
    times = []
    for i, file_ in enumerate(sorted(files)):
        # Per hour
        if i % 3 != 0:
            continue
        fpath = os.path.join(DATA_DIR, file_)
        df = pd.read_csv(fpath, sep='\t')
        if search_by == 'name':
            wanted_row = df[df.iloc[:, 2] == query]
        if search_by == 'id':
            wanted_row = df[df['crew_id'] == query]
        points.append(wanted_row.iloc[:, 3].values[0])
        times.append(file_[16:-4].replace('-', ':'))
    name = wanted_row.name.values[0]
    id_ = wanted_row.crew_id.values[0]
    points = [point - points[0] for point in points]

    print('Crew ID:\t{}'.format(id_))
    print('Name:\t{}'.format(name))
    print('GW:\t{}'.format(gw_num), 'Day:\t{}'.format(day), sep='\t')
    print('Accumulate points:')
    for i in range(0, len(points)):
        print(times[i], '{:,}'.format(points[i]), sep='\t')

def show_gain(query, gw_num, day, search_by='name'):
    ROOT = os.getcwd()
    DATA_DIR = os.path.join(ROOT, 'data', str(gw_num), 'speed', 'day{}'.format(day))
    files = [file for file in os.listdir(DATA_DIR) if not file.startswith('.')]
    points = []
    times = []
    for i, file_ in enumerate(sorted(files)):
        if i % 3 != 0:
            continue
        fpath = os.path.join(DATA_DIR, file_)
        df = pd.read_csv(fpath, sep='\t')
        if search_by == 'name':
            wanted_row = df[df.iloc[:, 2] == query]
        if search_by == 'id':
            wanted_row = df[df['crew_id'] == query]
        points.append(wanted_row.iloc[:, 3].values[0])
        times.append(file_[16:-4].replace('-', ':'))
    name = wanted_row.name.values[0]
    id_ = wanted_row.crew_id.values[0]
    points = [point - points[0] for point in points]
    gains = [points[i] - points[i - 1] for i in range(1, len(points))]
    print('Crew ID:\t{}'.format(id_))
    print('Name:\t{}'.format(name))
    print('GW:\t{}'.format(gw_num), 'Day:\t{}'.format(day), sep='\t')
    print('Points gained:')
    for i in range(0, len(gains)):
        print('{} - {}'.format(times[i],times[i+1]), '{:,}'.format(gains[i]), sep='\t')
    print('Total:\t{:,}\tpoints'.format(sum(gains)))
