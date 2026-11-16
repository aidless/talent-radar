// A 数据池前端测试：demo 不上传；开关关不上传；开关开+确认后上传带 consent。
const fs = require('fs');
const vm = require('vm');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];

function run(demo, checked, confirmed) {
  const calls = [];
  const el = () => ({checked, classList:{add(){},remove(){}}, style:{display:''},
    addEventListener(ev,cb){ this._cb=cb; }, appendChild(){}, set textContent(v){}, get textContent(){return '';},
    set innerHTML(v){}, get innerHTML(){return '';}, querySelectorAll(){return [];}, onclick:null});
  const ctx = {
    console, document:{getElementById:()=>el(),querySelector:()=>el(),querySelectorAll:()=>[],
      createElement:()=>el(), addEventListener(){}, body:el()},
    location:{search: demo ? '?demo=1' : '', href:''},
    localStorage:{getItem:()=>null,setItem(){},removeItem(){}},
    navigator:{clipboard:{writeText:()=>Promise.resolve()}},
    setTimeout:()=>{}, clearTimeout:()=>{}, alert(){}, confirm:()=>confirmed,
    fetch:(url,opt)=>{calls.push({url,body: JSON.parse(opt.body)});return Promise.resolve({ok:true,json:()=>Promise.resolve({ok:true})});},
    URLSearchParams, Blob: class {}, URL:{createObjectURL:()=>'', revokeObjectURL(){}},
    btoa:(s)=>Buffer.from(s).toString('base64'), crypto:{subtle:{digest:()=>Promise.resolve(new Uint8Array(16))}},
    TextEncoder, Float32Array, Math, Date, JSON, Object, Array, String, Number, Boolean, Promise, Error,
  };
  ctx.window = ctx; ctx.globalThis = ctx;
  vm.createContext(ctx);
  vm.runInContext(script + `
    globalThis.__TEST__ = {
      lastResult: typeof lastResult !== 'undefined' ? lastResult : null,
      isDemo: typeof isDemo !== 'undefined' ? isDemo : false,
      windowContribution: typeof windowContribution === 'function' ? windowContribution : null,
      submitContribution: typeof submitContribution === 'function' ? submitContribution : null,
    };
  `, ctx);
  const t = ctx.__TEST__;
  if (t.windowContribution) {
    t.lastResult = {per:{},ranked:[],name:'测试者',desc:'',top3:[]};
    // 通过 vm 内部设置 lastResult（外部赋值只改导出的引用副本）
    vm.runInContext(`lastResult = {per:Object.fromEntries(DIMS.map(d=>[d.k,{score:70,behMean:.8,selfMean:.6,vol:.2}])),ranked:DIMS,behMean:.8,selfMean:.6,name:'测试者',desc:'',top3:[]}; answers = QS.map(()=>4); submitContribution();`, ctx);
  }
  return {calls, t};
}
const checks = [];
try {
  const d = run(true, false, true);
  checks.push(['demo no fetch', d.calls.length === 0]);
  const off = run(false, false, true);
  checks.push(['toggle off no fetch', off.calls.length === 0]);
  const yes = run(false, true, true);
  checks.push(['confirmed posts', yes.calls.length === 1]);
  checks.push(['post url', yes.calls[0] && yes.calls[0].url === '/api/contribute']);
  checks.push(['consent version', yes.calls[0] && yes.calls[0].body.consent.version === '1.0']);
  const no = run(false, true, false);
  checks.push(['declined no fetch', no.calls.length === 0]);
} catch (e) { checks.push(['runtime', false]); console.error(e.message); }
for (const [n, ok] of checks) console.log((ok?'PASS':'FAIL')+' '+n);
if (checks.some(c=>!c[1])) process.exit(1);
