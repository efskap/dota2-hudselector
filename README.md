Replaces the default HUD with any other HUD in the game. Completely legal, as it simply extracts data from Dota 2's own game files and then mods it back in.

Uses the excellent [HLExtract tool](http://nemesis.thewavelength.net/index.php?p=35).

Requirements
===

- Python 3

So far I only have automatic installation location detection for Windows, but if you manually specify the path to Steam as an argument, it should work on Linux too.


Instructions
===
Run main.py with python 3, pick your HUD, and then choose "Default HUD" from the shared content menu in-game.

To restore the original HUD, just delete this folder:

    Steam\steamapps\common\dota 2 beta\dota\resource\flash3\images\hud_skins\default

Screenshots
===
![](http://i.imgur.com/tn6PvKj.png)
![](http://i.imgur.com/u4llyqY.jpg)
