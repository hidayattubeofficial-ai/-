export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const headers = {
      "content-type": "application/json; charset=UTF-8",
      "cache-control": "no-store",
      "access-control-allow-origin": "*"
    };
    const json = (data, status = 200) =>
      new Response(JSON.stringify(data), { status, headers });

    if (!env.DB) return json({ ok: false, error: "D1 binding DB is not configured" }, 503);

    try {
      if (url.pathname === "/api/categories") {
        const r = await env.DB.prepare(
          "SELECT id,name,slug,description,created_at FROM categories ORDER BY id"
        ).all();
        return json({ ok: true, items: r.results });
      }

      if (url.pathname === "/api/catalog") {
        const category = url.searchParams.get("category");
        const sql = category
          ? "SELECT * FROM catalog_items WHERE status='published' AND lower(category)=lower(?) ORDER BY id DESC"
          : "SELECT * FROM catalog_items WHERE status='published' ORDER BY id DESC";
        const r = category
          ? await env.DB.prepare(sql).bind(category).all()
          : await env.DB.prepare(sql).all();
        return json({ ok: true, items: r.results });
      }

      if (url.pathname === "/api/posts") {
        const category = url.searchParams.get("category");
        const sql = category
          ? "SELECT p.*,c.name AS category_name,c.slug AS category_slug FROM posts p LEFT JOIN categories c ON c.id=p.category_id WHERE p.status='published' AND c.slug=? ORDER BY COALESCE(p.published_at,p.created_at) DESC"
          : "SELECT p.*,c.name AS category_name,c.slug AS category_slug FROM posts p LEFT JOIN categories c ON c.id=p.category_id WHERE p.status='published' ORDER BY COALESCE(p.published_at,p.created_at) DESC";
        const r = category
          ? await env.DB.prepare(sql).bind(category).all()
          : await env.DB.prepare(sql).all();
        return json({ ok: true, items: r.results });
      }

      if (url.pathname.startsWith("/api/posts/")) {
        const slug = decodeURIComponent(url.pathname.slice("/api/posts/".length));
        const item = await env.DB.prepare(
          "SELECT p.*,c.name AS category_name,c.slug AS category_slug FROM posts p LEFT JOIN categories c ON c.id=p.category_id WHERE p.slug=? AND p.status='published' LIMIT 1"
        ).bind(slug).first();
        return item
          ? json({ ok: true, item })
          : json({ ok: false, error: "Not found" }, 404);
      }

      return new Response("Hidayat Technology API", {
        status: 200,
        headers: { "content-type": "text/plain; charset=UTF-8" }
      });
    } catch (error) {
      return json({ ok: false, error: String(error?.message || error) }, 500);
    }
  }
};