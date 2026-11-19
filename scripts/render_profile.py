"""Original animated profile art. Python standard library; public GitHub data only."""
from collections import defaultdict
from datetime import date, datetime, timezone
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'lab'
USER = os.environ.get('PROFILE_USERNAME', 'luan0217091310-gif')
if not re.fullmatch(r'[A-Za-z0-9-]+', USER):
    raise ValueError('Invalid GitHub username')
BG, PANEL, LINE = '#101e29', '#19313b', '#2c4650'
CREAM, MINT, CORAL, GOLD, MUTED = '#f2ead9', '#89d9bf', '#ee927e', '#edc481', '#a1b5b7'
MONO = 'Consolas, Menlo, monospace'
SANS = '-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif'
CSS = '''
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
@keyframes blink{0%,43%,47%,100%{transform:scaleY(1)}45%{transform:scaleY(.12)}}
@keyframes shimmer{0%,100%{opacity:.25}50%{opacity:1}}
@keyframes steam{0%{opacity:0;transform:translateY(3px)}30%{opacity:.65}100%{opacity:0;transform:translateY(-18px)}}
@keyframes cursor{50%{opacity:0}}
@keyframes notes{0%{opacity:0;transform:translate(0,8px)}25%{opacity:1}100%{opacity:0;transform:translate(10px,-28px)}}
@keyframes scan{from{transform:translateX(0)}to{transform:translateX(904px)}}
@keyframes scan-mobile{from{transform:translateX(0)}to{transform:translateX(424px)}}
@keyframes signal{0%{stroke-dashoffset:260}100%{stroke-dashoffset:0}}
.bob{animation:bob 4s ease-in-out infinite}.blink{transform-box:fill-box;transform-origin:center;animation:blink 6s infinite}
.twinkle{animation:shimmer 3s ease-in-out infinite}.cursor{animation:cursor 1s steps(1) infinite}
.steam{animation:steam 3s ease-out infinite}.note{animation:notes 4s ease-in-out infinite}
.signal{stroke-dasharray:18 242;animation:signal 7s linear infinite}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.steam,.note{opacity:.6}}
'''

