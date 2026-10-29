"""Bangla visual stories, screen mockups and worked examples.

HarfBuzz shapes Bangla text; glyph outlines keep SVG/PDF/PNG identical without
depending on installed viewer fonts. All mockups are teaching illustrations.
"""
import html
import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

import cairosvg
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/figures'
FONTS=ROOT/'assets/fonts'
BG='#f7f4ec'; INK='#203c48'; MUTED='#5b737e'; TEAL='#117f7a'; BLUE='#3266a0'
RED='#b7494e'; GOLD='#bc7e18'; PURPLE='#7151a1'; LINE='#d9e3e0'; WHITE='#ffffff'
PALE='#e5f1eb'; ROSE='#f9e9e5'; LAV='#eee9f5'; SAND='#f5ecd5'; SKY='#e7eff8'
FONT_PATHS={'regular':FONTS/'NotoSansBengali-Regular.ttf','bold':FONTS/'NotoSansBengali-Bold.ttf',
            'fallback':FONTS/'DejaVuSans.ttf'}
FONT={}
for name,path in FONT_PATHS.items():
    font=TTFont(path);face=hb.Face(path.read_bytes());hfont=hb.Font(face);hb.ot_font_set_funcs(hfont)
    hfont.scale=(face.upem,face.upem)
    FONT[name]={'tt':font,'hb':hfont,'upem':face.upem,'order':font.getGlyphOrder(),
                'glyphs':font.getGlyphSet(),'cmap':font.getBestCmap()}


@lru_cache(maxsize=12000)
def shape(text,bold=False):
    result=[];runs=[];current='';previous=None
    for character in text:
        script='Beng' if '\u0980'<=character<='\u09ff' else 'Latn'
        if not character.isalpha() and not ('\u0980'<=character<='\u09ff'):
            script=previous[1] if previous else 'Latn'
        family='bold' if bold else 'regular'
        if ord(character) not in FONT[family]['cmap'] and character not in '\u200d\u200c': family='fallback'
        key=(family,script)
        if previous and key!=previous:
            runs.append((previous,current));current=''
        current+=character;previous=key
    if current:runs.append((previous,current))
    cursor=0
    for (family,script),run in runs:
        buf=hb.Buffer();buf.add_str(run);buf.direction='ltr';buf.script=script;buf.language='bn' if script=='Beng' else 'en'
        hb.shape(FONT[family]['hb'],buf)
        for info,pos in zip(buf.glyph_infos,buf.glyph_positions):
            if info.codepoint==0:raise ValueError(f'Missing glyph in {run!r}')
            upem=FONT[family]['upem']
            result.append((family,info.codepoint,cursor+pos.x_offset/upem,pos.y_offset/upem))
            cursor+=pos.x_advance/upem
    return result,cursor


@lru_cache(maxsize=4000)
def glyph_path(family,gid):
    font=FONT[family];pen=SVGPathPen(font['glyphs']);font['glyphs'][font['order'][gid]].draw(pen)
    return pen.getCommands()


