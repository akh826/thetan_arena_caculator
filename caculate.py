from datetime import date
from thetan_arena_data import hero
import thetan_arena_data
import PySimpleGUI as sg

sg.theme('DarkAmber')   
arr1 = [
    sg.Text("Win rate: ",size=(10, 1)),
    sg.In(size=(25, 1), enable_events=True, key="-winrtate-"),
    sg.Text("gTHC Battles: ",size=(10, 1)),
    sg.In(size=(25, 1), enable_events=True, key="-gthcbattles-"),
    ]
arr2 = [
    sg.Text("THC prices: ",size=(10, 1)),
    sg.In(size=(25, 1), enable_events=True, key="-thc_prices-"),
    ]
hero_rarity = [
    sg.Text("Hero Rarity: ",size=(10, 1)),
    sg.Radio('common', "hero_rarity", default=True, key="-hero_rarity1-", enable_events=True),
    sg.Radio('epic', "hero_rarity", default=False, key="-hero_rarity2-", enable_events=True),
    sg.Radio('legendary', "hero_rarity", default=False, key="-hero_rarity3-", enable_events=True),
]
skin_rarity = [
    sg.Text("Skin Rarity: ",size=(10, 1)),
    sg.Radio('normal', "skin_rarity", default=True, key="-skin_rarity1-", enable_events=True),
    sg.Radio('rare', "skin_rarity", default=False, key="-skin_rarity2-", enable_events=True),
    sg.Radio('mythic', "skin_rarity", default=False, key="-skin_rarity3-", enable_events=True),
]
daily_profit =[
        sg.Text("Daily profit: ",size=(15, 1)),
        sg.Text("",key="expect_profit",size=(25, 1)),
        sg.Text("",key="expect_profit_money",size=(25, 1))
    ]
total_profit=[
        sg.Text("Total profit: ",size=(15, 1)),
        sg.Text("",key="total_profit",size=(25, 1)),
        sg.Text("",key="total_profit_money",size=(25, 1))
    ]
dur =[
        sg.Text("Duration (Days): ",size=(15, 1)),
        sg.Text("",key="duration",size=(25, 1))
    ]

layout = [ 
    arr1,
    arr2,
    hero_rarity,
    skin_rarity,
    daily_profit,
    total_profit,
    dur,
    [sg.Text("* Created by akh826",justification='right',key="duration",size=(75, 1))],
    ]
window = sg.Window('Thetan Arena Caculator', layout)
THC_prices = 0.25

def playduration(herorarity,skin,gthcbattles=None):
    if gthcbattles != None and gthcbattles > 0:
        exp =gthcbattles / hero[herorarity]["daily_battles"]
        return exp
    else:
        min = playduration(herorarity,skin,hero[herorarity][skin]["min_gthc"])
        max = playduration(herorarity,skin,hero[herorarity][skin]["max_gthc"])
        return min ,max

def totalearn(herorarity,winrate,gthcbattles=None):
    # print(gthcbattles)
    if gthcbattles != None and gthcbattles > 0:
        if herorarity in ['common_hero','epic_hero','legendary_hero']:
            round_earn = hero[herorarity]["win_bonus"]*winrate + (1-winrate)
            exp = round_earn*gthcbattles
            return exp
        else:
            return -1
    else:
        min = totalearn(herorarity,winrate,hero[herorarity]["normal"]["min_gthc"])
        max = totalearn(herorarity,winrate,hero[herorarity]["normal"]["max_gthc"])
        return min, max

def dailyearn(herorarity,winrate):
    winrate = float(winrate)
    if not (0 <= winrate <= 1):
        return -1

    if herorarity in ['common_hero','epic_hero','legendary_hero']:
        return dayily(hero[herorarity]["win_bonus"], hero[herorarity]["daily_battles"], winrate)
    else:
        return -1

def dayily(wb, db, wr):
    return wb*db*wr+db*(1-wr)

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def main():
    winrate = thetan_arena_data.winrate
    thc_prices = thetan_arena_data.thc_prices
    hero_rarity = "common_hero"
    skin_rarity = "normal"
    gthcbattles = hero[hero_rarity][skin_rarity]["min_gthc"]

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        try:
            if values['-winrtate-'] == '':
                winrate = thetan_arena_data.winrate
            if isfloat(values['-winrtate-']) and (0 <= float(values['-winrtate-']) <= 1):
                winrate = float(values['-winrtate-'])
        except Exception:
            print("Wrong input winrate")
        try:
            if values['-gthcbattles-'] == '':
                gthcbattles = hero[hero_rarity][skin_rarity]["min_gthc"]
            if isfloat(values['-gthcbattles-']) and (float(values['-gthcbattles-']) > 0):
                gthcbattles = float(values['-gthcbattles-'])
        except Exception:
            print("Wrong input gthcbattles")
        try:
            if values['-thc_prices-'] == '':
                thc_prices = thetan_arena_data.thc_prices
            if isfloat(values['-thc_prices-']):
                thc_prices = float(values['-thc_prices-'])
            else:
                thc_prices = thetan_arena_data.thc_prices
        except Exception:
            print("Wrong input thc_prices")
            thc_prices = thetan_arena_data.thc_prices
            
        if values["-hero_rarity1-"] == True:
            hero_rarity = "common_hero"
        elif values["-hero_rarity2-"] == True: 
            hero_rarity = "epic_hero"
        elif values["-hero_rarity3-"] == True:
            hero_rarity = "legendary_hero"

        if values["-skin_rarity1-"] == True:
            skin_rarity = "normal"
        elif values["-skin_rarity2-"] == True: 
            skin_rarity = "rare"
        elif values["-skin_rarity3-"] == True:
            skin_rarity = "mythic"
        
        expect_profit_money = dailyearn(hero_rarity,winrate)*thc_prices
        window.Element('expect_profit').update(dailyearn(hero_rarity,winrate))
        window.Element('expect_profit_money').update(f"{expect_profit_money}$")
        
        if gthcbattles == '':
            min_earn, max_earn = totalearn(hero_rarity,winrate)
            min_dur, max_dur = playduration(hero_rarity,skin_rarity)
        else:
            min_earn = max_earn = totalearn(hero_rarity,winrate,gthcbattles)
            min_dur = max_dur = playduration(hero_rarity,skin_rarity,gthcbattles)
            
        window.Element('total_profit').update(f"{min_earn} - {max_earn}")
        window.Element('total_profit_money').update(f"{format(float(min_earn*thc_prices),'.3f')}$ - {format(float(max_earn*thc_prices),'.3f')}$")
        window.Element('duration').update(f"{format(float(min_dur),'.1f')} - {format(float(max_dur),'.1f')}")

    window.close()

if __name__ == "__main__":
    main()
    