twimer
======

GPL v3. A simple twitter based time recorder - good for contractors and recording wasted or invested time

```
pip install virtualenv virtualenvwrapper : http://virtualenvwrapper.readthedocs.org/en/latest/
pip install -r requirements.txt
python mange.py syncdb
```

Add these key=value to your settings.py 

or RATHER (more secure) export as env vars

## For the public api and people using the service

```export TWITTER_CONSUMER_KEY=''```
```export TWITTER_CONSUMER_SECRET=''```
```export TWITTER_ACCESS_TOKEN=''```
```export TWITTER_ACCESS_TOKEN_SECRET=''```

## For the internal consumer service

```export MINUTESWASTEDAPP_TWITTER_CONSUMER_KEY=''```
```export MINUTESWASTEDAPP_TWITTER_CONSUMER_SECRET=''```
```export MINUTESWASTEDAPP_TWITTER_ACCESS_TOKEN=''```
```export MINUTESWASTEDAPP_TWITTER_ACCESS_TOKEN_SECRET=''```

# Start server
python manage.py runserver_plus

# Fetch mentions
python manage.py fetch_mentions

# Fetch direct messages
python manage.py fetch_direct_messages
