from data import hero
import PySimpleGUI as sg

sg.theme('DarkAmber')   
winrate_arr = [sg.Text("Win rate: "),sg.In(size=(25, 1), enable_events=True, key="-winrtate-"),]
hero_rarity = [
    sg.Text("Hero Rarity: "),
    sg.Radio('common', "hero_rarity", default=True, key="-hero_rarity1-", enable_events=True),
    sg.Radio('epic', "hero_rarity", default=False, key="-hero_rarity2-", enable_events=True),
    sg.Radio('legendary', "hero_rarity", default=False, key="-hero_rarity3-", enable_events=True),
]
skin_rarity = [
    sg.Text("Skin Rarity: "),
    sg.Radio('normal', "skin_rarity", default=True, key="-skin_rarity1-", enable_events=True),
    sg.Radio('rare', "skin_rarity", default=False, key="-skin_rarity2-", enable_events=True),
    sg.Radio('mythic', "skin_rarity", default=False, key="-skin_rarity3-", enable_events=True),
]

layout = [ 
    winrate_arr,
    hero_rarity,
    skin_rarity,
    [sg.Text("Daily Expect profit: "),sg.Text("",key="expect_profit")],
    [sg.Text("Total Expect profit: "),sg.Text("",key="total_profit")],
    [sg.Text("Duration: "),sg.Text("",key="duration")],
]
window = sg.Window('Thetan Arena Caculator', layout)
THC_prices = 0.25

def playduration(herorarity,skin):
    min = hero[herorarity][skin]["min_gthc"] / hero[herorarity]["daily_battles"]
    max = hero[herorarity][skin]["max_gthc"] / hero[herorarity]["daily_battles"]
    return min ,max

def totalearn(herorarity,winrate):
    winrate = float(winrate)
    if not (0 <= winrate <= 1):
        return -1
    
    if herorarity in ['common_hero','epic_hero','legendary_hero']:
        round_earn = hero[herorarity]["win_bonus"]*winrate + (1-winrate)
        min = round_earn*hero[herorarity]["normal"]["min_gthc"]
        max = round_earn*hero[herorarity]["normal"]["max_gthc"]
        return min, max
    else:
        return -1

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
    winrate = .5
    hero_rarity = "common_hero"
    skin_rarity = "normal"


    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif values["-hero_rarity1-"] == True:
            hero_rarity = "common_hero"
        elif values["-hero_rarity2-"] == True: 
            hero_rarity = "epic_hero"
        elif values["-hero_rarity3-"] == True:
            hero_rarity = "legendary_hero"

        if event == sg.WIN_CLOSED:
            break
        elif values["-skin_rarity1-"] == True:
            skin_rarity = "normal"
        elif values["-skin_rarity2-"] == True: 
            skin_rarity = "rare"
        elif values["-skin_rarity3-"] == True:
            skin_rarity = "mythic"
        
        if isfloat(values['-winrtate-']):
            winrate = values['-winrtate-']

        min_earn, max_earn = totalearn(hero_rarity,winrate)
        min_dur, max_dur = playduration(hero_rarity,skin_rarity)
        window.Element('expect_profit').update(dailyearn(hero_rarity,winrate))
        window.Element('total_profit').update(f"{min_earn} - {max_earn}")
        window.Element('duration').update(f"{min_dur} - {max_dur}")

    window.close()

if __name__ == "__main__":
    main()
    