# Rosneft Simulator
[MIT License](LICENSE)

## Description

Welcome to the Rosneft Simulator, a game developed for PyWeek 37 with the theme "tubes". This game is set in Russia and you play as [Rosneft](https://en.wikipedia.org/wiki/Rosneft), a large company responsible for a [significant portion of the country's oil production](https://en.wikipedia.org/wiki/Petroleum_industry_in_Russia). The goal of the game is to export and sell all the oil from Russia and get rich.

## How to run the game:
The game needs pygame and python to run.

0) (essential) Install [python 3.8 or above](https://www.python.org/downloads/)
1) clone the repository or download a .zip file from github.\
`git clone https://BUSH222/rosneft_simulator`
2) Install the requirements of the game: (if you are on mac, use python3 instead of python, some windows versions use py instead of python)\
`python -m pip install -r /path/to/requirements.txt`\
OR\
`python -m pip install pygame==2.5.2`
3) Run main.py using python: (if you are on mac, use python3 instead of python)\
`python /path/to/main.py`

Tested on MacOS v14.4 and Windows 10/11.\
It is preferrable to run this on a machine with a display aspect ratio of 16:9.

## Gameplay

In this game, Rosneft is the only company and spawns on a random [oil reservoir](https://en.wikipedia.org/wiki/Petroleum_reservoir). There is also an export pipe on the bottom or left side of Russia. Any oil that flows into this pipe gets exported and is directly converted into money.

As a player, you have four options (right menu):

1. **Buy Land**: Oil rigs can only be built on bought land.
2. **Survey Land**: Find oil on which to build the oil rigs.
3. **Build Pipe**: Build and sell pipes to export the oil.
4. **Build Oil Rig**: Build an oil rig to start drilling for oil.

At the top there are information panels:
1. **Oil percentage** - how much oil Russia still has left.
2. **Budget** - how much money your company still has
3. **Net income** - how much money your company is making.

Every placed object and bought land require upkeep. Every action costs some money. Oil reservoirs have a certain amount of oil in them and they run out over time.

## Tutorial

Color scheme:
- oil: grey colored tiles, only visible after being bought and surveyed
- buy land: When selecting buying land, you can select a square on the map to buy. When selecting that square, the prices of tiles will appear yellow in color. The darker the yellow, the less expensive it is. Grey tiles mean that part of the map was already bought.
- survey land: same as buy land, but the price to survey the land is the same for every tile, except bought tiles.
- build rigs and pipes: when first building pipes or rigs, a preview will appear. If the preview is red, you can't place pipes or a rig. If it is green - you can.
- Export pipe - a black tile with a yellowish pipe on it will generate randomly somewhere on the left or bottom side of Russia.

Here's a quick start guide to playing the game:

1. Start by placing one or several oil rigs on the grey colored tiles.
2. Connect them to the export pipe (remember, the export pipe is a black tile somewhere on the left or bottom side of Russia)
3. Expand by buying more land. Click on 'Buy Land' and expand your territory.
4. Once you've bought the land, you can survey it to find oil. Click on the 'Survey Land' button and then select a square of bought land you want to survey.
5. Repeat until the percentage of oil at the top left (the total oil Russia has left) hits 0!

Remember, every action costs money and every object and bought land require upkeep, so manage your resources wisely!

## Common questions (Q&A)
> Q: I started the game, but cannot build anything, why??\
A: At the start of the game, before the player bought anything the player can only build rigs on the already discovered oil (given at the start, look out for gray tiles). 

> Q: What to connect my rigs to? Where is the export pipe?\
A: You should connect your rigs with pipes to the export pipe. The export pipe is a yellow pipe on a black tile somewhere at the bottom or left of the map (hint: use the arrow keys to move the map around)

> Q: How to buy and survey tiles?\
A: You can buy and survey tiles by selecting **Buy land** or **Survey** from the menu on the right. When one of them is selected, click one tile, then a preview should appear. Then, select a second tile and a square will be bought.
Here's an example ![Alt Text](/readme-pics/buy_land.gif)

> Q: How to view bought and surveyed tiles?\
A: To avoid clutter on the map, we decided that you will be able to see bought tiles only when enter buy land or survey mode. So, enter buy or survey mode and select a large square around where you want to see the bought land. The bought land will be gray, whereas the non-bought will be a shade of yellow (depending on its price.) Same for the surveyed land, but the colors will be a bit different.

> Q: How to demolish/destroy pipes and rigs?\
A: To demolish pipes, press **Build pipes** from the right menu and right click the 2 points. A pipe preview will appear. If you use right click instead of left click, the pipes in the path will be demolished. Same is true for rigs.

> Q: I am negative on money, what do I do??\
A: Every single bought tile, placed pipe and placed oil rig require upkeep, especially the oil rigs. If you are low on money, try to demolish the rigs to reduce your upkeep. This should get you out of debt.

## Team members
This project was completed by first-year IT and Computer Science students from NUST MISIS.
- github: **[BUSH222](https://github.com/BUSH222)** discord: **@bush22** | Team lead, Game logic
- github: **[ShagDasha10](https://github.com/Dashaht)** telegram: **@ShagDasha** | UI/UX Design
- github: **[ponypedro2005](https://github.com/ponypedro2005)** telegram: **@ponypedro2005** | Asset design, QA/QC

Honourable mention:
- github **[allhorrorshow](https://github.com/Maximkapp)** telegram: **@Allhorrorshow**

## Conclusion

We hope you enjoy playing Rosneft Simulator and get a glimpse into the world of oil production and export. Good luck and have fun!