const { put, list } = require("@vercel/blob");
const crypto = require("crypto");

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, x-admin-password",
};

const PADRAO = {
  senha: "FlavioSnoocker2026",
  campeonatos: [
    {
      title: "Campeonato de Sinuca — Snooker Club Salto",
      date: "Data a confirmar",
      format: "Individual ou dupla",
      prize: "A definir",
      details: "Novos torneios são anunciados aqui, no Instagram e no WhatsApp do clube.",
      status: "aberto",
    },
  ],
};

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

module.exports = async (req, res) => {
  Object.entries(CORS).forEach(([k, v]) => res.setHeader(k, v));
  if (req.method === "OPTIONS") {
    res.status(204).end();
    return;
  }
  try {
    let dados = await lerDados();
    if (!dados) {
      dados = PADRAO;
      await put("snooker-dados.json", JSON.stringify(dados), {
        access: "public",
        addRandomSuffix: false,
      });
    }
    const ok = mesmaSenha(req.headers["x-admin-password"], dados.senha);
    if (!ok) {
      res.status(401).json({ erro: "Senha incorreta" });
      return;
    }
    res.status(200).json({ campeonatos: dados.campeonatos || [] });
  } catch (e) {
    res.status(500).json({ erro: "Armazenamento do site não conectado" });
  }
};
