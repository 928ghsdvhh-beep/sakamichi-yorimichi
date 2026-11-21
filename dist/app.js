const query=document.querySelector('#query');
if(query){
 const group=document.querySelector('#group'),kind=document.querySelector('#kind'),year=document.querySelector('#year');
 const cards=[...document.querySelectorAll('#goods-grid .goods-card')];
 const normalize=text=>text.normalize('NFKC').toLowerCase().replaceAll('アクスタ','アクリルスタンド').trim();
 const update=(sync=true)=>{const term=normalize(query.value);let n=0;for(const c of cards){const ok=(group.value==='all'||c.dataset.group===group.value)&&(kind.value==='all'||c.dataset.kind===kind.value)&&(year.value==='all'||c.dataset.year===year.value)&&term.split(/\s+/).every(t=>normalize(c.dataset.search).includes(t));c.hidden=!ok;if(ok)n++;}document.querySelector('#count').textContent=n+'件の販売記録';document.querySelector('#empty').hidden=n>0;if(sync===true){const params=new URLSearchParams();if(query.value.trim())params.set('q',query.value.trim().slice(0,400));for(const [key,el] of [['group',group],['kind',kind],['year',year]])if(el.value!=='all')params.set(key,el.value);history.replaceState(null,'',location.pathname+(params.size?'?'+params:'')+'#archive');}};
 const restore=()=>{const params=new URLSearchParams(location.search);query.value=(params.get('q')||'').slice(0,400);for(const [key,el] of [['group',group],['kind',kind],['year',year]]){const value=params.get(key)||'all';el.value=[...el.options].some(option=>option.value===value)?value:'all';}update(false);};
 query.addEventListener('input',()=>update());[group,kind,year].forEach(el=>el.addEventListener('change',()=>update()));
 document.querySelector('#clear').addEventListener('click',()=>{query.value='';group.value=kind.value=year.value='all';update();query.focus();});
 window.addEventListener('popstate',restore);
 restore();
}
const memberForm=document.querySelector('#member-form');
if(memberForm){
 const updateMemberQuery=()=>{
  const group=document.querySelector('#member-group').value;
  const member=document.querySelector('#member-name').value.trim();
  const event=document.querySelector('#member-event').value.trim();
  const keyword=[group,member,event,'グッズ'].filter(Boolean).join(' ');
  document.querySelector('#amazon-keyword').value=keyword;
  document.querySelector('#member-search-link').href='https://www.amazon.co.jp/s?'+new URLSearchParams({k:keyword,tag:'moon12-22'});
 };
 memberForm.addEventListener('submit',event=>{event.preventDefault();updateMemberQuery();document.querySelector('#member-search-link').click();});
 memberForm.addEventListener('input',updateMemberQuery);
 memberForm.addEventListener('change',updateMemberQuery);
 updateMemberQuery();
}
