import sys
import os
import codecs
import re

filepath = sys.argv[1]

with open(filepath) as ff, open("/Users/kumaraswamychitturi/development/input.pp", 'w') as p:
    for line in ff:
        if not line.isspace():
            p.write(line)

with open('input.pp') as f, open("/Users/kumaraswamychitturi/development/output.json", 'w') as k:
    k.write('{\n')
    prev_line = ''
    cnt = 1
    for line in f:
        line = line.replace(',]', ']')
        if not line.isspace():
            if line.strip().startswith('#'):
                if prev_line.strip().find('}') == -1:
                    k.write("\"comment"+str(cnt)+"\": \""+line.strip()+"\",\n")
                else:
                    k.write("},\n\"comment"+str(cnt)+"\": \""+line.strip()+"\",\n")
                cnt += 1
            elif line.strip().startswith('class osuser::identity'):
                k.write("\"class osuser::identity\" : {\n")
            elif line.strip().startswith('osuser::sshuser'):
                line = line.split('\'')[1]
                if prev_line.strip().startswith("}") != -1:
                    k.write("},\n\"osuser::sshuser\" : {\n\""+line+"\" : {\n")
                else:
                    k.write("\"osuser::sshuser\" : {\n\""+line+"\" : {\n")
            elif line.strip().startswith('ensure'):
                line = line.replace(' ', '').replace('=>', ':').replace('\'', "\"")
                k.write("\""+line.split(':')[0]+"\" : \""+line.split(':')[1].strip(',\n')+"\",\n")
            elif line.strip().startswith('comment') or line.strip().startswith('uid'):
                line = line.replace(' ', '').replace('=>', ':').replace('\'', "\"")
                k.write("\""+line.split(':')[0]+"\" : "+line.split(':')[1].strip()+"\n")
            elif line.strip().startswith('groups') or line.strip().startswith('environments') or line.strip().startswith('environments_with_sudo') or line.strip().startswith('sshkeys'):
                line = line.replace(' ', '').replace('=>', ':').replace('\'', "\"")
                k.write("\""+line.split(':')[0]+"\" : "+line.split(':')[1].strip()+"\n")
            # elif line.strip().startswith('}') and ( prev_line.strip().find("]") != -1 or line.strip().find(']') != -1 ):
            #     k.write(line.strip('\n')+"\n},\n")
            elif line.strip().startswith('}') and prev_line.strip().find("}") != -1:
                k.write(line.strip(',\n')+"\n}\n}")
            else:
                line = line.replace('=>', ':').replace('\'', '\"')
                k.write(line)
        prev_line = line

# with open('output.json') as c, open('identity.json', 'w') as d:
#     p_line = ''
#     for line in c:
#         if not line.isspace():
#             if line.strip().startswith('},') and p_line.strip().find("}") != -1:
#                 d.write(line.strip(','))
#             else:
#                 d.write(line)
#         p_line = line




# def parse(data):
#     mm = re.search('\((.*?)\)', data,re.MULTILINE)
#     dd = {}
#     if not mm:
#         return dd
#     matches = re.finditer("\s*\$(.*?)\s*=\s*'(.*?)'", mm.group(1), re.MULTILINE)
#     for mm in matches:
#         dd[mm.group(1)] = mm.group(2)
#     return dd
#
# def main():
#     with codecs.open(filepath,'r') as ff:
#         dd = parse(ff.read())

   # if not os.path.isfile(filepath):
   #     print("File path {} does not exist. Exiting...".format(filepath))
   #     sys.exit()
   #
   # bag_of_words = {}
   # with open(filepath) as fp:
   #     print("fp:", fp)
   #     for line in fp:
   #         print("{}".format(line))
#    sorted_words = order_bag_of_words(bag_of_words, desc=True)
#    print("Most frequent 10 words {}".format(sorted_words[:10]))
#
# def order_bag_of_words(bag_of_words, desc=False):
#    words = [(word, cnt) for word, cnt in bag_of_words.items()]
#    return sorted(words, key=lambda x: x[1], reverse=desc)
#
# def record_word_cnt(words, bag_of_words):
#    for word in words:
#        if word != '':
#            if word.lower() in bag_of_words:
#                bag_of_words[word.lower()] += 1
#            else:
#                bag_of_words[word.lower()] = 1


# if __name__ == '__main__':
#    main()
