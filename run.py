import requests
import time
import optparse
import datetime
import json
import pause

# ID_APPLICATION = 81560887

def login(session, account, password):
    headers = {
        'authority': 'sport.nubapp.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://sport.nubapp.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://sport.nubapp.com/web/index.php',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
        'username': account,
        'password': password
    }

    return session.post('https://sport.nubapp.com/web/ajax/users/checkUser.php', headers=headers, data=data)


def get_slots(session, start_timestamp, end_timestamp, now_timestamp):
    
    headers = {
        'authority': 'sport.nubapp.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://sport.nubapp.com/web/index.php',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('id_category_activity', '677'),
        ('offset', '-120'),
        ('start', start_timestamp),
        ('end', end_timestamp),
        ('_', now_timestamp),
    )

    return session.get('https://sport.nubapp.com/web/ajax/activities/getActivitiesCalendar.php', headers=headers, params=params)


def book(session, id_activity_calendar):

    headers = {
        'authority': 'sport.nubapp.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://sport.nubapp.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://sport.nubapp.com/web/index.php',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
        'items[activities][0][id_activity_calendar]': id_activity_calendar,
        'items[activities][0][unit_price]': '0',
        'items[activities][0][n_guests]': '0',
        'items[activities][0][id_resource]': 'false',
        'discount_code': 'false',
        'form': ''
    }

    return session.post('https://sport.nubapp.com/web/ajax/bookings/bookBookings.php', headers=headers, data=data)


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


def get_session_id(session, id_application):
    headers = {
        'authority': 'sport.nubapp.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'referer': 'https://sport.nubapp.com/web/setApplication.php?id_application=81560887',
        'accept-language': 'fr-FR,fr;q=0.9',
        'cookie': 'applicationId=%s' % id_application,
    }

    params = (
        ('id_application', id_application),
        ('isIframe', 'false'),
    )

    return session.get('https://sport.nubapp.com/web/cookieChecker.php', headers=headers, params=params)

def main(account, password, id_app):
    
    print(f"\n")
    print("=" * 100)
    print(f"[{account}] Running script on {str(datetime.datetime.now())}")

    ## Wait until 8pm
    d = datetime.datetime.today()
    d_wait = datetime.datetime(d.year, d.month, d.day, 11, 51)
    assert((d_wait - d).total_seconds() < 300)
    pause.until(d_wait)

    session = requests.Session()
    
    ## Login
    sess_id = get_session_id(session, id_app)
    res_login = login(session, account, password)

    # Build slots
    start_h, start_min, end_h, end_min = 11, 0, 14, 0 

    calendar = {}
    days = [('monday', 0), ('wednesday', 2), ('friday', 4)]
    for t in days:
        weekday = next_weekday(d, t[1])
        search_start = datetime.datetime(weekday.year, weekday.month, weekday.day, start_h, start_min)
        search_end = datetime.datetime(weekday.year, weekday.month, weekday.day, end_h, end_min)

        slots = get_slots(session, search_start.timestamp(),search_end.timestamp(), datetime.datetime.now().timestamp())
        slots = json.loads(slots.content)


        slots = [s for s in slots if '12:15:00' in s['start']]

        assert len(slots) == 1
        slot = slots[0]

        calendar[t[0]] = {
            'start' : slot['start'],
            'end' : slot['end'],
            'slot_id' : slot['id_activity_calendar']
        }

    # Booking
    for k, v in calendar.items():
        print(f"Booking for {k}, {v['start']} and {v['end']}")
        book_res = book(session, v['slot_id'])
        book_res = json.loads(book_res.content)
        print(json.dumps(book_res, indent=4, sort_keys=True))

if __name__ == "__main__":
  
    parser = optparse.OptionParser()

    parser.add_option('-e', '--account', action="store", dest="account")
    parser.add_option('-p', '--password', action="store", dest="password")
    parser.add_option('-i', '--id_app', action="store", dest="id_app")
   
    options, _ = parser.parse_args()
    
    main(options.account, options.password, options.id_app)
