# Evil Launcher
#### The most evil launcher ever conceived

Evil launcher is a CLI launcher for classic doom mod packs


## Usage

The `.hell` files should be formatted like this:

```
[WAD file]
{configuration file to use for the mod pack}
All your
mods ordered
in whatever
way you want
# You can also make comments!
```

Usage of the script goes like this:

```
evil [.hell file]
```

if no [path] is given, it'll use the parent folder of the `.hell` file as the root. Useful for self-contained mod packs!

if you wanted to use subfolders to organize your mods, you'll have to add the relative path from `root` in the `.hell` file
