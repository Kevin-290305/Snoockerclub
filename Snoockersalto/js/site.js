/* Snooker Club Salto — interações mínimas em JavaScript puro.
   O site é HTML + CSS; este arquivo só complementa o que é
   impossível sem script: status aberto/fechado, formulário
   do WhatsApp e animações de entrada. */
(function () {
  "use strict";

  document.documentElement.classList.add("js");

  /* Ano no rodapé */
  var ano = String(new Date().getFullYear());
  document.querySelectorAll("[data-ano]").forEach(function (el) {
    el.textContent = ano;
  });

  /* Horário de funcionamento — fuso de Salto/SP */
  var HOURS = [
    [17, 23], // 0 domingo
    [15, 23], // 1 segunda
    null,     // 2 terça (fechado)
    [15, 23], // 3 quarta
    [15, 23], // 4 quinta
    [15, 23], // 5 sexta
    [14, 23], // 6 sábado
  ];

  var sp = new Date(new Date().toLocaleString("en-US", { timeZone: "America/Sao_Paulo" }));
  var day = sp.getDay();
  var hour = sp.getHours() + sp.getMinutes() / 60;
  var today = HOURS[day];
  var aberto = !!today && hour >= today[0] && hour < today[1];

  document.querySelectorAll("[data-day]").forEach(function (li) {
    if (Number(li.getAttribute("data-day")) === day) li.classList.add("today");
  });

  document.querySelectorAll("[data-open-badge]").forEach(function (badge) {
    badge.classList.remove("is-open", "is-closed");
    badge.classList.add(aberto ? "is-open" : "is-closed");
    badge.innerHTML =
      '<span class="dot"></span>' + (aberto ? "Aberto agora" : "Fechado agora");
  });

  /* Revelar seções ao rolar */
  var reveals = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("revealed");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("revealed"); });
  }

  /* Formulário de inscrição → WhatsApp do clube */
  var form = document.getElementById("form-inscricao");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;

      var dados = new FormData(form);
      var linhas = [
        "*INSCRIÇÃO — SNOOKER CLUB SALTO*",
        "",
        "Modalidade: " + dados.get("modalidade"),
        "Nome/time: " + dados.get("nome"),
        "Idade: " + dados.get("idade"),
        "Sexo: " + dados.get("sexo"),
        "Campeonato: " + dados.get("campeonato"),
        "Telefone: " + dados.get("telefone"),
        "Cidade: " + dados.get("cidade"),
      ];
      var obs = (dados.get("obs") || "").trim();
      if (obs) linhas.push("Observações: " + obs);
      linhas.push("", "Enviado pelo site do clube.");

      var url =
        "https://wa.me/5511985157388?text=" + encodeURIComponent(linhas.join("\n"));
      window.open(url, "_blank", "noopener");

      var ok = document.getElementById("form-sucesso");
      if (ok) ok.hidden = false;
      form.querySelector("[data-testid='submit-register-whatsapp-btn']").textContent =
        "Inscrição enviada — confirme no WhatsApp";
    });
  }

  /* ---------- Campeonatos dinâmicos (painel do clube) ---------- */
  var TROFEU =
    '<svg class="champ-trophy" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M8 21h8m-4-4v4M7 4h10v5a5 5 0 0 1-10 0V4Z" stroke-linecap="round" stroke-linejoin="round"/><path d="M7 6H4v1a3 3 0 0 0 3 3M17 6h3v1a3 3 0 0 1-3 3" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var ICO_CAL =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4m8-4v4M3 11h18" stroke-linecap="round"/></svg>';
  var ICO_RELOGIO =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3" stroke-linecap="round"/></svg>';
  var ICO_PREMIO =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="8" r="6"/><path d="M15.5 13 17 22l-5-3-5 3 1.5-9" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function esc(t) {
    var d = document.createElement("div");
    d.textContent = t == null ? "" : String(t);
    return d.innerHTML;
  }

  function cardCampeonato(c) {
    return (
      '<article class="champ-card" data-testid="championship-card-item">' +
        '<div class="champ-top">' +
          '<span class="badge badge-open" data-testid="championship-status-badge"><span class="dot"></span>Inscrições abertas</span>' +
          TROFEU +
        "</div>" +
        "<h3>" + esc(c.title) + "</h3>" +
        (c.details ? '<p class="champ-details">' + esc(c.details) + "</p>" : "") +
        '<ul class="champ-info">' +
          "<li>" + ICO_CAL + '<span><strong>Data:</strong> ' + esc(c.date || "Data a confirmar") + "</span></li>" +
          "<li>" + ICO_RELOGIO + '<span><strong>Formato:</strong> ' + esc(c.format || "Consulte pelo WhatsApp") + "</span></li>" +
          "<li>" + ICO_PREMIO + '<span><strong>Premiação:</strong> ' + esc(c.prize || "A definir") + "</span></li>" +
        "</ul>" +
        '<a class="btn btn-gold btn-block" href="inscricao.html?campeonato=' + encodeURIComponent(c.title) + '" data-testid="championship-register-btn">Escrever meu time / me inscrever</a>' +
      "</article>"
    );
  }

  function carregarCampeonatos() {
    var lista = document.getElementById("champ-list");
    if (!lista) return;
    var items = Array.isArray(window.CAMPEONATOS) ? window.CAMPEONATOS : [];
    if (!items.length) {
      lista.innerHTML =
        '<div class="champ-empty" data-testid="championship-empty">' +
          "<h3>Nenhum campeonato aberto no momento</h3>" +
          "<p>Novos torneios são anunciados aqui, no Instagram do clube e no WhatsApp. Quer garantir vaga no próximo? Fale com a gente.</p>" +
          '<a class="btn btn-ghost" href="https://wa.me/5511985157388?text=' + encodeURIComponent("Olá! Quero saber quando abre o próximo campeonato do Snooker Club Salto.") + '" target="_blank" rel="noopener" data-testid="championship-waitlist-btn">Avisem-me do próximo</a>' +
        "</div>";
    } else {
      lista.innerHTML = items.map(cardCampeonato).join("");
    }
  }
  carregarCampeonatos();

  /* ---------- Opções de campeonato na ficha de inscrição ---------- */
  var selCamp = document.getElementById("f-campeonato");
  if (selCamp) {
    var itens = Array.isArray(window.CAMPEONATOS) ? window.CAMPEONATOS : [];
    selCamp.innerHTML = '<option value="" disabled selected>Selecione o campeonato</option>';
    itens.forEach(function (c) {
      var o = document.createElement("option");
      o.value = c.title;
      o.textContent = c.title;
      selCamp.appendChild(o);
    });
    var oAviso = document.createElement("option");
    oAviso.value = "Ainda não sei — quero ser avisado do próximo";
    oAviso.textContent = oAviso.value;
    selCamp.appendChild(oAviso);

    var pre = new URLSearchParams(location.search).get("campeonato");
    if (pre) {
      for (var i = 0; i < selCamp.options.length; i++) {
        if (selCamp.options[i].value === pre) {
          selCamp.value = pre;
          break;
        }
      }
    }
  }
})();
