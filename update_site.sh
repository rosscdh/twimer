#/bin/bash
echo "Pulling changes"
git pull
echo "Chmodding"
chown -R app .
echo "Reloading uWSGI server"
kill -HUP `cat /tmp/minuteswasted.pid`