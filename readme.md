# Evil Launcher
#### The most evil launcher ever conceived

Evil launcher is a CLI launcher for classic doom mod packs


## Requirements

- Python
- gzdoom
- wget
- unar

## Usage

Usage of the script goes like this:

```
evil [.hell file]
```

## Format Definition

The `.hell` files should be formatted like this:

```
[WAD file]
{optional configuration file to use for the mod pack}

-- You can also make comments!

-- if you want to fetch from the internet
www.example.com as /output/wads/example.pk3

-- in case you want the file to be extracted after download
www.examplezip.com as /output/mods/%%examplezip%%/mod.pk3
-- Here, %%this%% means "extract to this folder", which can be new or an
-- existant folder

-- You can also check hashes on downloads
www.totallysafe.com as /output/mods/%%notavirus%%/virus.pk3 with sha256 9c2f6a794acac9d5cbc2ebcd456ab6d0d6f452c97765fe315b10a9347a021adf

All your
mods ordered
in whatever
way you want
```

The hashes currently implemented are `sha256`, `md5` and `sha1`.

All files you reference in it, have to have relative paths to the `.hell` file.
