const JSON_HEADERS = {
  "content-type": "application/json; charset=UTF-8",
  "cache-control": "no-store",
  "access-control-allow-origin": "*"
};

const HTML_HEADERS = {
  "content-type": "text/html; charset=UTF-8",
  "cache-control": "no-store"
};

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: JSON_HEADERS });

const esc = (value) =>
  String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");

const slugify = (value) =>
  String(value ?? "")
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");

function page(title, body) {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)} | Hidayat Technology</title>
<style>
:root{color-scheme:light;--green:#0b6b4f;--dark:#12372a;--bg:#f5f8f6;--card:#fff;--muted:#64746d}
*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Arial,sans-serif;background:var(--bg);color:#17211d}
header{background:linear-gradient(135deg,#0b6b4f,#154c3b);color:#fff;padding:22px 18px;position:sticky;top:0;z-index:5}
.wrap{max-width:1120px;margin:auto}.brand{font-size:25px;font-weight:800}.tag{opacity:.9;margin-top:3px}
nav{display:flex;gap:8px;overflow:auto;margin-top:16px}nav a,.btn{color:#fff;text-decoration:none;border:1px solid rgba(255,255,255,.28);padding:9px 13px;border-radius:999px;white-space:nowrap}
main{max-width:1120px;margin:28px auto;padding:0 18px}.hero{background:#fff;border-radius:20px;padding:28px;box-shadow:0 8px 28px #12372a12}
h1{margin:0 0 8px;font-size:32px}h2{margin-top:30px}.muted{color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:18px}
.card{background:var(--card);border-radius:16px;padding:18px;box-shadow:0 5px 20px #12372a10;border:1px solid #e1e9e5}
.card h3{margin:0 0 8px}.card a{color:var(--green);font-weight:700;text-decoration:none}.btn2{display:inline-block;padding:8px 12px;border:1px solid #b8d8ca;border-radius:10px;background:#eef8f3;color:var(--green)!important}.pill{display:inline-block;background:#e5f3ed;color:var(--green);padding:5px 9px;border-radius:999px;font-size:12px}
.card-img{width:100%;height:150px;object-fit:cover;border-radius:12px;background:#e9f2ee;border:1px solid #d9e7e0;margin-bottom:14px}
.card-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
.btn3{display:inline-block;padding:9px 11px;border-radius:10px;border:1px solid #b8d8ca;text-decoration:none;font-weight:700;background:#fff;color:var(--green)!important}
.btn3.primary{background:var(--green);color:#fff!important;border-color:var(--green)}
.btn3.download{background:#12372a;color:#fff!important;border-color:#12372a}
footer{max-width:1120px;margin:50px auto;padding:20px 18px;color:var(--muted)}
.empty{padding:24px;border:1px dashed #b9c9c1;border-radius:14px;background:#fff}.ticker{overflow:hidden;background:#12372a;color:#fff;border-radius:14px;padding:12px 16px;margin-bottom:18px}.ticker-track{display:inline-block;white-space:nowrap;animation:ticker 28s linear infinite}.ticker-track:hover{animation-play-state:paused}@keyframes ticker{from{transform:translateX(100%)}to{transform:translateX(-100%)}}
</style>
</head>
<body>
<header><div class="wrap"><div class="brand">Hidayat Technology</div><div class="tag">AI • Technology • Practical Knowledge</div>
<nav><a href="/">Latest</a><a href="/catalog">Software & Tools</a><a href="/transcript">YouTube Transcript</a><a href="/api/categories">API</a></nav></div></header>
<main>${body}</main><footer>Hidayat Technology • Public site • Cloudflare + D1</footer>
</body></html>`;
}

async function loadCategories(db) {
  const r = await db.prepare(
    "SELECT id,name,slug,description,created_at FROM categories ORDER BY id"
  ).all();
  return r.results;
}

async function loadCatalog(db, category) {
  if (category) {
    const r = await db.prepare(
      "SELECT * FROM catalog_items WHERE status='published' AND (lower(category)=lower(?) OR (?='Software' AND category IN ('Technology','Developer Tools','Browsers','Security','Cloud & Web','System Tuning & Utilities','Web Design','WordPress','Video & Image','Ecommerce')) OR (?='AI & LLM' AND category='AI Tools') OR (?='Science & Quantum' AND category IN ('Quantum & Physics','Data Science')) OR (?='Marketing' AND category='SEO')) ORDER BY id DESC"
    ).bind(category,category,category,category,category).all();
    return r.results;
  }
  const r = await db.prepare(
    "SELECT * FROM catalog_items WHERE status='published' ORDER BY id DESC"
  ).all();
  return r.results;
}

function categoryCards(categories) {
  return categories.map(c => `<article class="card">
<h3>${esc(c.name)}</h3><p class="muted">${esc(c.description || "Explore this category.")}</p>
<a href="/category/${encodeURIComponent(c.slug)}">Open category →</a>
</article>`).join("");
}

function catalogCards(items) {
  if (!items.length) return '<div class="empty">No published catalog items are available in this category yet.</div>';
  return '<div class="grid">' + items.map(item => {
    const postSlug = 'auto-' + (item.slug || slugify(item.title || item.name || ''));
    const source = item.source_url || '';
    const image = item.image_url || 'https://dummyimage.com/900x500/e9f2ee/0b6b4f&text=' + encodeURIComponent(item.title || item.name || 'Hidayat Technology');
    const short = item.description || item.summary || 'Practical technology resource from the Hidayat Technology catalog.';
    const longUrl = '/post/' + encodeURIComponent(postSlug);
    const more = source ? '<a class="btn3" href="' + esc(source) + '" target="_blank" rel="noopener">More link →</a>' : '';
    const download = item.download_url ? '<a class="btn3 download" href="' + esc(item.download_url) + '" target="_blank" rel="noopener" download>Download ↓</a>' : '';
    return '<article class="card"><img class="card-img" src="' + esc(image) + '" alt="' + esc(item.title || item.name || 'Resource') + '"><span class="pill">' + esc(item.category || 'Technology') + '</span><h3>' + esc(item.title || item.name || 'Untitled') + '</h3><p class="muted">' + esc(short) + '</p><div class="card-actions"><a class="btn3 primary" href="' + longUrl + '">Long detail →</a>' + more + download + '</div></article>';
  }).join('') + '</div>';
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (!env.DB) return json({ok:false,error:"D1 binding DB is not configured"},503);

    try {
      if (url.pathname === "/api/categories") return json({ok:true,items:await loadCategories(env.DB)});

      if (url.pathname === "/api/catalog") {
        const category = url.searchParams.get("category");
        return json({ok:true,items:await loadCatalog(env.DB, category)});
      }

      if (url.pathname === "/api/posts") {
        const category = url.searchParams.get("category");
        const sql = category
          ? "SELECT p.*,c.name AS category_name,c.slug AS category_slug FROM posts p LEFT JOIN categories c ON c.id=p.category_id WHERE p.status='published' AND c.slug=? ORDER BY COALESCE(p.published_at,p.created_at) DESC"
          : "SELECT p.*,c.name AS category_name,c.slug AS category_slug FROM posts p LEFT JOIN categories c ON c.id=p.category_id WHERE p.status='published' ORDER BY COALESCE(p.published_at,p.created_at) DESC";
        const r = category ? await env.DB.prepare(sql).bind(category).all() : await env.DB.prepare(sql).all();
        return json({ok:true,items:r.results});
      }

      if (url.pathname.startsWith("/api/posts/")) {
        const slug = decodeURIComponent(url.pathname.slice("/api/posts/".length));
        const item = await env.DB.prepare(
          "SELECT p.*,c.name AS category_name,c.slug AS category_slug FROM posts p LEFT JOIN categories c ON c.id=p.category_id WHERE p.slug=? AND p.status='published' LIMIT 1"
        ).bind(slug).first();
        return item ? json({ok:true,item}) : json({ok:false,error:"Not found"},404);
      }

      if (url.pathname.startsWith("/api/transcript") && request.method === "POST") {
        if (!env.TRANSCRIPT_API_KEY) return json({ok:false,error:"Transcript provider key is not configured."},503);
        const b = await request.json();
        const r = await fetch("https://www.youtubetranscript.dev/api/v2/transcribe",{method:"POST",headers:{"Authorization":"Bearer "+env.TRANSCRIPT_API_KEY,"Content-Type":"application/json"},body:JSON.stringify({video:String(b?.video||""),format:{timestamp:true,paragraphs:true}})});
        const t = await r.text(); let d; try { d=JSON.parse(t); } catch { d={error:t}; }
        return json(r.ok?{ok:true,data:d}:{ok:false,error:d?.message||d?.error||"Provider error",provider_status:r.status},r.status);
      }

      if (url.pathname.startsWith("/post/")) {
        const slug = decodeURIComponent(url.pathname.slice("/post/".length));
        const item = await env.DB.prepare("SELECT p.*,c.name AS category_name,c.slug AS category_slug FROM posts p LEFT JOIN categories c ON c.id=p.category_id WHERE p.slug=? AND p.status='published' LIMIT 1").bind(slug).first();
        if (!item) return new Response(page("Post not found", '<div class="empty"><h1>Post not found</h1><a href="/">Back to Hidayat Technology</a></div>'), {status:404,headers:HTML_HEADERS});
        const content = esc(item.content).replaceAll("\n","<br>");
        const catalogSlug = slug.startsWith("auto-") ? slug.slice(5) : "";
        const catalog = catalogSlug
          ? await env.DB.prepare("SELECT title,source_url,category,description FROM catalog_items WHERE slug=? LIMIT 1").bind(catalogSlug).first()
          : null;
        const source = catalog?.source_url
          ? '<div class="card" style="margin-top:20px"><strong>Official source</strong><br><a class="btn2" href="'+esc(catalog.source_url)+'" target="_blank" rel="noopener">Open official source →</a></div>'
          : '<div class="card" style="margin-top:20px"><strong>Source</strong><p class="muted">Hidayat Technology catalog</p><p class="muted">An official source link is added when this catalog resource has a verified source URL.</p></div>';
        return new Response(page(item.title, '<article class="hero"><span class="pill">'+esc(item.category_name || "Technology")+'</span><h1>'+esc(item.title)+'</h1><p class="muted">'+esc(item.excerpt || "")+'</p><div class="card" style="margin-top:20px;line-height:1.8">'+content+'</div>'+source+'</article>'), {headers:HTML_HEADERS});
      }

      if (url.pathname === "/catalog") {
        const items = await loadCatalog(env.DB);
        return new Response(page("Software & Tools", `<section class="hero"><h1>Software & Tools</h1><p class="muted">Published technology resources connected directly to Hidayat Technology D1.</p></section><h2>Catalog</h2>${catalogCards(items)}`), {headers:HTML_HEADERS});
      }

      if (url.pathname === "/transcript") {
        return new Response(page("YouTube Transcript", '<section class="hero"><h1>YouTube Transcript</h1><p class="muted">Paste a public YouTube URL to fetch a real transcript. No fake transcript data is generated.</p><form id="tf" class="card" style="margin-top:16px"><input id="video" placeholder="https://www.youtube.com/watch?v=..." required style="width:100%;padding:12px;margin-bottom:10px"><button class="btn2" type="submit">Fetch Transcript →</button></form><div id="status" class="empty" style="margin-top:16px">Ready.</div><pre id="out" class="card" style="white-space:pre-wrap;display:none;margin-top:16px"></pre></section><script>tf.onsubmit=async e=>{e.preventDefault();status.textContent="Fetching…";try{const r=await fetch("/api/transcript",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({video:video.value})});const x=await r.json();if(!x.ok)throw Error(x.error||"Transcript failed");const d=x.data?.data||x.data||{},t=d.transcript||{};out.textContent=(d.video_title?d.video_title+"\\n\\n":"")+(t.text||"");out.style.display="block";status.textContent="Transcript fetched successfully."}catch(e){status.textContent="Error: "+e.message}}</script>'), {headers:HTML_HEADERS});
      }

      if (url.pathname.startsWith("/category/")) {
        const slug = decodeURIComponent(url.pathname.slice("/category/".length));
        const categories = await loadCategories(env.DB);
        const category = categories.find(c => c.slug === slug);
        if (!category) return new Response(page("Not found", '<div class="empty"><h1>Category not found</h1><a href="/">Back to Hidayat Technology</a></div>'), {status:404,headers:HTML_HEADERS});
        const items = await loadCatalog(env.DB, category.name);
        return new Response(page(category.name, `<section class="hero"><span class="pill">Category</span><h1>${esc(category.name)}</h1><p class="muted">${esc(category.description || "")}</p></section><h2>${esc(category.name)} resources</h2>${catalogCards(items)}`), {headers:HTML_HEADERS});
      }

      const categories = await loadCategories(env.DB);
      const items = await loadCatalog(env.DB);
      return new Response(page("Home", `<div class="ticker" aria-label="Latest headlines"><div class="ticker-track"><strong>Latest:</strong> ${items.slice(0,8).map(i=>esc(i.title || i.name || "New resource")).join(" • ")}</div></div><section class="hero"><h1>AI • Technology • Practical Knowledge</h1><p class="muted">Explore Hidayat Technology categories and published software/resources. Every category opens its own page.</p></section><h2>Home Categories</h2><div class="grid">${categoryCards(categories)}</div><h2>Latest Software & Tools</h2>${catalogCards(items.slice(0,12))}`), {headers:HTML_HEADERS});
    } catch (error) {
      return json({ok:false,error:String(error?.message || error)},500);
    }
  }
};