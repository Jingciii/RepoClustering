#!/bin/bash

start=`date +%s`

read -p "Enter the repos list collect data from: " repos_list


#for x in ` awk '{print}' $repos `
for x in ` cat $repos_list ` 
{
user="$(cut -d'/' -f1 <<<"$x")"
repo="$(cut -d'/' -f2 <<<"$x")"
bash extract.sh "$user" "$repo" 
if [ ! -s "${repo}/linguistfiles.log" ]
then
	echo "***** No source code found in ${x} *********"
	rm -rf $repo 
	echo "***** ${repo}'s directory has been removed *******"
else

	python parse_token.py "$user" "$repo"

	echo "*********** ${x} has been collected **************"

	rm -rf $repo 
	echo "***** ${repo}'s directory has been removed *******"
fi
} 


end=`date +%s` 
dif=$[ end - start ]

echo "RunTime: $dif seconds"