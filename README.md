You input a deadline and a timeframe for reminders; the script
schedules a sequence of email reminders to be sent at ever-shorter
time intervals, until the deadline is reached. You'll need a Mailgun
account for this.

Due to limitations inherent in Mailgun, the current version has two
quite damning drawbacks: you can only set deadlines less than 72
hours into the future, and there is no way to recall scheduled emails,
so you can't reply 'DONE' or equivalent to cancel the email reminders.

Inspired by Beeminder's [Zeno Polling](http://blog.beeminder.com/zeno/) feature.

# Instructions

0. Clone the repository to your machine.
1. Set up a Mailgun account.
2. Go to settings-sample.py, change what needs changing, and save the
file as settings.py.
3. Run `python zeno.py` and follow the instructions.