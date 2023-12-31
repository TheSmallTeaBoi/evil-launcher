#!/bin/sh

if [ $2 ]; then
	path="$2"
else
	path="$(dirname $1)/"	
fi

wad_folder=$path/WADs/
mod_folder=$path/mods/
config_folder=$path/config/

usage='Evil Launcher Usage
-h, --help             show this message
----------------------------------------
'$0' [modpack file] [doom root path]
For a more detailed explanation, check `readme.md`
'

# Help
if [[ "$#" -ne 1 ]] || [[ $1 == '-h' ]] || [[ $1 == '--help' ]]; then
    echo "$usage"
    exit 1
fi

# Read the .hell file passed as an argument
read_file(){
	echo "Reading $1"
	hellcat=$(cat $1)
}

# Get the .wad file out of the .hell file
get_wad(){
	echo "Getting WAD name"
	wad=$(echo $hellcat | sed 's/.*\[(.*?)\].*/\1/' -r)
	echo "WAD name is $wad"
	echo "WAD location is $path$wad"
}

# Get the config file name (or make one if it doesn't exist)
get_config(){
	echo "Getting config file"
	config_path="$(echo ${hellcat} | sed 's/.*\{(.*?)\}.*/\1/' -r)"
	if echo "${config_path}" | grep -E -q '.*\.config'; then
		echo "{$config_path} is specificied, using it"
		config_file="$config_path"
	else
		echo "Config file not specified, making base64 hash"
		config_hash=$(base64 $1)
		echo "the config hash is $config_hash"
		config_file="$config_hash.config"
	fi
}

# Get the rest of the files (the mods :P)
get_mods(){
	echo "Getting the mod filepaths"
	mods_string=$(cat $1 | sed -r 's/^[.*\#|.*\[|.*{.*].*//')
	mod_array=($mods_string)
	echo "There are ${#mod_array[@]} mods:"
	for key in "${!mod_array[@]}"
	do 
		echo "    ${mod_array[key]}"
		mod_array_with_path[key]="$mod_folder/${mod_array[key]}"
	done
}

read_file $1
get_wad $hellcat
get_config $1
get_mods $1

#echo "running gzdoom -iwad $wad_folder/$wad -config "$config_folder/$config_file" -file ${mod_array_with_path[@]}" # For debugging purposes
echo -ne "Running gzdoom\n\n"
gzdoom -iwad "${wad_folder:?}/$wad" -config "${config_folder:?}/$config_file" -file "${mod_array_with_path[@]}"
