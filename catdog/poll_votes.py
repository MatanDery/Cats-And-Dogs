from time import sleep
from catdog import r

def update_votes(voted, req_ip):
    sleep(2)
    if vote_check(req_ip) != 0:
        r.set(voted, int(r.get(voted)) + 1)
    return


def vote_check(req_ip):
    x = r.sadd('voted_ip', req_ip)
    return x
