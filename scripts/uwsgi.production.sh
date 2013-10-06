#!/bin/bash
source ../bin/activate
source tokens
exec uwsgi --uid=app --gid=app --chdir=/var/apps/wastingtimer/ --module=wastingtimer.wsgi:application --env  DJANGO_SETTINGS_MODULE=wastingtimer.settings --socket=127.0.0.1:8001 --master --die-on-term --pidfile=/tmp/minuteswasted.pid --processes=2 --harakiri=20 --max-requests=5000 --vacuum --stats 127.0.0.1:1717