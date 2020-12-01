project_data = open('project_twitter_data.csv')

punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']
positive_words = []
with open("positive_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            positive_words.append(lin.strip())
negative_words = []
with open("negative_words.txt") as neg_f:
    for lin in neg_f:
        if lin[0] != ';' and lin[0] != '\n':
            negative_words.append(lin.strip())


def strip_punctuation(arg):
    for i in punctuation_chars:
        arg = arg.replace(i, '')
    return arg


def get_pos(arg):
    count = 0
    for i in arg.split():
        i = strip_punctuation(i.lower())
        if i in positive_words:
            count += 1
    return count


def get_neg(arg):
    count = 0
    for i in arg.split():
        i = strip_punctuation(i.lower())
        if i in negative_words:
            count += 1
    return count


with open('resulting_data.csv', 'a') as resulting_data:
    resulting_data.write('Number of Retweets,Number of Replies,Positive Score,Negative Score,Net Score\n')
    for i in project_data.readlines()[1:]:
        i = i.split(',')
        pos = get_pos(i[0])
        neg = get_neg(i[0])
        resulting_data.write('{},{},{},{},{} \n'.format(i[1].strip(), i[2].strip(), pos, neg, pos - neg))
project_data.close()
