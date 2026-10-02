const items=[
{name:"Medusa",cat:"Ecommerce",license:"MIT",type:"Software",desc:"Open-source commerce engine for modern online stores.",latest:true},
{name:"Bagisto",cat:"Ecommerce",license:"MIT",type:"Software",desc:"Laravel-based open-source ecommerce platform.",latest:true},
{name:"Saleor",cat:"Ecommerce",license:"BSD-3-Clause",type:"Software",desc:"API-first commerce platform for scalable stores.",latest:true},
{name:"FastAPI",cat:"Developer Tools",license:"MIT",type:"Software",desc:"Modern Python framework for building APIs.",latest:true},
{name:"Playwright",cat:"Automation",license:"Apache-2.0",type:"Software",desc:"Browser automation and end-to-end testing.",latest:true},
{name:"Blender",cat:"3D / Video",license:"GPL-3.0",type:"Media",desc:"3D creation, animation, rendering and video editing."},
{name:"GIMP",cat:"Images",license:"GPL-3.0",type:"Media",desc:"Free image editing and graphic design software."},
{name:"Audacity",cat:"Audio",license:"GPL-3.0",type:"Media",desc:"Audio recording and editing software."},
{name:"Krita",cat:"Images",license:"GPL-3.0",type:"Media",desc:"Digital painting and illustration application."},
{name:"OpenShot",cat:"Video",license:"GPL-3.0",type:"Media",desc:"Open-source video editor for desktop."},
{name:"OpenStax",cat:"Books",license:"CC BY 4.0",type:"Course",desc:"Free peer-reviewed open textbooks."},
{name:"freeCodeCamp",cat:"Courses",license:"BSD-3-Clause",type:"Course",desc:"Free coding curriculum and interactive practice."}
];
const categories=[...new Set(items.map(x=>x.cat)),"Operating Systems","Inventory","POS","AI / LLM","APIs","Games","Templates","Websites","Databases","Security","Cloud","Islamic Resources","Books","Courses","Pictures","Video","Audio"];
const esc=s=>s.replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function card(x){return '<article class="card"><span class="tag">'+esc(x.cat)+'</span><h3>'+esc(x.name)+'</h3><p>'+esc(x.desc)+'</p><div class="meta"><strong>'+esc(x.license)+'</strong><span>'+esc(x.type)+' • Free catalog</span></div></article>'}
function render(query=""){const q=query.toLowerCase();const found=items.filter(x=>(x.name+" "+x.cat+" "+x.license+" "+x.desc).toLowerCase().includes(q));document.querySelector("#latest-grid").innerHTML=found.filter(x=>x.latest).map(card).join("")||"<p>No matching resources found.</p>";document.querySelector("#software-grid").innerHTML=found.filter(x=>x.type==="Software").map(card).join("")||"<p>No matching software found.</p>";document.querySelector("#media-grid").innerHTML=found.filter(x=>x.type==="Media").map(card).join("")||"<p>No matching media found.</p>";document.querySelector("#courses-grid").innerHTML=found.filter(x=>x.type==="Course").map(card).join("")||"<p>No matching courses found.</p>";document.querySelector("#count").textContent=found.length+" catalog entries"}document.querySelector("#category-list").innerHTML=categories.map(x=>'<a href="#software" data-category="'+esc(x)+'">'+esc(x)+'</a>').join("");document.querySelector("#search").addEventListener("input",e=>render(e.target.value));document.querySelector("#clear").addEventListener("click",()=>{document.querySelector("#search").value="";render()});render();