## Core implementation of Zeno reminders

import requests
import time
import sys
from email.utils import formatdate
from datetime import datetime

import settings

def schedule_reminder(task, delivery_time, next_time, deadline, remaining):
  body_nonfinal = '''This is a Zeno reminder for the following task:
\n%s (due %s)
\nThe next reminder will be sent %s. If you complete the task by \
then, great! (But you'll still get all the remaining %s reminders, \
sorry...)
\n
-
Sent with Zeno Reminders (http://github.com/alexschell/zeno)''' %(
  task, deadline, next_time, remaining)
  
  body_final = '''This is a Zeno reminder for the following task:
\n%s
\nThis task is due NOW, and this is your final reminder!
\n
-
Sent with Zeno Reminders (http://github.com/alexschell/zeno)''' % task
  
  if delivery_time == deadline:
    body = body_final
  else:
    body = body_nonfinal
  
  return requests.post(
    'https://api.mailgun.net/v2/%s/messages' % settings.domain,
    auth=('api', settings.auth_key_mg),
    data={'from': 'Zeno Bot <%s>' % settings.bot_email,
          'to': [settings.my_email],
          'subject': 'Zeno reminder for %s' % task,
          'text': body,
          'o:deliverytime': delivery_time})

def date_string(timestamp):
  return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

#def time_string(timestamp):
#  return datetime.fromtimestamp(timestamp).strftime('%H:%M')

def timestamp(date_str, time_str):
  return time.mktime(time.strptime(' '.join([date_str, time_str]), '%Y-%m-%d %H:%M'))

def datetime_string(timestamp):
  return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

# Read task
confirm = ''
while not(confirm == 'y' or confirm == 'yes'):
  valid = False
  while not valid:
    task = raw_input('Enter a short task description (< 100 characters): ')
    if len(task) > 0 and len(task) < 100:
      valid = True
  print 'Confirm task description \'%s\' (y/n): ' % task,
  confirm = raw_input().lower()

# Read deadline
current_time = time.time()
opts = [current_time + 24 * 3600 * x for x in range(4)]
opts = [timestamp(date_string(x), '12:00') for x in opts]
opts = [date_string(x) for x in opts]
print 'Now enter the deadline for the task. ',
print 'This will be the time your last reminder is sent. '
confirm = ''
while not(confirm == 'y' or confirm == 'yes'):
  valid = False
  while not valid:
    print 'Choose the date (enter one of 1...4):'
    print '(1) %s (today)' % opts[0]
    print '(2) %s' % opts[1]
    print '(3) %s' % opts[2]
    print '(4) %s' % opts[3]
    try:
      choice = int(raw_input()) - 1
      valid = choice in range(4)
      dl_date = opts[choice]
    except:
      pass
  
  valid = False
  while not valid:
    print 'Enter the time (hh:mm in 24 h format) ',
    print 'or RETURN to default to noon: ',
    dl_time = raw_input()
    try:
      valid = len(dl_time) in [4, 5]
      valid = valid and int(dl_time[:2]) in range(23)
      valid = valid and int(dl_time[-2:]) in range(59)
      dl_timestamp = timestamp(dl_date, dl_time)
      too_far = dl_timestamp > current_time + 70 * 3600
      too_soon = dl_timestamp <= current_time + 3600
      # valid = valid and not too_far and not too_soon
      if too_far:
        print 'Deadline must be less than 70 hours from now!'
      if too_soon:
        print 'Deadline must be at least one hour from now!'
    except:
      pass
    #handle defaulting
  print 'Deadline OK? %s (y/n): ' % formatdate(dl_timestamp, localtime = True),
  confirm = raw_input().lower()

# Read timeframe
opts = [1, 4, 12, 24]
opts_str = ['(1) 1 hour: 60 min, 30, 15, 7.5 ...',
            '(2) 4 hours: 4 h, 2, 1, 30 min ...',
            '(3) 12 hours: 12 h, 6, 3, 1.5 ...',
            '(4) 24 hours: 24 h, 12, 6, 3 ... ']
dl_hours = (dl_timestamp - current_time) / 3600
opts_indices = [index for index,value in enumerate(opts) if
                value <= dl_hours]
confirm = ''
while not(confirm == 'y' or confirm == 'yes'):
  valid = False
  while not valid:
    print 'Choose the date (enter one of 1...):'
    for i in opts_indices:
      print opts_str[i]
    try:
      choice = int(raw_input()) - 1
      valid = choice in opts_indices
      timeframe = opts[choice]
    except:
      pass
  print 'Confirm %s h timeframe (y/n): ' % timeframe
  confirm = raw_input().lower()

# Compute delivery time sequence
zeno = [timeframe * 3600 * pow(settings.rate, x) for x in range(settings.Nmax)]
zeno = [x for x in zeno if x > settings.dmax]
times = [dl_timestamp - x for x in zeno]
times.append(dl_timestamp)
print times  # debug

# Confirmation
print 'Confirm sending of Zeno reminders to %s ' % settings.my_email,
print '(enter y to continue, anything else to exit): ',
confirm = raw_input()
if confirm != 'y':
  sys.exit(0)

# Scheduling
deadline = datetime_string(dl_timestamp)
for i in range(len(times) - 1):
  delivery_time = formatdate(times[i])
  next_time = datetime_string(times[i+1])
  remaining = len(times) - i - 1
  schedule_reminder(task, delivery_time, next_time, deadline, remaining)

schedule_reminder(task, formatdate(times[-1]), None, None, None)

print 'Scheduled %s email reminders.' % len(times)
