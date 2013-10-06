#/bin/bash
sleep 5

cd /var/apps/wastingtimer
source ../bin/activate
source tokens
./manage.py fetch_mentions
./manage.py fetch_direct_messages