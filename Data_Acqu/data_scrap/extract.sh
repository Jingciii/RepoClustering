#!/bin/bash



user="$1"
repo="$2"

url="https://github.com/${user}/${repo}.git"

git clone $url
./linguist_script.sh "${repo}"


#linguist="${repo}"/linguistfiles.log


#for line in ` cat linguistfiles.log `
#for path in ` awk -F"[;]" '{ print $2 }' "${linguist}" `
#{
#	echo "$path"

#	pygmentize -f raw "${repo}"/"$path" | grep 'Token.Name' >> "${user}"_"${repo}"_token_name
	
#}

