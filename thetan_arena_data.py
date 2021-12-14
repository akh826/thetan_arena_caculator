from pythonpancakes import PancakeSwapAPI
from multiprocessing.pool import ThreadPool

def getprices(address):
    ps = PancakeSwapAPI()
    tokens = ps.tokens(address)
    prices = tokens['data']['price']
    return float(prices)

def getprices_thc():
    try:
        return getprices('0x24802247bd157d771b7effa205237d8e9269ba8a')
    except Exception:
        return 0.2

def getprices_thg():
    try:
        return getprices('0x9fd87aefe02441b123c3c32466cd9db4c578618f')
    except Exception:
        return 0.2

def get_prices_data():
    pool = ThreadPool(processes=10)
    async_result = pool.apply_async(getprices_thc)
    async_result2 = pool.apply_async(getprices_thg)
    return async_result.get(),async_result2.get()




hero = {}
hero['common_hero'] = {}
hero['epic_hero'] = {}
hero['legendary_hero'] = {}

winrate = .5
thc_prices, thg_prices = get_prices_data()

# common_hero = {}
# epic_hero = {}
# legendary_hero = {}

hero['common_hero']["win_bonus"] = 3.25
hero['epic_hero']["win_bonus"] = 6.5
hero['legendary_hero']["win_bonus"] = 23.55

hero['common_hero']["daily_battles"] = 8
hero['epic_hero']["daily_battles"] = 10
hero['legendary_hero']["daily_battles"] = 12

hero['common_hero']["normal"] = {}
hero['common_hero']["normal"]["min_gthc"] = 215
hero['common_hero']["normal"]["max_gthc"] = 227

hero['common_hero']["rare"] = {}
hero['common_hero']["rare"]["min_gthc"] = 228
hero['common_hero']["rare"]["max_gthc"] = 240

hero['common_hero']["mythic"] = {}
hero['common_hero']["mythic"]["min_gthc"] = 241
hero['common_hero']["mythic"]["max_gthc"] = 253

hero['epic_hero']["normal"] = {}
hero['epic_hero']["normal"]["min_gthc"] = 348
hero['epic_hero']["normal"]["max_gthc"] = 373

hero['epic_hero']["rare"] = {}
hero['epic_hero']["rare"]["min_gthc"] = 376
hero['epic_hero']["rare"]["max_gthc"] = 402

hero['epic_hero']["mythic"] = {}
hero['epic_hero']["mythic"]["min_gthc"] = 405
hero['epic_hero']["mythic"]["max_gthc"] = 433

hero['legendary_hero']["normal"] = {}
hero['legendary_hero']["normal"]["min_gthc"] = 753
hero['legendary_hero']["normal"]["max_gthc"] = 829

hero['legendary_hero']["rare"] = {}
hero['legendary_hero']["rare"]["min_gthc"] = 839
hero['legendary_hero']["rare"]["max_gthc"] = 923

hero['legendary_hero']["mythic"] = {}
hero['legendary_hero']["mythic"]["min_gthc"] = 933
hero['legendary_hero']["mythic"]["max_gthc"] = 1026

def main():
    print(thc_prices)
    print(thg_prices)
    print(hero)
    

if __name__ == "__main__":
    main()
