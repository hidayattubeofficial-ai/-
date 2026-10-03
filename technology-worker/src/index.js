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
.card h3{margin:0 0 8px}.card a{color:var(--green);font-weight:700;text-decoration:none}.pill{display:inline-block;background:#e5f3ed;color:var(--green);padding:5px 9px;border-radius:999px;font-size:12px}
footer{max-width:1120px;margin:50px auto;padding:20px 18px;color:var(--muted)}
.empty{padding:24px;border:1px dashed #b9c9c1;border-radius:14px;background:#fff}
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
    ).bind(category,category,category,category).all();
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
  return '<div class="grid">' + items.map(item => `<article class="card">
<span class="pill">${esc(item.category || "Technology")}</span>
<h3>${esc(item.title || item.name || "Untitled")}</h3>
<p class="muted">${esc(item.description || item.summary || "")}</p>
${item.source_url ? `<a href="${esc(item.source_url)}" target="_blank" rel="noopener">Open resource →</a>` : ""}
</article>`).join("") + "</div>";
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

      if (url.pathname === "/catalog") {
        const items = await loadCatalog(env.DB);
        return new Response(page("Software & Tools", `<section class="hero"><h1>Software & Tools</h1><p class="muted">Published technology resources connected directly to Hidayat Technology D1.</p></section><h2>Catalog</h2>${catalogCards(items)}`), {headers:HTML_HEADERS});
      }

      if (url.pathname === "/transcript") {
        return new Response(page("YouTube Transcript", `<section class="hero"><h1>YouTube Transcript</h1><p class="muted">Transcript functionality is reserved for a real transcript provider/API. No fake transcript data is shown.</p><div class="empty">Backend route is ready for integration; published posts and catalog data remain sourced from D1.</div></section>`), {headers:HTML_HEADERS});
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
      return new Response(page("Home", `<section class="hero"><h1>AI • Technology • Practical Knowledge</h1><p class="muted">Explore Hidayat Technology categories and published software/resources. Every category opens its own page.</p></section><h2>Categories</h2><div class="grid">${categoryCards(categories)}</div><h2>Latest Software & Tools</h2>${catalogCards(items.slice(0,12))}`), {headers:HTML_HEADERS});
    } catch (error) {
      return json({ok:false,error:String(error?.message || error)},500);
    }
  }
};