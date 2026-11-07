"""Generate missing audio (mp3) with Azure neural text-to-speech.
Reads audio/texts-<lang>.json ([[hash, text], ...]) written by the app build and
writes audio/<lang>/<hash>.mp3 plus audio/<lang>/index.json (list of hashes with audio).
Secrets: AZURE_SPEECH_KEY, AZURE_SPEECH_REGION (e.g. westeurope)."""
import json, os, sys, time, subprocess, urllib.request, urllib.error
from xml.sax.saxutils import escape
KEY=os.environ.get('AZURE_SPEECH_KEY','').strip(); REGION=os.environ.get('AZURE_SPEECH_REGION','').strip().lower()
if not KEY or not REGION:
    print('Secrets AZURE_SPEECH_KEY / AZURE_SPEECH_REGION are not set yet – nothing to do.'); sys.exit(0)
VOICES={'mn':('mn-MN','mn-MN-YesuiNeural'),'kz':('kk-KZ','kk-KZ-AigulNeural')}
RATE=os.environ.get('TTS_RATE','-10%')
URL=f'https://{REGION}.tts.speech.microsoft.com/cognitiveservices/v1'
DEADLINE=time.time()+float(os.environ.get('TTS_MAX_MINUTES','300'))*60
def synth(lang,text):
    loc,voice=VOICES[lang]
    ssml=f"<speak version='1.0' xml:lang='{loc}'><voice name='{voice}'><prosody rate='{RATE}'>{escape(text)}</prosody></voice></speak>"
    req=urllib.request.Request(URL,data=ssml.encode('utf-8'),method='POST',headers={'Ocp-Apim-Subscription-Key':KEY,'Content-Type':'application/ssml+xml','X-Microsoft-OutputFormat':'audio-24khz-48kbitrate-mono-mp3','User-Agent':'mn-kz-app'})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req,timeout=60) as r: return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503,504):
                wait=int(e.headers.get('Retry-After') or 0) or min(60,5*(attempt+1)); time.sleep(wait); continue
            print('HTTP',e.code,e.read()[:200],text[:60]); return None
        except Exception as e:
            print('ERR',e); time.sleep(5)
    return None
def commit(msg):
    subprocess.run(['git','add','audio'],check=True)
    if subprocess.run(['git','diff','--cached','--quiet']).returncode==0: return
    subprocess.run(['git','commit','-q','-m',msg],check=True)
    for _ in range(3):
        if subprocess.run(['git','push','-q']).returncode==0: return
        subprocess.run(['git','pull','-q','--rebase'])
done_total=0
for lang in ('mn','kz'):
    src=f'audio/texts-{lang}.json'
    if not os.path.exists(src): continue
    items=json.load(open(src,encoding='utf-8')); d=f'audio/{lang}'; os.makedirs(d,exist_ok=True)
    have={f[:-4] for f in os.listdir(d) if f.endswith('.mp3')}
    todo=[(h,t) for h,t in items if h not in have]
    print(lang,'total',len(items),'missing',len(todo))
    n=0
    for h,t in todo:
        if time.time()>DEADLINE: print('time limit reached'); break
        a=synth(lang,t)
        if a:
            open(f'{d}/{h}.mp3','wb').write(a); have.add(h); n+=1; done_total+=1
        time.sleep(float(os.environ.get('TTS_PAUSE','0.4')))
        if n and n%500==0:
            json.dump(sorted(have),open(f'{d}/index.json','w')); commit(f'Audio: {lang} +{n}')
    valid={h for h,_ in items}
    json.dump(sorted(have & valid),open(f'{d}/index.json','w'))
    commit(f'Audio: {lang} +{n} ({len(have & valid)}/{len(items)})')
print('new files',done_total)
