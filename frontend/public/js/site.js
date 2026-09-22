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
})();
