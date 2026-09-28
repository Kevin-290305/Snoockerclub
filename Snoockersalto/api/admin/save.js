const { put, list } = require("@vercel/blob");
const crypto = require("crypto");

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, x-admin-password",
};

const STATUS_VALIDOS = ["aberto", "pausado", "cancelado"];

async function lerDados() {
  const resultado = await list({ prefix: "snooker-dados.json" });
  if (!resultado.blobs.length) return null;
  const res = await fetch(resultado.blobs[0].url);
  return await res.json();
}

function mesmaSenha(a, b) {
  const x = Buffer.from(String(a));
  const y = Buffer.from(String(b || ""));
  return x.length === y.length && crypto.timingSafeEqual(x, y);
}

function lerCorpo(req) {
  return new Promise((resolve, reject) => {
    let t = "";
    req.on("data", (c) => (t += c));
    req.on("end", () => {
      try {
        resolve(t ? JSON.parse(t) : {});
      } catch (e) {
        reject(e);
      }
    });
    req.on("error", reject);
  });
}

module.exports = async (req, res) => {
  Object.entries(CORS).forEach(([k, v]) => res.setHeader(k, v));
  if (req.method === "OPTIONS") {
    res.status(204).end();
    return;
  }
  try {
    let dados = await lerDados();
    if (!dados) dados = { senha: "FlavioSnoocker2026", campeonatos: [] };
    const corpo = await lerCorpo(req);
    if (!mesmaSenha(corpo.password, dados.senha)) {
      res.status(401).json({ erro: "Senha incorreta" });
      return;
    }
    if (!Array.isArray(corpo.campeonatos)) {
      res.status(400).json({ erro: "Lista inválida" });
      return;
    }
    const limpos = corpo.campeonatos
      .filter((c) => c && String(c.title || "").trim())
      .map((c) => ({
        title: String(c.title).slice(0, 120),
        date: String(c.date || "Data a confirmar").slice(0, 120),
        format: String(c.format || "").slice(0, 120),
        prize: String(c.prize || "").slice(0, 120),
        details: String(c.details || "").slice(0, 300),
        status: STATUS_VALIDOS.indexOf(c.status) >= 0 ? c.status : "aberto",
      }));
    dados.campeonatos = limpos;
    await put("snooker-dados.json", JSON.stringify(dados), {
      access: "public",
      addRandomSuffix: false,
    });
    res.status(200).json({ ok: true });
  } catch (e) {
    res.status(500).json({ erro: "Armazenamento do site não conectado" });
  }
};
