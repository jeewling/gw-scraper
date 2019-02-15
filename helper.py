import time
from pathlib import Path

import pandas as pd
from selenium import webdriver
from seleniumrequests import Chrome
from tqdm import tqdm


class ChromeConfig():
    def __init__(self, os_):
        self.root_dir = Path()
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--disable-infobars')
        self.chrome_profile_dir = self.root_dir / 'chrome_profile'
        if os_ == 'Windows':
            self.chrome_options.add_argument(
                r'user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data'
            )
            self.driver_path = self.root_dir / 'webdriver' / 'chromedriver.exe'
            # self.chrome_options.add_argument('--profile-directory=Profile 1')
        if os_ == 'Darwin':
            self.chrome_options.add_argument(f'user-data-dir={self.chrome_profile_dir}')
            self.driver_path = self.root_dir / 'webdriver' / 'chromedriver'
            # self.chrome_options.add_argument('--profile-directory=Profile 1')

    def open_chrome(self):
        return Chrome(executable_path=self.driver_path, options=self.chrome_options)


class GuildWarInfo():
    def __init__(self, gw_num, suffix=''):
        self.gw_num = gw_num
        self.suffix = suffix
        self.request_headers = {'Accept': '''application/json'''}
        self.home_url = 'http://game.granbluefantasy.jp/'
        self.base_crew_prelim_rankings_url = f'{self.home_url}teamraid0{gw_num}/rest/ranking/guild/detail/'
        self.base_seed_rankings_url = f'{self.home_url}teamraid0{gw_num}/rest_ranking_seedguild/detail/'
        self.base_crew_rankings_url = f'{self.home_url}teamraid0{gw_num}/rest/ranking/totalguild/detail/'
        self.base_indiv_rankings_url = f'{self.home_url}teamraid0{gw_num}/rest_ranking_user/detail/'


class Header():
    def __init__(self, suffix, mode):
        if mode == 'crew':
            self.crew_id = 'crew_id'
            self.crew_ranking = f'ranking{suffix}'
            self.crew_name = f'name{suffix}'
            self.crew_points = f'points{suffix}'
            self.col_name = [
                self.crew_ranking,
                self.crew_id,
                self.crew_name,
                self.crew_points
            ]
        if mode == 'player':
            self.player_ranking = f'ranking{suffix}'
            self.player_rank = f'rank{suffix}'
            self.player_name = f'name{suffix}'
            self.player_battles = f'battles{suffix}'
            self.player_points = f'points{suffix}'
            self.col_name = [
                self.player_ranking,
                self.player_rank,
                'id',
                self.player_name,
                self.player_battles,
                self.player_points
            ]


def login(GBF):
    GBF.get('http://game.granbluefantasy.jp/')
    input('Please login and then press any key to start.')

def scrape(start_page, end_page, base_url, info, GBF_, mode):
    rows = []
    header = Header(info.suffix, mode)
    for page_num in tqdm(range(start_page, end_page + 1)):
        chk = True
        while chk:
            try: 
                URL = f'{base_url}{page_num}'
                response = GBF_.request('get', URL, headers=info.request_headers)
                response = response.json()
                data = response['list']
                chk = False
            except:
                tqdm.write(f'Error occurs on page {page_num}, retry...')
                continue

        if mode == 'crew':
            for crew in data:
                row = (
                    crew['ranking'],
                    crew['id'],
                    crew['name'],
                    crew['point']
                )
                rows.append(row)

        if mode == 'player':
            for player in data:
                row = (
                    player['rank'],
                    player['level'],
                    player['user_id'],
                    player['name'],
                    player['defeat'],
                    player['point'],
                )
                rows.append(row)
    return pd.DataFrame(rows, columns=header.col_name)
