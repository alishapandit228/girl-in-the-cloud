const login=$("#login"), logout=$("#logout"), range=$("#range");
if(login) login.onsubmit=async event=>{
  event.preventDefault();
  try{await api("login",{password:login.elements.password.value});location.replace("/admin");}
  catch(e){$("[role=status]",login).textContent=e.message;}
};
if(logout) logout.onclick=async()=>{try{await api("logout",{});location.replace("/admin");}catch(e){$("#report").textContent=e.message;}};
async function refresh(){
  const root=$("#report");root.textContent="Loading report…";
  try{
    const report=await api("report?"+new URLSearchParams(new FormData(range)));
    root.replaceChildren();
    for(const [title,values] of Object.entries(report)){
      const section=element("section","");section.append(element("h2",title));
      const maximum=Math.max(1,...values.map(v=>v[1]));
      for(const [label,value] of values){
        const row=element("div","");row.className="chartrow";const meter=element("meter","");meter.max=maximum;meter.value=value;meter.setAttribute("aria-label",label);
        row.append(element("span",label),meter,element("span",value));section.append(row);
      }
      if(!values.length)section.append(element("p","No records in this period."));
      root.append(section);
    }
  }catch(e){root.textContent=e.message;}
}
if(range){range.onsubmit=e=>{e.preventDefault();refresh();};refresh();}