def rect(x,y,w,h,fill,r=0,stroke=None,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+f' {extra}/>'

def text(x,y,value,size=16,color=CREAM,weight=400,mono=False,extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" font-family="{MONO if mono else SANS}" {extra}>{escape(str(value))}</text>'

def path(d,color=LINE,width=1,fill='none',extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'

def circle(x,y,r,fill,extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {extra}/>'

def group(content,x=0,y=0,scale=1,extra=''):
    return f'<g transform="translate({x} {y}) scale({scale})" {extra}>{content}</g>'

def pill(x,y,label,accent=MINT,width=None):
    width=width or len(label)*7+24
    return rect(x,y,width,28,PANEL,14,LINE)+text(x+12,y+19,label,11,accent,600,True)

def shell(w,h,title,content,desc=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h+12}" viewBox="0 0 {w} {h+12}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc or title)}</desc><style>{CSS}</style>'
            +rect(.5,.5,w-1,h-1,BG,18,LINE)+content+'</svg>')

def robot():
    body=rect(7,8,48,42,CREAM,12)+rect(13,19,36,19,BG,7)
    body+='<g class="blink">'+circle(23,28,3.2,MINT)+circle(39,28,3.2,MINT)+'</g>'
    body+=path('M27 35 Q31 38 35 35',MINT,1.5)
    body+=path('M31 8 V1',GOLD,2)+circle(31,0,3,GOLD,'class="twinkle"')
    body+=rect(0,24,7,15,CORAL,3)+rect(55,24,7,15,CORAL,3)
    body+=rect(16,48,10,8,GOLD,3)+rect(38,48,10,8,GOLD,3)
    return '<g class="bob">'+body+'</g>'

def keyboard(x,y,w=150):
    s=rect(0,0,w,35,'#27404b',5)+rect(6,7,w-12,23,CREAM,2)
    for i in range(1,12):
        px=6+i*(w-12)/12
        s+=path(f'M{px:.1f} 7 V30',BG,.8)
        if i%7 not in (3,0):s+=rect(round(px-3,1),7,6,13,BG,1)
    s+=rect(7,26,(w-12)/12-1,4,MINT,1,extra='class="twinkle"')
    return group(s,x,y)

def scene():
    s=rect(0,0,420,332,'#142b34',16,LINE)
    s+=rect(172,21,220,151,'#0b1927',8,'#36535c')
    s+=circle(341,62,21,GOLD)+circle(350,55,19,'#0b1927')
    for i,(x,y) in enumerate([(196,39),(228,75),(283,46),(367,102),(310,113),(258,30),(201,118)]):
        s+=circle(x,y,1.6,CREAM,f'class="twinkle" style="animation-delay:{i*.47}s"')
    for x,y,h in [(183,132,24),(209,119,37),(238,137,19),(272,124,32),(306,138,18),(345,128,28),(373,139,17)]:
        s+=rect(x,y,18,h,'#233c49')+rect(x+5,y+7,3,4,GOLD)
    s+=path('M282 22 V170 M173 104 H391','#36535c',3)
    s+=rect(164,171,236,8,'#405859',3)
    s+=path('M56 0 V38',GOLD,2)+path('M34 57 L43 36 H69 L79 57 Z',GOLD,2,GOLD)
    s+=path('M36 63 L16 109 H98 L77 63',GOLD,1,extra='opacity=".13"')
    s+=text(23,134,'IDEAS / IN PROGRESS',9,MUTED,400,True)
    s+=rect(23,147,91,58,BG,5,LINE)
    for i,h in enumerate([12,27,18,34,23,15,30]):
        s+=rect(33+i*10,194-h,5,h,MINT if i%3 else CORAL,2,extra=f'class="twinkle" style="animation-delay:{i*.3}s"')
    s+=rect(25,263,374,12,'#bb9371',4)+rect(34,275,10,57,'#856e5d',2)+rect(379,275,10,57,'#856e5d',2)
    s+=rect(130,151,151,95,'#08151f',8,'#4e6870')+rect(137,158,137,78,'#132731',4)
    s+=circle(144,164,1.5,CORAL)+circle(151,164,1.5,GOLD)+circle(158,164,1.5,MINT)
    s+=text(149,184,'const curiosity =',10,MINT,400,True)
    s+=text(157,200,'"always on";',10,GOLD,400,True)
    s+=text(149,221,'build(something);',9,CREAM,400,True)
    s+=rect(250,211,5,11,CORAL,extra='class="cursor"')
    s+=rect(196,247,19,10,'#577278',2)+rect(178,257,55,5,'#7e9290',2)
    s+=keyboard(114,281,155)
    s+=circle(338,274,30,MINT,'opacity=".05"')+group(robot(),311,208,.82)
    s+=rect(283,245,16,19,GOLD,3)+path('M299 248 H304 Q310 254 300 259',GOLD,2)
    for i in range(3):
        s+=group(path('M0 0 Q-5 -4 0 -8 Q5 -12 0 -16',CREAM,1.5,extra=f'class="steam" style="animation-delay:{i}s"'),287+i*4,242)
    s+=path('M62 243 V211 M62 226 Q42 222 43 208 Q60 207 62 226 M63 232 Q83 229 83 214 Q67 216 63 232',MINT,2,MINT)
    s+=path('M47 240 H78 L73 262 H52 Z',CORAL,1,CORAL)
    s+=group(text(0,0,'♪',23,GOLD,600,extra='class="note"'),303,193)
    s+=group(text(0,0,'♫',18,MINT,600,extra='class="note" style="animation-delay:2s"'),363,204)
    return s

def hero(mobile=False):
    w,h=(480,650) if mobile else (960,420)
    s=circle(32,34,4,MINT,'class="twinkle"')+text(45,38,"LUÂN'S MIDNIGHT LAB",12,MINT,600,True)
    x=28 if mobile else 38
    s+=text(x,91 if mobile else 105,'PHÙNG HỮU LUÂN',16,MUTED,500,extra='letter-spacing="2"')
    sy=145 if mobile else 168
    s+=text(x,sy,'Curiosity,',46 if mobile else 48,CREAM,650)
    s+=text(x,sy+55,'turned into code.',43 if mobile else 47,CORAL,650)
    s+=text(x,sy+95,'Một chút code. Một chút nhạc.',17,CREAM)
    s+=text(x,sy+121,'Và rất nhiều điều muốn khám phá.',17,MUTED)
    if mobile:
        s+=group(scene(),30,312,1)
    else:
        s+=pill(x,325,'WEB APPS',width=94)+pill(x+104,325,'EXPERIMENTS',GOLD,118)+pill(x+232,325,'MUSIC + AI',CORAL,110)
        s+=group(scene(),508,48)
        s+=text(38,391,'BUILD. LEARN. REPEAT.',10,MUTED,400,True,extra='letter-spacing="1.6"')
    return shell(w,h,'Phùng Hữu Luân — Midnight Lab',s,'Góc làm việc ban đêm: robot chớp mắt, hơi trà, màn hình code, cửa sổ sao và những nốt nhạc chuyển động.')

def note_ui():
    s=rect(0,0,410,196,'#203641',10,'#456069')+rect(0,0,410,29,'#2b454e',10)
    s+=circle(15,14,3,CORAL)+circle(27,14,3,GOLD)+circle(39,14,3,MINT)+text(60,18,'notes / a place for ideas',10,MUTED,400,True)
    s+=rect(12,42,76,142,'#172c36',6)+text(23,61,'WORKSPACE',8,MUTED,600,True)
    for i,label in enumerate(['All notes','Ideas','Learning','Pinned']):
        if i==1:s+=rect(19,90,62,22,'#2b514e',3)
        s+=text(24,83+i*23,label,9,MINT if i==1 else CREAM)
    s+=text(104,62,'A small idea can go a long way.',11,CREAM,600)
    for i,(fill,title,rows) in enumerate([(GOLD,'A new idea',[53,75,40]),(MINT,'Learn by doing',[69,50,71]),(CORAL,'Next little build',[65,78,45])]):
        card=rect(0,0,89,101,fill,6)+text(9,21,title,8,BG,600)
        for j,length in enumerate(rows):card+=rect(9,35+j*12,length,3,BG,1,extra='opacity=".2"')
        card+=circle(72,86,5,BG,'opacity=".12"')
        s+=group(card,104+i*98,76)
    s+=circle(374,165,4,MINT,'class="twinkle"')
    return s

def note_card(mobile=False):
    w,h=(480,468) if mobile else (960,264)
    s=text(28,33,'01 / WEB APPLICATION',11,MINT,600,True)
    s+=text(28,80,'Note App',36,CREAM,650)
    s+=text(28,113,'Giữ ý tưởng. Kết nối người cùng làm.',17,CREAM)
    s+=text(28,143,'Ghi chú · cộng tác thời gian thực · ngoại tuyến',14,MUTED)
    s+=pill(28,166,'LARAVEL',MINT,92)+pill(130,166,'MYSQL',GOLD,78)+pill(218,166,'PWA',CORAL,60)
    if mobile:s+=group(note_ui(),25,237,1.05)
    else:
        s+=group(note_ui(),521,36)
        s+=text(28,235,'MỞ REPOSITORY  ↗',11,MINT,600,True)
    return shell(w,h,'Note App — Laravel, cộng tác thời gian thực và ngoại tuyến',s)

def experiment_card(kind):
    is_wasm=kind=='wasm'
    accent=GOLD if is_wasm else CORAL
    label='02 / BROWSER EXPERIMENT' if is_wasm else '03 / IDEA IN PROGRESS'
    name='WebAssembly' if is_wasm else 'VocaPiano AI'
    s=text(25,32,label,10,accent,600,True)+text(25,72,name,30,CREAM,650)
    s+=text(25,102,'Đưa C++ vào trình duyệt.' if is_wasm else 'Khi code gặp những giai điệu.',15,CREAM)
    s+=text(25,126,'Xử lý ảnh với JavaScript và Wasm.' if is_wasm else 'Ý tưởng AI hỗ trợ học hát và piano.',13,MUTED)
    if is_wasm:
        s+=rect(25,149,410,94,'#172e37',8,LINE)+rect(39,163,138,64,BG,4)
        for row in range(5):
            for col in range(11):
                fill=[GOLD,'#5b7778',MINT,CORAL][(row*col+col//3)%4]
                s+=rect(45+col*11,169+row*10,9,8,fill,1,extra=f'opacity="{.35+row*.12}"')
        s+=path('M195 196 H236 M229 190 L237 196 L229 202',GOLD,2)
        s+=rect(254,163,162,64,BG,4)+text(266,184,'pixels → process',11,GOLD,400,True)
        s+=text(266,211,'C++ / WebAssembly',10,MUTED,400,True)
        s+=rect(266,193,105,2,LINE,1)+rect(266,193,75,2,MINT,1,extra='class="twinkle"')
    else:
        s+=rect(25,149,410,94,'#172e37',8,LINE)+keyboard(42,183,230)
        for i in range(11):
            hh=[20,37,24,48,34,20,43,29,38,51,26][i]
            s+=rect(294+i*10,218-hh,5,hh,CORAL if i%3 else GOLD,2,extra=f'class="twinkle" style="animation-delay:{i*.2}s"')
        s+=group(text(0,0,'♪',23,CORAL,600,extra='class="note"'),120,178)
        s+=group(text(0,0,'♫',18,GOLD,600,extra='class="note" style="animation-delay:2s"'),235,186)
    s+=text(25,275,'PHP · JavaScript · C++' if is_wasm else 'ĐỀ XUẤT NGHIÊN CỨU · AI + AUDIO',10,accent,500,True)
    s+=text(420,275,'↗',18,accent)
    return shell(460,296,name,s)

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells={}
        self.counts={}
        self.tooltip=None
        self.content=[]

    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='td' and a.get('data-date'):
            self.cells[a['id']]={'date':a['data-date'],'level':int(a['data-level'])}
        if tag=='tool-tip' and a.get('for','').startswith('contribution-day-component-'):
            self.tooltip=a['for']
            self.content=[]

    def handle_data(self,data):
        if self.tooltip:self.content.append(data)

    def handle_endtag(self,tag):
        if tag=='tool-tip' and self.tooltip:
            m=re.match(r'\s*(No|[\d,]+) contributions? on ',''.join(self.content))
            if not m:raise ValueError('Unrecognized public contribution tooltip')
            self.counts[self.tooltip]=0 if m[1]=='No' else int(m[1].replace(',',''))
            self.tooltip=None

def fetch(url,is_json=False):
    headers={'User-Agent':'Luans-Midnight-Lab','Accept':'application/vnd.github+json' if is_json else 'text/html'}
    if is_json and os.environ.get('GITHUB_TOKEN'):
        headers['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=40) as r:
        return json.load(r) if is_json else r.read().decode('utf-8')

def public_activity():
    source=fetch(f'https://github.com/users/{USER}/contributions')
    parser=Calendar()
    parser.feed(source)
    if len(parser.cells)<350 or parser.cells.keys()!=parser.counts.keys():
        raise ValueError('Incomplete public contribution calendar; keeping existing artwork')
    days=sorted([{**cell,'count':parser.counts[key]} for key,cell in parser.cells.items()],key=lambda d:d['date'])
    total=sum(d['count'] for d in days)
    summary=re.search(r'id="js-contribution-activity-description"[^>]*>\s*([\d,]+)\s+contributions?',source)
    if not summary or int(summary[1].replace(',',''))!=total:
        raise ValueError('Public contribution totals do not agree; keeping existing artwork')
    repos=[]
    for page in range(1,101):
        batch=fetch(f'https://api.github.com/users/{USER}/repos?per_page=100&type=owner&page={page}',True)
        repos.extend(r for r in batch if not r.get('private',True))
        if len(batch)<100:break
    return days,total,len(repos)

def pulse(days,total,repos,mobile=False):
    w,h=(480,414) if mobile else (960,344)
    s=text(28,35,'THE BUILD RHYTHM / PUBLIC ACTIVITY',11,MINT,600,True)
    active=sum(d['count']>0 for d in days)
    values=[(total,'đóng góp / năm'),(active,'ngày có hoạt động'),(repos,'repo công khai')]
    step=148 if mobile else 304
    for i,(value,label) in enumerate(values):
        x=28+i*step
        s+=text(x,96 if mobile else 105,value,38 if mobile else 45,[CREAM,MINT,CORAL][i],650)
        s+=text(x,122 if mobile else 135,label,12 if mobile else 14,MUTED)
    top=172 if mobile else 180
    s+=path(f'M28 {top-18} H{w-28}',LINE)
    weeks=defaultdict(int)
    first=date.fromisoformat(days[0]['date'])
    for d in days:weeks[(date.fromisoformat(d['date'])-first).days//7]+=d['count']
    count=max(weeks)+1
    gap=3 if mobile else 5
    bw=(w-56-gap*(count-1))/count
    chart_h=130 if mobile else 100
    baseline=top+chart_h
    for i in range(count):
        value=weeks.get(i,0)
        height=4+(chart_h-4)*value/max(1,max(weeks.values(),default=0))
        x=28+i*(bw+gap)
        color=LINE if not value else (CORAL if i==count-1 else MINT)
        s+=rect(round(x,2),round(baseline-height,2),round(bw,2),round(height,2),color,min(3,bw/2))
    scan='scan-mobile' if mobile else 'scan'
    s+=f'<g opacity=".5" style="animation:{scan} 16s linear infinite">'+path(f'M28 {top-3} V{baseline+7}',GOLD,1.5)+'</g>'
    s+=text(28,baseline+26,days[0]['date'][:7],10,MUTED,400,True)
    s+=text(w-28,baseline+26,days[-1]['date'][:7],10,MUTED,400,True,extra='text-anchor="end"')
    updated=datetime.now(timezone.utc).strftime('%d.%m.%Y')
    footer_y=384 if mobile else 322
    s+=text(28,footer_y,f'{count} TUẦN · MỖI CỘT LÀ MỘT TUẦN',9,MUTED,400,True)
    s+=text(28 if mobile else w-28,footer_y+17 if mobile else footer_y,f'CẬP NHẬT {updated}',9,MUTED,400,True,extra='' if mobile else 'text-anchor="end"')
    desc=f'{total} đóng góp trên lịch công khai trong năm qua, {active} ngày hoạt động, {repos} repository công khai. Mỗi cột là tổng đóng góp của một tuần. Cập nhật {updated}.'
    return shell(w,h,'Nhịp xây dựng của Phùng Hữu Luân',s,desc)

def footer():
    d='M28 56 H110 Q130 56 130 36 V28 H200 Q220 28 220 48 V64 H298'
    s=path(d,LINE,2)+path(d,MINT,2,extra='class="signal"')
    s+=text(480,40,'Hẹn gặp ở lần commit tiếp theo.',23,CREAM,600,extra='text-anchor="middle"')
    s+=text(480,67,'STAY CURIOUS. KEEP MAKING.',10,MINT,500,True,extra='text-anchor="middle" letter-spacing="2"')
    s+=group(robot(),842,24,.8)
    return shell(960,106,'Hẹn gặp ở lần commit tiếp theo.',s)

def main():
    days,total,repos=public_activity()
    assets={'hero.svg':hero(),'hero-mobile.svg':hero(True),
            'note.svg':note_card(),'note-mobile.svg':note_card(True),
            'wasm.svg':experiment_card('wasm'),'music.svg':experiment_card('music'),
            'pulse.svg':pulse(days,total,repos),'pulse-mobile.svg':pulse(days,total,repos,True),
            'footer.svg':footer()}
    for name,content in list(assets.items()):
        assets[name.replace('.svg','-still.svg')]=content.replace('</style>','*{animation:none!important}.steam,.note{opacity:.6}</style>')
    for name,content in assets.items():
        root=ET.fromstring(content)
        assert root.tag.endswith('svg'),name
        assert '<script' not in content and '<foreignObject' not in content,name
    OUT.mkdir(parents=True,exist_ok=True)
    for name,content in assets.items():(OUT/name).write_text(content+'\n',encoding='utf-8')
    print(f'Generated {len(assets)} SVGs; public contributions={total}, public repositories={repos}.')

if __name__=='__main__':main()
