import argparse
import platform
from time import time, sleep
from datetime import datetime, timedelta
from pathlib import Path

from tqdm import tqdm
from helper import ChromeConfig, GuildWarInfo, scrape, login


parser = argparse.ArgumentParser()
parser.add_argument('gw', type=str, help="Current GW number only.")
parser.add_argument("--prelim", 
                    help="Scrape prelim ranking, seed ranking, crew rankings and individual ranking at the end of prelim",
                    nargs=5,
                    type=int,
                    metavar=('start', 'prelim_end', 'seed_end', 'crew_end', 'indiv_end'))
parser.add_argument("--interlude",
                    help="Scrape only individual rankings data",
                    nargs=2,
                    type=int,
                    metavar=('start', 'end'))
parser.add_argument("--speed", 
                    help="Scrape crew rankings data thoughout the day",
                    nargs=4,
                    metavar=('day', 'top', 'every', 'timestep'))
parser.add_argument("--crew",
                    help="Scrape crew rankings data",
                    nargs=3,
                    type=int,
                    metavar=('start', 'end', 'day'))
parser.add_argument("--indiv", 
                    help="Scrape player rankings data",
                    nargs=3,
                    type=int,
                    metavar=('start', 'end', 'day'))
args = parser.parse_args()

def main():
    info = GuildWarInfo(args.gw, suffix='')
    os_ = platform.system()
    browser = ChromeConfig(os_)
    ROOT_DIR = ChromeConfig(os_).root_dir

    if args.prelim is not None:
        start_page, prelim_end_page, seed_end_page, crew_end_page, indiv_end_page = args.prelim
        save_dir = ROOT_DIR / 'data' / args.gw / 'prelim' / 'crew'
        # Prelim rankings
        GBF = browser.open_chrome()
        login(GBF)
        print(f'*************** Scraping crew preliminary ranking ***************')
        df = scrape(start_page, 
                    prelim_end_page, 
                    info.base_crew_prelim_rankings_url, 
                    info, GBF, 'crew')
        print(f'*************** Done ***************')
        if not save_dir.exists(): save_dir.mkdir(parents=True)
        fname = f'{args.gw}_prelim_ranking.tsv'
        fpath = save_dir / fname
        df.to_csv(fpath, sep='\t', index=False)
        print(f'*************** Saved at {fpath} ***************')

        # Seed rankings
        print(f'*************** Scraping seed ranking ***************')
        df = scrape(start_page, 
                    seed_end_page, 
                    info.base_seed_rankings_url, 
                    info, GBF, 'crew')
        print(f'*************** Done ***************')
        fname = f'{args.gw}_seed_ranking.tsv'
        fpath = save_dir / fname
        df.to_csv(fpath, sep='\t', index=False)
        print(f'*************** Saved at {fpath} ***************')

        # Total crew rankings (end of prelim)
        info.suffix = '_prelim'
        save_dir = ROOT_DIR / 'data' / args.gw / 'total' / 'crew'
        print(f'*************** Scraping crew ranking ***************')
        df = scrape(start_page, 
                    crew_end_page, 
                    info.base_crew_rankings_url, 
                    info, GBF, 'crew')
        print(f'*************** Done ***************')
        fname = f'{args.gw}_crew_prelim.tsv'
        if not save_dir.exists(): save_dir.mkdir(parents=True)
        fpath = save_dir / fname
        df.to_csv(fpath, sep='\t', index=False)
        print(f'*************** Saved at {fpath} ***************')

        # Total individual rankings (end of prelim)
        save_dir = ROOT_DIR / 'data' / args.gw / 'total' / 'indiv'
        print(f'*************** Scraping individual ranking ***************')
        df = scrape(start_page, 
                    indiv_end_page, 
                    info.base_indiv_rankings_url, 
                    info, GBF, 'player')
        GBF.close()
        print(f'*************** Done ***************')
        if not save_dir.exists(): save_dir.mkdir(parents=True)
        fname = f'{args.gw}_indiv_prelim.tsv'
        fpath = save_dir / fname
        df.to_csv(fpath, sep='\t', index=False)
        print(f'*************** Saved at {fpath} ***************')

    if args.interlude is not None:
        # At the end of interlude, scrape only player.
        start_page, end_page = args.interlude
        info.suffix = '_interlude'
        save_dir = ROOT_DIR / 'data' / args.gw / 'total' / 'indiv'
        
        GBF = browser.open_chrome()
        login(GBF)
        print(f'*************** Scraping individual ranking ***************')
        df = scrape(start_page,
                    end_page,
                    info.base_indiv_rankings_url,
                    info, GBF, 'player')
        GBF.close()
        print(f'*************** Done ***************')
        if not save_dir.exists(): save_dir.mkdir(parents=True)
        fname = f'{args.gw}_indiv_interlude.tsv'
        fpath = save_dir / fname
        df.to_csv(fpath, sep='\t', index=False)
        print(f'*************** Saved at {save_dir} ***************')

    if args.speed is not None:
        def cal_date():
            date = datetime.now() + timedelta(hours=2)
            hour = date.strftime("%H")
            if hour == '00': hour = '24'
            first_dig_minute = int(date.strftime("%M")[0])
            if first_dig_minute in range(0, 2): first_dig_minute = 0
            elif first_dig_minute in range(2,4): first_dig_minute = 2
            else: first_dig_minute = 4
            return date, hour, first_dig_minute

        day, topk, interval, timestep = [int(arg) for arg in args.speed]
        assert day in [1, 2, 3, 4]

        save_dir = ROOT_DIR / 'data' / args.gw / 'speed' / f'day{day}'
        if not save_dir.exists(): save_dir.mkdir(parents=True)

        GBF = browser.open_chrome()
        login(GBF)
        for _ in range(timestep):
            date, hour, first_dig_minute = cal_date()
            t0 = time()
            print(f'*************** Scraping top {topk} crew points @{hour}:{first_dig_minute}0 JST  ***************')
            df = scrape(1,
                        topk // 10,
                        info.base_crew_rankings_url,
                        info, GBF, 'crew')
            print(f'*************** Done ***************')
            date, hour, first_dig_minute = cal_date()
            fname = f'{args.gw}_top{topk}_day{day}_{hour}-{first_dig_minute}0JST.tsv'
            fpath = save_dir / fname
            df.to_csv(fpath, sep='\t', index=False)
            print(f'*************** Saved at {fpath} ***************')
            next_iter = (date + timedelta(minutes=20)).strftime("%H.%M")
            print(f'*************** Next iteration: {next_iter} JST ***************')
            t1 = time()
            sleep(interval * 60 - (t1 - t0))
        GBF.close()

    if args.crew is not None:
        # Scrape crew rankings at the end of each round (Day 1 to Day 4)
        start_page, end_page, day = args.crew
        info.suffix = f'_r{day}'
        save_dir = ROOT_DIR / 'data' / args.gw / 'total' / 'crew'

        GBF = browser.open_chrome()
        login(GBF)
        print(f'*************** Scraping crew ranking ***************')
        df = scrape(start_page, 
                    end_page, 
                    info.base_crew_rankings_url, 
                    info, GBF, 'crew')
        GBF.close()
        print(f'*************** Done ***************')
        if not save_dir.exists(): save_dir.mkdir(parents=True)
        fname = f'{args.gw}_crew{info.suffix}.tsv'
        fpath = save_dir / fname
        df.to_csv(fpath, sep='\t', index=False)
        print(f'*************** Saved to {fpath} ***************')

    if args.indiv is not None:
        # Scrape individual rankings at the end of each round (Day 1 to Day 4)
        start_page, end_page, day = args.indiv
        info.suffix = f'_r{day}'
        save_dir = ROOT_DIR / 'data' / args.gw / 'total' / 'indiv'

        GBF = browser.open_chrome()
        login(GBF)
        print(f'*************** Scraping individual ranking ***************')
        df = scrape(start_page, 
                    end_page, 
                    info.base_indiv_rankings_url, 
                    info, GBF, 'player')
        GBF.close()
        print(f'*************** Done ***************')
        if not save_dir.exists(): save_dir.mkdir(parents=True)
        fname = f'{args.gw}_indiv{info.suffix}.tsv'
        fpath = save_dir / fname
        df.to_csv(fpath, sep='\t', index=False)
        print(f'*************** Saved at {fpath} ***************')
if __name__ == '__main__':
    main()
