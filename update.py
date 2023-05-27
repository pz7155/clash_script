import subprocess,yaml

# 下载订阅文件
url = ""
if not url:
    print("URL不能为空")
    raise SystemExit
subprocess.Popen(["curl", "-o", "config.yaml", url]).wait()

with open('parser.yaml', 'r', encoding='utf-8') as f:
    parser = yaml.safe_load(f)
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# prepend-proxy-groups:
config['proxy-groups']=parser['prepend-proxy-groups']+config['proxy-groups']

# append-proxy-groups:
config['proxy-groups'].extend(parser['append-proxy-groups'])

# prepend-rules:
config['rules']=parser['prepend-rules']+config['rules']

#commands:
#- proxy-groups.1.proxies.0+🚀 LB
config['proxy-groups'][1]['proxies'].insert(0, '🚀 LB')

proxyNames = []
groupNames = []
for proxy in config['proxies']:
    proxyNames.append(proxy['name'])
for group in parser['append-proxy-groups']:
    groupNames.append(group['name'])

def filter(group, keyword):
    group['proxies'] = [i for i in proxyNames if keyword in i]

for group in config['proxy-groups']:
    if group['name'] == '🚀 LB': #- proxy-groups.🚀 LB.proxies=[]groupNames|⚖️
        group['proxies'] = groupNames
    elif group['name'] == '⚖️ HK': #- proxy-groups.⚖️ HK.proxies=[]proxyNames|香港
        filter(group, '香港')
    elif group['name'] == '⚖️ TW': #- proxy-groups.⚖️ TW.proxies=[]proxyNames|台湾
        filter(group, '台湾')
    elif group['name'] == '⚖️ US': #- proxy-groups.⚖️ US.proxies=[]proxyNames|美国
        filter(group, '美国')

#good format
class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)

with open('config.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(config, f, Dumper=IndentDumper,allow_unicode=True,default_flow_style=False,sort_keys=False)

subprocess.call(['reboot.bat'])