class Canvas:
    def __init__(self,name,title,subtitle='',height=900):
        self.name=name;self.title=title;self.width=1440;self.height=height
        self.parts=[];self.used=set();self.labels=[];self.problems=[]
        self.rect(0,0,1440,height,BG,r=0)
        self.rect(48,43,10,62,TEAL,r=4)
        self.text(80,87,title,44,bold=True)
        if subtitle:self.text(80,134,subtitle,25,color=MUTED)
        self.line(48,height-70,1392,height-70,LINE,2)
        self.text(50,height-29,'দেখা থেকে জানা  /  শিক্ষামূলক দৃশ্য',21,color=MUTED)
        self.text(1390,height-29,name.split('-')[0],22,color=MUTED,align='right')
    def rect(self,x,y,w,h,fill=WHITE,stroke=None,r=18):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="2"' if stroke else '')+'/>')
    def line(self,x1,y1,x2,y2,color=LINE,width=3,dash=None):
        self.parts.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def path(self,d,fill='none',stroke=INK,width=3):
        self.parts.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>')
    def circle(self,x,y,r,fill=TEAL,stroke=None):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="3"' if stroke else '')+'/>')
    def text(self,x,y,value,size=28,color=INK,bold=False,align='left'):
        value=str(value);glyphs,width=shape(value,bold);width*=size
        if align=='center':x-=width/2
        if align=='right':x-=width
        if x<20 or x+width>1420:self.problems.append({'text':value,'x':x,'width':width})
        self.labels.append(value)
        self.parts.append(f'<g fill="{color}" aria-label="{html.escape(value,quote=True)}">')
        for family,gid,gx,gy in glyphs:
            self.used.add((family,gid));scale=size/FONT[family]['upem']
            self.parts.append(f'<use href="#g_{family}_{gid}" transform="translate({x+gx*size:.3f} {y-gy*size:.3f}) scale({scale:.7f} {-scale:.7f})"/>')
        self.parts.append('</g>')
        return width
    def wrap(self,x,y,value,width,size=28,color=INK,bold=False,leading=1.55):
        words=value.split();lines=[];current=''
        for word in words:
            nextline=(current+' '+word).strip()
            if shape(nextline,bold)[1]*size>width and current:lines.append(current);current=word
            else:current=nextline
        if current:lines.append(current)
        for i,line in enumerate(lines):self.text(x,y+i*size*leading,line,size,color,bold)
        return y+len(lines)*size*leading
    def arrow(self,x1,y1,x2,y2,color=TEAL,label=None):
        import math
        self.line(x1,y1,x2,y2,color,4)
        angle=math.atan2(y2-y1,x2-x1);size=13
        a=(x2-size*math.cos(angle-.5),y2-size*math.sin(angle-.5))
        b=(x2-size*math.cos(angle+.5),y2-size*math.sin(angle+.5))
        self.path(f'M{a[0]} {a[1]} L{x2} {y2} L{b[0]} {b[1]}',stroke=color,width=4)
        if label:self.text((x1+x2)/2,(y1+y2)/2-15,label,24,color,align='center')
    def tag(self,x,y,label,color=TEAL,bg=PALE,width=None):
        w=width or shape(label,True)[1]*23+32
        self.rect(x,y,w,43,bg,r=13);self.text(x+16,y+30,label,23,color,bold=True)
    def check(self,x,y,ok=True):
        self.circle(x,y,19,TEAL if ok else RED)
        if ok:self.path(f'M{x-9} {y} l6 7 l13 -14',stroke=WHITE,width=4)
        else:self.line(x-7,y-7,x+7,y+7,WHITE,3);self.line(x-7,y+7,x+7,y-7,WHITE,3)
    def avatar(self,x,y,label,color=BLUE):
        self.circle(x,y,34,SKY if color==BLUE else PALE)
        self.circle(x,y-7,11,color)
        self.path(f'M{x-20} {y+21} Q{x-20} {y+5} {x} {y+5} Q{x+20} {y+5} {x+20} {y+21}',fill=color,stroke=color)
        self.text(x+49,y+10,label,27,bold=True)
    def browser(self,x,y,w,h,title='RelayDesk'):
        self.rect(x+5,y+7,w,h,'#e1e7e2',r=19);self.rect(x,y,w,h,WHITE,LINE,r=19)
        self.rect(x,y,w,50,'#edf1ed',r=18)
        for i,color in enumerate([RED,GOLD,TEAL]):self.circle(x+22+i*18,y+25,5,color)
        self.text(x+88,y+34,title,22,color=MUTED)
    def ticket(self,x,y,w,label='t_101',color=TEAL,detail='Login failure'):
        self.rect(x,y,w,85,PALE if color==TEAL else SKY,r=11)
        self.rect(x,y,6,85,color,r=2);self.text(x+18,y+33,label,25,color,bold=True)
        self.text(x+18,y+65,detail,24)
    def number(self,x,y,n):
        self.circle(x,y,22,TEAL);self.text(x,y+9,str(n),25,WHITE,bold=True,align='center')
    def save(self,chapter,kind='conceptual'):
        defs=[]
        for family,gid in sorted(self.used):
            defs.append(f'<path id="g_{family}_{gid}" d="{glyph_path(family,gid)}"/>')
        svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="{self.height}" viewBox="0 0 1440 {self.height}" role="img">'
             f'<title>{html.escape(self.title)}</title><desc>{html.escape(" | ".join(self.labels))}</desc><defs>'+''.join(defs)+'</defs>'+''.join(self.parts)+'</svg>')
        (OUT/(self.name+'.svg')).write_text(svg,encoding='utf-8')
        cairosvg.svg2png(bytestring=svg.encode(),write_to=str(OUT/(self.name+'.png')),output_width=1800,output_height=round(self.height*1.25))
        if self.problems:raise ValueError({self.name:self.problems})
        source='reports/lab-results.json' if kind=='executed_local_lab' else 'data/latency.csv' if kind=='synthetic' else None
        return {'file':self.name,'kind':kind,'chapter':chapter,'language':'bn','title':self.title,'generator':'scripts/make_visual_stories.py','data':source}


