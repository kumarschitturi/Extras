import sys
import os
import codecs
import re
import json

filepath = sys.argv[1]
# please provide class name in puppet manifest file.
pp_cls = 'class osuser::identity'
pp_fn = 'osuser::sshuser'
# list1 is list of keys which values are not enclosed in ''.
list1 = ['ensure']
#list 2 is list of keys which values are strings.
list2 = ['comment', 'uid']
#list3 containes keys which values are list type.
list3 = ['groups', 'environments', 'environments_with_sudo', 'sshkeys']


with open(filepath) as ff, open("input.pp", 'w') as p:
    for line in ff:
        if not line.isspace():
            p.write(line)

def covert_pp_to_json():
    with open('input.pp') as f, open("identity.json", 'w') as k:
        k.write('{\n')
        prev_line = ''
        cnt = 1
        for line in f:
            line = line.replace(',]', ']')
            if not line.isspace():
                if line.strip().startswith('#'):
                    if prev_line.strip().find('}') == -1:
                        k.write("\"user_comment"+str(cnt)+"\": \""+line.strip()+"\",\n")
                    else:
                        k.write("},\n\"user_comment"+str(cnt)+"\": \""+line.strip()+"\",\n")
                    cnt += 1
                    # print("Ignoring comments")
                elif line.strip().startswith(pp_cls):
                    k.write("\""+pp_cls+"\" : {\n")
                elif line.strip().startswith(pp_fn):
                    line = line.split('\'')[1]
                    if prev_line.strip().startswith("}"):
                        k.write("},\n\""+pp_fn+"\" : {\n\""+line+"\" : {\n")
                    else:
                        k.write("\""+pp_fn+"\" : {\n\""+line+"\" : {\n")
                elif any(line.strip().startswith(item) for item in list1):
                    line = line.replace(' ', '').replace('=>', ':').replace('\'', "\"")
                    k.write("\""+line.split(':')[0]+"\" : \""+line.split(':')[1].strip(',\n')+"\",\n")
                elif any(line.strip().startswith(item) for item in list2):
                    line = line.replace(' ', '').replace('=>', ':').replace('\'', "\"")
                    k.write("\""+line.split(':')[0]+"\" : "+line.split(':')[1].strip()+"\n")
                elif any(line.strip().startswith(item) for item in list3):
                    line = line.replace(' ', '').replace('=>', ':').replace('\'', "\"")
                    k.write("\""+line.split(':')[0]+"\" : "+line.split(':')[1].strip()+"\n")
                elif line.strip().startswith('}') and prev_line.strip().find("}") != -1:
                    k.write(line.strip(',\n')+"\n}\n}")
                else:
                    line = line.replace('=>', ':').replace('\'', '\"')
                    k.write(line)
            prev_line = line


def convert_json_to_pp():
    with open('input.pp') as f, open("identity_new.pp", 'w') as k:
        prev_line = ''
        for line in f:
            line = line.replace(',]', ']')
            if not line.isspace():
                if line.strip().startswith('{') and prev_line == '':
                    pass
                elif line.strip().find("user_comment") != -1:
                    k.write(line.strip('\"').split(':')[1].replace('"', "")+"\n")
                elif line.strip().find(pp_cls) != -1 or line.strip().find(pp_fn) != -1:
                    k.write(line.replace('"', '').strip())
                elif prev_line.strip().find(pp_fn) != -1:
                    k.write(line.replace('"', '\'').replace('{', ''))
                elif any(item in line.strip() for item in list1):
                    k.write(line.replace('"', '').replace(':', '=>'))
                elif any(item in line.strip() for item in list2) or any(item in line.strip() for item in list3):
                    k.write(line.split(':')[0].replace('"', '')+" =>"+line.split(':')[1].replace('"', '\''))
                elif line.strip().startswith('}') and prev_line.strip().find("}") != -1 and line.strip().find(",") == -1:
                    k.write(line.replace('}', ''))
                else:
                    line = line.replace('},', '')
                    k.write(line)
            prev_line = line
        k.write('}')


if __name__ == '__main__':
    if filepath.endswith('.pp'):
        print("[info] Provided puppet manifest as input, converting to json.")
        covert_pp_to_json()
        print("[info] coversion successful please find the json file in workspace.")
    elif filepath.endswith('.json'):
        print("[info] Provided json as input, converting to puppet format.")
        convert_json_to_pp()
        print("[info] coversion successful please find the pp file in workspace.")
    else:
        print("[error] script only supports files .pp or .json file types. exiting")
        exit()
