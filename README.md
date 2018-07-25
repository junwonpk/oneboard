## Setting Up on Your Local Machine
```
git clone https://github.com/junwonpk/oneboard
cd oneboard

conda create -n "oneboard" python=2.7 anaconda
source activate oneboard

pip install slackbot
python run.py
```

## Message Routing
See oneboard/oneboard.py to see which messages the slack bot is handling and how.

## Adding New Features
Keep oneboard/oneboard.py concise by writing as much of your addition as separate classes as possible. See class definition in oneboard/user.py and use of User class in oneboard/oneboard.py as an example.

## Testing Slack Bot
Log in to microsoftoneboard.slack.com then open a new DM chat with the app "Oneboard". Then send it some messages!

## Backlog
1. Bring IntentClassifier in.
2. Instead of chapter+=1 to advance, check for user.thingsToTeach, until it becomes empty.