def make():
    manifest=[]
    # A UI reveal, not another abstract layer diagram.
    c=Canvas('15-refresh-reveal','একই রকম দেখাচ্ছে। Refresh দিলে?','প্রথমে অনুমান করো; তারপর নিচের দুই ফল দেখো।',940)
    for x,head,real in [(60,'অ্যাপ A',False),(750,'অ্যাপ B',True)]:
        c.tag(x,177,head,BLUE,SKY)
        c.browser(x,235,625,205,'টিকিট তালিকা · এখন')
        c.ticket(x+25,310,575)
        c.arrow(x+310,453,x+310,515,label='Refresh')
        c.browser(x,535,625,225,'টিকিট তালিকা · আবার খোলা')
        if real:c.ticket(x+25,610,575)
        else:c.text(x+310,665,'এখানে কোনো ticket নেই',32,MUTED,align='center')
        c.check(x+28,802,real);c.text(x+61,813,'নতুন read-এ ticket পাওয়া গেল' if real else 'এই run-এ state হারিয়েছে',28)
    manifest.append(c.save('01'))

    c=Canvas('16-repository-map','একটি bug খুঁজতে পাঁচটি জায়গা','উদাহরণ: button চাপলে success, কিন্তু reload-এ ticket নেই।')
    c.rect(60,180,590,560,INK);c.text(90,230,'relaydesk/',34,WHITE,bold=True)
    folders=[('README.md','চালানোর পথ'),('ui/TicketForm','user কী পাঠাচ্ছেন'),('api/create','কোন handler চলছে'),('domain/TicketService','নিয়ম ও persistence'),('tests/','কী যাচাই হয়েছে')]
    for i,(name,note) in enumerate(folders):
        y=300+i*83;c.line(110,257,110,y, '#71919b',3);c.line(110,y,144,y,'#71919b',3)
        c.text(165,y+8,name,28,WHITE)
        c.arrow(665,y,742,y,color=BLUE)
        c.number(785,y,i+1);c.text(825,y+10,note,28)
    c.tag(65,770,'প্রথম কাজ: active call path খুঁজে বের করা',TEAL,PALE)
    manifest.append(c.save('02'))

    c=Canvas('17-evidence-sort','দেখেছি, ভেবেছি, না-জানা—তিনটি আলাদা ঘর','দৃশ্য: assignment-এর পরে screen-এ নীরার নাম উঠেছে।')
    c.browser(60,190,560,320,'Ticket t_101');c.avatar(100,300,'নীরা',TEAL);c.tag(85,370,'UI-তে নাম বদলেছে',TEAL,PALE)
    c.path('M558 497 Q640 570 713 497',stroke=GOLD,width=6)
    for y,title,body,color,bg in [(185,'দেখেছি','এই screen-এ assignee এখন নীরা।',TEAL,PALE),(385,'এখনও পরীক্ষা বাকি','Reload-এর পরও নামটি থাকবে?',GOLD,SAND),(585,'এখান থেকে জানা যায় না','Server কোন database ব্যবহার করে?',PURPLE,LAV)]:
        c.rect(735,y,645,160,bg);c.text(760,y+48,title,31,color,bold=True);c.wrap(760,y+98,body,590,28)
    c.wrap(72,605,'পরের ছোট পরীক্ষা: নতুন session থেকে একই ticket পড়ো।',545,31)
    manifest.append(c.save('03'))

    c=Canvas('18-journey-strip','একটি ticket-এর ছোট যাত্রা','একটি feature মানে শুধু তার প্রথম screen নয়।',850)
    scenes=[('১ · লেখা','Title: Login failure','এখনও draft'),('২ · পাঠানো','POST /tickets','ফল আসেনি'),('৩ · পাওয়া','id: t_101','server response'),('৪ · আবার খোলা','t_101 এখনও আছে','নতুন read')]
    for i,(title,body,foot) in enumerate(scenes):
        x=55+i*348;c.browser(x,240,292,333,title);c.text(x+23,355,body,24)
        c.ticket(x+22,390,248,'t_101' if i>1 else 'draft',detail='Login failure')
        c.tag(x+16,600,foot,TEAL if i>1 else GOLD,PALE if i>1 else SAND)
        if i<3:c.arrow(x+299,470,x+337,470)
    c.text(720,730,'প্রতিটি ধাপের আলাদা প্রশ্ন আছে: input? ফল? storage? access?',30,align='center')
    manifest.append(c.save('04'))

    c=Canvas('19-two-clicks','দুই click দেখে সিদ্ধান্ত নয়—request-ও গুনো','দুটি আলাদা ঘটনা বাইরে থেকে একই রকম লাগতে পারে।')
    for x,head,requests,note,color in [(60,'ঘটনা A',1,'Client দ্বিতীয় request পাঠায়নি',BLUE),(750,'ঘটনা B',2,'দুই request, এক persisted record',TEAL)]:
        c.rect(x,195,625,548,WHITE,LINE);c.text(x+25,245,head,33,color,bold=True)
        c.text(x+25,312,'Click:  ১   ২',30);c.text(x+25,385,'Network log',26,MUTED)
        for i in range(requests):c.tag(x+25,408+i*63,'POST /tickets  ·  key=k1',color,SKY if color==BLUE else PALE,width=560)
        c.ticket(x+25,570,560,'t_101',detail='list-এ একটি ticket')
        c.wrap(x+25,700,note,565,25,color)
    c.text(720,802,'একটি card দেখা গেলেই server deduplication প্রমাণ হয় না।',30,align='center')
    manifest.append(c.save('05'))

    c=Canvas('20-ui-contact-sheet','একই form, ছয়টি আলাদা মুহূর্ত','কোন screen-এ user আবার submit করবেন? কোনটিতে আগে ফল খুঁজবেন?',1130)
    states=[('১ · লিখছি','Login failure','টিকিট তৈরি',BLUE,SKY),('২ · পাঠাচ্ছে','Login failure','অপেক্ষা করুন',GOLD,SAND),
            ('৩ · input খালি','শিরোনাম লিখুন','এখানে title দরকার',RED,ROSE),('৪ · confirmed','t_101 তৈরি হয়েছে','টিকিট খুলুন',TEAL,PALE),
            ('৫ · response হারিয়েছে','লেখাটি রাখা আছে','আগের ফল যাচাই',GOLD,SAND),('৬ · অন্যজন বদলেছেন','server এখন v2','নতুন state দেখুন',PURPLE,LAV)]
    for i,(head,value,button,color,bg) in enumerate(states):
        x=55+(i%3)*463;y=200+(i//3)*401
        c.browser(x,y,412,341,head);c.text(x+22,y+104,'শিরোনাম',24,MUTED)
        c.rect(x+20,y+123,372,72,bg,r=9);c.text(x+36,y+168,value,25,color)
        c.rect(x+20,y+232,372,64,color,r=10);c.text(x+206,y+275,button,27,WHITE,align='center')
    c.text(720,1022,'৫ নম্বরে নতুন operation তৈরি করলে duplicate হতে পারে।',31,align='center')
    manifest.append(c.save('06'))

    c=Canvas('21-api-envelope','একটি request-এর খাম খুলে দেখি','HTTP উদাহরণটি service contract বোঝানোর জন্য।',940)
    c.rect(55,200,620,492,SKY);c.tag(80,224,'পাঠানো',BLUE,WHITE)
    for y,label,value in [(322,'ঠিকানা','POST /workspaces/ws_a/tickets'),(420,'পরিচয়','trusted session → alice'),(518,'operation','Idempotency-Key: k1'),(616,'body','{"title": "Login failure"}')]:
        c.text(80,y,label,24,MUTED);c.text(80,y+40,value,28)
    c.arrow(690,450,756,450)
    for y,head,body,color,bg in [(200,'201 · তৈরি হয়েছে','id=t_101  /  version=1',TEAL,PALE),(375,'422 · title খালি','title field-এর পাশে বার্তা',RED,ROSE),(550,'409 · key মেলেনি','k1-এ আগের title আলাদা',GOLD,SAND)]:
        c.rect(778,y,607,144,bg);c.text(804,y+49,head,31,color,bold=True);c.text(804,y+101,body,27)
    c.wrap(80,785,'খামের ঠিকানা, পরিচয়, key আর body—প্রতিটি আলাদা কাজ করে। একটির পরীক্ষা দিয়ে বাকিগুলো যাচাই হয় না।',1260,31)
    manifest.append(c.save('07'))

    c=Canvas('22-state-metro','Ticket-এর চলার পথ','আমাদের lab-এর rule: সব station থেকে সব station-এ যাওয়া যায় না।',820)
    points=[(175,'open','নতুন'),(535,'in_progress','কাজ চলছে'),(895,'resolved','সমাধান'),(1255,'closed','শেষ')]
    c.line(175,365,1255,365,TEAL,5)
    for x in [355,715,1075]:c.arrow(x-25,365,x+25,365,TEAL)
    for x,state,bn in points:
        c.circle(x,365,28,WHITE,TEAL);c.circle(x,365,11,TEAL)
        c.text(x,450,state,29,bold=True,align='center');c.text(x,493,bn,28,MUTED,align='center')
    c.path('M895 330 C895 210 535 210 535 318',stroke=BLUE,width=4);c.arrow(535,300,535,320,BLUE)
    c.text(715,230,'আবার কাজ দরকার',28,BLUE,align='center')
    c.line(175,595,1255,595,RED,4,dash='12 10');c.check(715,595,False)
    c.text(715,655,'open → closed সরাসরি নয়',31,RED,align='center')
    manifest.append(c.save('08'))

    c=Canvas('23-delete-shadows','Delete চাপলে কোন কপিগুলো থাকে?','t_101 মুছে ফেলার পরে চার জায়গায় খোঁজ নাও।',880)
    for i,(label,value,color,bg) in enumerate([('Primary store','t_101: deleted v10',TEAL,PALE),('Search result','পুরোনো title এখনও আছে',RED,ROSE),('Attachment link','access revoke হয়েছে?',GOLD,SAND),('Backup','retention policy মেনে থাকবে',PURPLE,LAV)]):
        x=60+(i%2)*690;y=200+(i//2)*265
        c.rect(x,y,630,223,bg);c.text(x+30,y+53,label,33,color,bold=True)
        c.path(f'M{x+35} {y+88} h45 l17 17 v69 h-62 z',fill=WHITE,stroke=color,width=3)
        c.wrap(x+120,y+132,value,465,30)
    c.text(720,774,'আগে v10 delete, পরে v9 update এলে record যেন ফিরে না আসে।',29,align='center')
    manifest.append(c.save('09'))

    c=Canvas('24-retry-receipts','একই রসিদ, নাকি নতুন অর্ডার?','এখানে ticket তৈরির operation-কে রসিদ দিয়ে মনে রাখছি।',990)
    rows=[('k1','Login failure','নতুন t_101',TEAL,PALE),('k1','Login failure','আগের t_101',BLUE,SKY),
          ('k1','Changed title','conflict',RED,ROSE),('k2','Login failure','নতুন t_102',TEAL,PALE)]
    c.text(90,220,'KEY',24,MUTED);c.text(330,220,'PAYLOAD',24,MUTED);c.text(1025,220,'ফল',27,MUTED)
    for i,(key,title,result,color,bg) in enumerate(rows):
        y=255+i*133;c.rect(60,y,680,103,WHITE,LINE);c.tag(85,y+30,key,BLUE,SKY,width=120)
        c.text(270,y+63,title,31);c.arrow(770,y+52,915,y+52,color)
        c.rect(945,y,435,103,bg);c.text(1162,y+64,result,32,color,bold=True,align='center')
    c.tag(65,825,'একই actor + workspace-এর ভেতরের উদাহরণ',PURPLE,LAV)
    manifest.append(c.save('10'))

    c=Canvas('25-network-curtain','Gate-এর নাম দেখে ভেতরের ঘর চেনা যায়?','Response header: Server: nginx',850)
    c.browser(65,275,360,248,'Browser');c.text(92,385,'request',33);c.text(92,452,'response header',26,MUTED)
    c.rect(560,235,300,330,SKY);c.text(710,310,'Edge / proxy',34,BLUE,bold=True,align='center')
    for y in [355,425]:c.rect(600,y,220,44,WHITE);c.circle(625,y+22,7,TEAL)
    c.arrow(440,385,545,385);c.arrow(875,385,975,385)
    c.rect(990,225,385,360,LAV);c.text(1182,355,'?',112,PURPLE,bold=True,align='center')
    c.text(1182,455,'Origin app',33,PURPLE,align='center');c.text(1182,510,'Python? Go? অন্য কিছু?',25,align='center')
    c.wrap(85,690,'nginx দেখা গেছে। Application language জানতে আরও আলাদা evidence লাগবে।',1250,32)
    manifest.append(c.save('11'))

    c=Canvas('26-workspace-doors','দুটি workspace, দুটি দরজা','Login করা আছে—তবু কোন দরজাটি খোলা যাবে?',940)
    for x,title,color,bg in [(70,'Workspace A',TEAL,PALE),(780,'Workspace B',BLUE,SKY)]:
        c.rect(x,200,590,425,bg);c.text(x+295,262,title,35,color,bold=True,align='center')
        c.rect(x+210,300,170,252,WHITE,color,r=6);c.circle(x+353,434,9,color)
        c.text(x+295,595,'t_A' if x==70 else 't_B',30,color,align='center')
    c.avatar(120,717,'Alice · member A',TEAL);c.arrow(320,685,365,641,TEAL)
    c.avatar(835,717,'Bob · member B',BLUE);c.arrow(1060,685,1075,641,BLUE)
    c.line(850,790,365,790,RED,4,dash='10 9');c.check(610,790,False)
    c.text(720,860,'Bob → t_A: server প্রত্যাখ্যান করবে',31,RED,align='center')
    manifest.append(c.save('12'))

    c=Canvas('27-hundred-requests','একশো request-কে একশো বিন্দু ভাবো','প্রতিটি বিন্দু একটি request। শেষ পাঁচজনকে চোখে দেখো।',920)
    for i in range(100):
        color=TEAL if i<90 else GOLD if i<95 else RED
        c.circle(115+(i%10)*67,240+(i//10)*52,17,color)
    for y,head,number,color in [(245,'দ্রুত · ৯০টি','১০০ ms',TEAL),(407,'মাঝারি · ৫টি','২০০ ms',GOLD),(569,'ধীর · ৫টি','১,৫০০ ms',RED)]:
        c.circle(890,y-12,16,color);c.text(930,y,head,32,color,bold=True);c.text(930,y+57,number,39)
    c.text(720,795,'Mean = ১৭৫ ms। তবু লাল পাঁচজন অপেক্ষা করেছেন ১.৫ সেকেন্ড।',29,align='center')
    manifest.append(c.save('14','synthetic'))

    c=Canvas('28-architecture-rooms','এক বাড়ির ঘর, নাকি আলাদা বাড়ি?','দুটি design-এ একই responsibility থাকতে পারে; যোগাযোগের খরচ আলাদা।',980)
    c.rect(60,205,625,490,PALE,TEAL);c.text(372,265,'এক deploy',35,TEAL,bold=True,align='center')
    for x,y,label in [(95,320,'Ticket'),(390,320,'Identity'),(95,500,'Notify'),(390,500,'Search')]:
        c.rect(x,y,260,130,WHITE,LINE);c.text(x+130,y+77,label,32,align='center')
    c.tag(100,730,'ভেতরে module boundary',TEAL,PALE)
    c.text(1060,265,'আলাদা deploy',35,BLUE,bold=True,align='center')
    for x,y,label in [(760,320,'Ticket'),(1090,320,'Identity'),(760,535,'Notify'),(1090,535,'Search')]:
        c.rect(x,y,285,115,SKY,BLUE);c.text(x+142,y+70,label,32,align='center')
    c.arrow(1055,375,1080,375,BLUE);c.arrow(900,450,900,525,BLUE,'network');c.arrow(1230,450,1230,525,BLUE,'network')
    c.tag(795,730,'deploy স্বাধীন; failure path বাড়ে',BLUE,SKY)
    c.text(720,870,'প্রশ্ন: আলাদা scale/deploy-এর প্রয়োজন কি এখন সত্যিই আছে?',30,align='center')
    manifest.append(c.save('15'))

    actual=json.loads((ROOT/'reports/lab-results.json').read_text())
    c=Canvas('29-lab-snapshots','Lab চালিয়ে যে সংখ্যাগুলো পাওয়া যায়','Saved local lab report থেকে নেওয়া ফল; real provider নয়।',940)
    samples=[('একই create আবার',f"ticket count = {actual['duplicate_submission']['ticket_count']}",'একই ID ফিরে আসে',TEAL,PALE),
             ('Send-এর পরে crash',f"effect {actual['ack_gap']['provider_effects']}  /  pending {actual['ack_gap']['pending_events']}",'কাজ হয়েছে; mark বাকি',GOLD,SAND),
             ('Worker আবার চালানো',f"effect {actual['worker_retry']['provider_effects']}  /  pending {actual['worker_retry']['pending_events']}",'provider একই event চিনেছে',BLUE,SKY)]
    for i,(head,numbers,note,color,bg) in enumerate(samples):
        x=60+i*463;c.rect(x,230,410,440,bg);c.number(x+38,275,i+1);c.wrap(x+25,348,head,365,34,color,True)
        c.text(x+205,481,numbers,29,color,bold=True,align='center');c.wrap(x+25,574,note,360,29)
    c.text(720,778,'সবচেয়ে অদ্ভুত ঘরটি মাঝখানে: effect আছে, pending-ও আছে।',30,align='center')
    c.text(720,826,'Response/ack না পেলে আগে operation-এর ফল খুঁজে দেখো।',29,MUTED,align='center')
    manifest.append(c.save('16','executed_local_lab'))

    c=Canvas('30-cache-before-after','এক ticket, দুই জায়গায় দুই নাম','Discrepancy: details বদলেছে, list-এর cache বদলায়নি।',900)
    for x,title,person,color in [(60,'আগে: mismatch','আরিফ',RED),(750,'সংশোধনের পরে','নীরা',TEAL)]:
        c.tag(x,190,title,color,ROSE if color==RED else PALE)
        c.browser(x,270,625,390,'RelayDesk · t_101')
        c.rect(x+20,347,265,205,SKY);c.text(x+40,392,'List',26,BLUE,bold=True);c.avatar(x+64,469,person,BLUE)
        c.rect(x+305,347,300,205,PALE);c.text(x+325,392,'Details',26,TEAL,bold=True);c.avatar(x+351,469,'নীরা',TEAL)
        c.check(x+35,722,color==TEAL);c.wrap(x+73,732,'mutation-এর পরে সংশ্লিষ্ট list update' if color==TEAL else 'একই resource-এর inconsistent copy',535,27)
    manifest.append(c.save('17'))

    c=Canvas('31-four-worlds','চার product-এ চারটি ছোট প্রশ্ন','একই পদ্ধতি: ঘটনার মাঝে থেমে পরের state অনুমান করো।',1080)
    panels=[(60,190,'দোকান','Stock ১ · buyer ২','দুজনই reserve করতে পারবেন?',GOLD,SAND),
            (750,190,'একসঙ্গে লেখা','CAT → XCAT','পুরোনো “প্রথম অক্ষর” কোনটি?',PURPLE,LAV),
            (60,590,'AI agent','Draft তৈরি → Send?','পাঠানোর অনুমতি এসেছে?',BLUE,SKY),
            (750,590,'Offline note','Local save → restart','নোটটি কি এখনও আছে?',TEAL,PALE)]
    for x,y,title,state,question,color,bg in panels:
        c.rect(x,y,625,340,bg);c.text(x+28,y+56,title,37,color,bold=True)
        c.rect(x+28,y+95,568,100,WHITE);c.text(x+311,y+160,state,32,color,align='center')
        c.wrap(x+28,y+255,question,560,30)
    manifest.append(c.save('18'))

    c=Canvas('32-agent-conversation','Agent-কে পরের কাজটি স্পষ্ট করে দাও','একটি conversation-এ scope, evidence আর test কোথায় বসে দেখো।',1030)
    c.avatar(95,225,'তুমি',BLUE);c.rect(270,180,1090,125,SKY);c.text(302,233,'“সব production-ready করো”',35,BLUE,bold=True);c.text(302,275,'কোন outcome? কোথায় থামবে?',27,MUTED)
    c.avatar(95,405,'তুমি',BLUE);c.rect(270,345,1090,255,PALE)
    for i,line in enumerate(['“শুধু create ticket-এর retry সামলাও।”','একই key + payload → এক ticket','অন্য payload → conflict','দুই overlapping request দিয়ে test চালাও']):c.text(302,403+i*51,line,29,TEAL if i==0 else INK,bold=i==0)
    c.avatar(95,735,'Agent',TEAL);c.rect(270,650,1090,230,WHITE,LINE)
    for i,line in enumerate(['Changed: service + tests','Ran: duplicate, conflict, reopen checks','বাকি: real provider integration যাচাই হয়নি']):c.text(302,710+i*56,line,30)
    manifest.append(c.save('19'))

    c=Canvas('33-migration-bridge','Field বদলানোর সময় দুই version-ই চলছে','name থেকে display_name-এ যাওয়ার একটি compatibility plan।',920)
    stages=[('১ · Expand','name + display_name','দুটি field সহ schema'),('২ · Migrate','backfill + read switch','নতুন write-ও মিলিয়ে দেখো'),('৩ · Contract','display_name','পুরোনো consumer শেষ হলে')]
    for i,(head,field,note) in enumerate(stages):
        x=60+i*463;c.rect(x,245,410,365,SKY if i==1 else PALE);c.text(x+25,306,head,34,bold=True)
        c.rect(x+22,344,366,125,WHITE);c.wrap(x+42,395,field,325,30,BLUE,True)
        c.wrap(x+25,536,note,360,28)
        if i<2:c.arrow(x+420,425,x+450,425)
    c.rect(85,690,1270,115,SAND);c.wrap(115,735,'Old worker এখনও name পড়লে তৃতীয় ধাপে যেও না। আগে consumer compatibility যাচাই করো।',1210,29)
    manifest.append(c.save('20'))

    c=Canvas('34-release-gate','সবুজ অনেকগুলো। তবু দরজা বন্ধ।','Cosmetic pass আর critical failure একই ওজনের সিদ্ধান্ত নয়।',860)
    c.rect(70,220,610,400,WHITE,LINE);c.text(105,280,'১০টি visual check',34,TEAL,bold=True)
    for i in range(10):c.check(130+(i%5)*110,355+(i//5)*105,True)
    c.rect(780,220,590,400,ROSE);c.text(815,280,'Tenant isolation',34,RED,bold=True)
    c.check(1075,395,False);c.text(1075,483,'অন্যের ticket দেখা যাচ্ছে',30,RED,align='center')
    c.line(180,715,1260,715,RED,18);c.rect(525,675,390,84,WHITE,RED);c.text(720,730,'Release gate: FAIL',32,RED,bold=True,align='center')
    manifest.append(c.save('21'))

    c=Canvas('35-daily-workbench','আজকের ডেস্কে তিনটি ছোট খাতা','আগের session-এর কাজ ধরে পরের ছোট পরীক্ষা বেছে নাও।',900)
    cards=[('দেখেছি','API-তে assignee = nira','E-017',TEAL,PALE),('এখনও অজানা','List কেন arif দেখাচ্ছে?','U-008',GOLD,SAND),('পরের কাজ','Cache key ও invalidation দেখব','EXP-009',BLUE,SKY)]
    for i,(head,note,key,color,bg) in enumerate(cards):
        x=60+i*463;c.rect(x+7,247,410,415,'#dfe3da');c.rect(x,235,410,415,bg)
        c.rect(x+140,218,130,33,'#e2d3a9',r=3);c.text(x+28,320,head,37,color,bold=True)
        c.wrap(x+28,410,note,350,33);c.tag(x+28,555,key,color,WHITE)
    c.text(720,758,'দিন শেষে: কোন প্রশ্নের উত্তর বদলাল, সেটুকু লিখে রাখো।',31,align='center')
    manifest.append(c.save('23'))

    c=Canvas('36-memory-postcards','বই বন্ধ করে এই ছয়টি প্রশ্ন বলো','প্রতিটি প্রশ্নের জন্য নিজের project থেকে একটি উদাহরণ দাও।',1090)
    notes=[('দেখেছি কী?','screen / response / trace',TEAL,PALE),('কোথায় সত্য?','server / cache / projection',BLUE,SKY),
           ('কার অনুমতি?','actor + resource + action',PURPLE,LAV),('আবার হলে?','retry / duplicate / version',GOLD,SAND),
           ('মাঝে থামলে?','commit / send / ack',RED,ROSE),('কী যাচাই হলো?','scenario + actual result',TEAL,PALE)]
    for i,(head,note,color,bg) in enumerate(notes):
        x=60+(i%2)*690;y=190+(i//2)*255
        c.rect(x,y,625,210,bg);c.number(x+46,y+48,i+1);c.text(x+90,y+60,head,36,color,bold=True)
        c.text(x+28,y+147,note,27)
    manifest.append(c.save('24'))
    return manifest


if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    new=make()
    manifest_path=OUT/'manifest.json'
    old=json.loads(manifest_path.read_text())
    old=[entry for entry in old if entry.get('generator')!='scripts/make_visual_stories.py']
    manifest_path.write_text(json.dumps(old+new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'reports/visual-stories.json').write_text(json.dumps({'count':len(new),'language':'bn','figures':new},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Generated {len(new)} Bengali SVG/PNG visual stories.')
