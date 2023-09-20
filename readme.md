# Evil Launcher
#### The most evil launcher ever conceived

Evil launcher is a CLI launcher for classic doom mod packs


## Usage

The `.hell` files should be formatted like this:

```
[WAD file]
{optional configuration file to use for the mod pack}
All your
mods ordered
in whatever
way you want
```

Usage of the script goes like this:
```
evillauncher.sh [.hell file] [path to your doom root folder]
```

To work, your directories should follow a specific folder structure.
```
Root/
    |WADs
    |mods
    |config
```
if you wanted to use subfolders to organize your mods, you'll have to add the relative path from `root` in the `.hell` file
