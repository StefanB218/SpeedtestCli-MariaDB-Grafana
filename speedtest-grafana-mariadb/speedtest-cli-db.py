#!/usr/bin/env bash

# Character for separating values
# (commas are not safe, because some servers return speeds with commas)
#speedtestserver=2495
mariadblogin=name
mariadbpassword=pw
mariadbdb=db_name

#Temporary file holding speedtest-cli output
user=$USER
if test -z $user; then
  user=$USERNAME
fi
log=/tmp/$user/speedtest-mysql.log
#log=/tmp/speedtest-mariadb.log
## Local functions
str_extract() {
 pattern=$1
 # Extract
 res=`grep "$pattern" $log | sed "s/$pattern//g"`
 # Drop trailing ...
 res=`echo $res | sed 's/[.][.][.]//g'`
 # Trim
 res=`echo $res | sed 's/^ *//g' | sed 's/ *$//g'`
 echo $res
}

mkdir -p `dirname $log`

start=`date +"%Y-%m-%d %H:%M:%S"`

echo "Speedtest started at : $start"

# Query Speedtest
#/usr/local/bin/speedtest-cli --server $speedtestserver --share > $log
/usr/local/bin/speedtest-cli --share > $log
stop=`date +%s`

# Parse
from=`str_extract "Testing from "`
from=`echo $from | sed 's/ (.*//g'`
server=`str_extract "Hosted by "`
server_ping=`echo $server | sed 's/.*: //g'`
server=`echo $server | sed 's/: .*//g'`

download=`str_extract "Download: "`
upload=`str_extract "Upload: "`
share_url=`str_extract "Share results: "`

# Send to Local mariadb

server_ping=`echo $server_ping | cut -d" " -f1`
download=`echo $download | cut -d" " -f1`
upload=`echo $upload | cut -d" " -f1` 

sql="INSERT INTO data (ping,dl,ul,url) VALUES ('$server_ping','$download','$upload','$share_url');"
echo "$sql" | mariadb -u$mariadblogin -p$mariadbpassword $mariadbdb
