from __future__ import division
from collections import Counter

hamcount = Counter()
spamcount = Counter()

hamprob = {} # P(ham | word)
spamprob = {} # P(spam | word)

def train(messages):
    for msg in messages:
        if msg.is_spam:
            d = spamcount
        else:
            d = hamcount

        for rule in msg.spam_rules.split(','):
            d[rule] += 1
        for word in msg.msubject.split():
            d[word]  += 1

        d[msg.attachment_hash] += 1
        d[msg.attachment_name] += 1
        d[msg.source_ip] += 1
        d[msg.mfrom] += 1

        domain = msg.mfrom.rsplit("@")[-1]
        tld = domain.rsplit(".")[-1]
        d[domain] += 1
        d[tld] += 1

    words = sorted(set(hamcount).union(spamcount))
    for word in words:
        # P(ham | word) = P(word | ham) * P(ham) / P(word)
        #               = P(word & ham) / P(word)
        #               = (numham / totalwords) / (numham+numspam / totalwords)
        #               = numham / numham+numspam
        bothcount = hamcount[word] + spamcount[word]
        hamprob[word] = (1 + hamcount[word]) / (1 + bothcount)
        spamprob[word] = (1 + spamcount[word]) / (1 + bothcount)

def getprob(d, message):
    p = 1. # prior probability = .5
    q = 2.
    for rule in msg.spam_rules.split(','):
        if rule in d:
            r = d[rule]
            p *= r
            q *= 1-r
    for word in msg.msubject.split():
        if word in d:
            r = d[word]
            p *= r
            q *= 1-r

    if msg.attachment_hash in d:
        r = d[msg.attachment_hash]
        p *= r
        q *= 1-r

    if msg.attachment_name in d:
        r = d[msg.attachment_name]
        p *= r
        q *= 1-r

    if msg.source_ip in d:
        r = d[msg.source_ip]
        p *= r
        q *= 1-r

    if msg.mfrom in d:
        r = d[msg.mfrom]
        p *= r
        q *= 1-r

    return p / (p + q)

class Message(object): pass

def load_messages(filename):
    import csv
    messages = []
    with open(filename, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            msg = Message()
            msg.mid = row['mid']
            msg.is_spam = int(row['is_spam'])
            msg.spam_rules = row['spam_rules']
            msg.source_ip = row['source_ip']
            msg.mfrom = row['mfrom']
            msg.attachment_hash = row['attachment_hash']
            msg.attachment_name = row['attachment_name']
            msg.msubject = row['msubject']
            messages.append(msg)
    return messages


def main():
    import random

    message_data = load_messages('wow.csv')
    training_data = random.sample(message_data, 50000)
    train(training_data)

    for msg in message_data:
        p = getprob(spamprob, msg)
        q = getprob(hamprob, msg)
        if bool(msg.is_spam) != p > q:
            print msg.mid, msg.is_spam, p, q

main()
