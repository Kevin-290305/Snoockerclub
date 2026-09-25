# PRD — Snooker Club Salto (Site Oficial)

## Problema original
Criar um site profissional e interativo para o Snooker Club Salto (Salto/SP), mantendo o tema e a paleta da logo enviada (azul-marinho, vermelho, verde-feltro, creme/dourado), com tema de sinuca no site inteiro, seções de sobre/horários/contato, campeonatos, lives do YouTube, galeria com as 4 fotos reais do local + fotos profissionais, e fluxo de inscrição em campeonatos que envia os dados pelo WhatsApp do clube.

## Decisões do usuário (coletadas via ask_human)
- Estilo: mistura de "escuro e moderno" (fundo escuro de mesa de sinuca, verde/vermelho/dourado) com "clássico inglês" (madeira, ambiente tradicional).
- Recursos: galeria + botão flutuante de WhatsApp + seção de campeonatos em destaque + link das lives do YouTube.
- Telefone do clube: +55 11 98515-7388. Formulário de inscrição com (nome ou nome do time, idade, sexo, para qual campeonato, dados da pessoa) enviado para o WhatsApp do clube.
- Logo: recriar em alta qualidade mantendo o estilo (feito com image generation a partir da logo original).
- Atualização do usuário no meio do build: "faça tudo em HTML e CSS" → site estático em HTML + CSS puros (sem React), com um mini script vanilla JS apenas para: status aberto/fechado, formulário → WhatsApp e reveals de scroll.

## Arquitetura
- Servido pelo dev server do Create React App (port 3000) a partir de /app/frontend/public:
  - index.html (one-page: hero cinético, marquee, manifesto numerado, galeria com lightbox CSS puro (:target), campeonatos, lives YouTube, horários, contato, footer, FAB WhatsApp)
  - inscricao.html (ficha de inscrição → wa.me/5511985157388 com mensagem formatada)
  - css/style.css (design system: tokens da logo, Cinzel + Cormorant Garamond + Plus Jakarta Sans, madeira/latão/feltro, responsivo 1440/390)
  - js/site.js (vanilla: badge aberto/fechado no fuso America/Sao_Paulo, destaque do dia atual, IntersectionObserver reveals, submit do formulário)
  - img/ (logo recriada em alta resolução + 4 fotos reais do clube)
- Backend FastAPI não é usado pelo site (decisão: site 100% estático a pedido do usuário). server.py template permanece intacto.

## Conteúdo (integridade — apenas fatos fornecidos)
- Nome: Snooker Club Salto · Desde 2022 · Slogan: "O maior clube de Snooker da região"
- Diferencial: conforto e entretenimento a todas as famílias, experiência única pelo esporte da sinuca
- Endereço: Rua John Kennedy, 379 - Bela Vista, Salto/SP, CEP 13321-380 · Maps: plus code RP36+QC
- WhatsApp: (11) 98515-7388 (+55 11 98515-7388) · Instagram: @snookerclub_salto · YouTube: Kauã da Sinuquinha (youtube.com/@kauadasinuquinha)
- Horários: Seg 15-23 · Ter fechado · Qua-Qui-Sex 15-23 · Sáb 14-23 · Dom 17-23

## Status
- 2026-09-22: MVP entregue — home completa + página de inscrição, verificado com screenshots (desktop 1440 e mobile 390) e curl 200 em todas as rotas. Corrigidos: caminho %PUBLIC_URL% em inscricao.html (página sem estilo), overflow-x dos inputs de rádio, contraste/cor do botão da navbar.
- 2026-09-22: Responsividade completa — verificado sem overflow-x em 1920×1080, 1440×900, 768×1024, 414×896, 390×844 e 360×800. Menu hamburger ativado até 900px, navbar compacta ≤1180px, breakpoints novos: ≤400px (celulares pequenos), paisagem baixa (max-height 560), ≥1600px (monitores grandes), @media (hover: none) para legendas da galeria em toque.
- 2026-09-22: Link do Instagram corrigido para https://www.instagram.com/snookerclube_salto/ (home + inscrição + JSON-LD; frontend reiniciado para limpar cache do template).
- 2026-09-22: Pasta organizada /app/Snoockersalto (index.html, inscricao.html, css/, js/, img/, LEIA-ME.txt) com cópia limpa e portátil do site + /app/Snoockersalto.zip para download. Site no preview segue servido por frontend/public.
- 2026-09-22: Campeonatos dinâmicos + painel do clube — backend FastAPI/Mongo (/api/campeonatos público; /api/admin/* protegido por senha via header x-admin-password + hmac.compare_digest, conforme playbook do integration_expert); inscrições também gravadas no banco e visíveis no painel; painel em /admin.html (senha em backend/.env ADMIN_PASSWORD e em test_credentials.md); home renderiza cards da API com estado vazio; seletor da ficha de inscrição populado pela API + pré-seleção via ?campeonato=. Corrigidos durante o build: trailing brace errado no Promise.all do admin (JS "Unexpected token }") e fechamento do bloco @media (hover:none) comido ao adicionar estilos novos (regras do mapa/admin mortas).
- 2026-09-22: Google Maps incorporado na seção de contato (iframe output=embed sem chave, endereço completo) + botão "Traçar rota" (maps.dir) — iframe a 1162×400 verificado.
- 2026-09-22: Dados de exemplo no banco (removíveis pelo painel): campeonatos "Campeonato de Sinuca — Snooker Club Salto" (seed automático) e "Copa Kauã da Sinuquinha" (criado em teste); 0 inscrições.
- 2026-09-22: Senha do painel trocada pelo usuário para FlavioSnoocker2026 (responsável: Flavio) — antiga invalidada (401), nova validada; seção "Campeonatos publicados" no painel agora rotulada deixando claro o botão Excluir por campeonato; pasta Snoockersalto + zip atualizados.
- 2026-09-22: Olhinho para mostrar/ocultar a senha no portão do painel (/admin.html) — testado: alterna password↔text e volta; pasta Snoockersalto + zip atualizados.
- 2026-09-25: Revisão dos arquivos enviados pelo usuário (local): .env correto (FlavioSnoocker2026), admin/inscricao/pytest ok, index local com 4 fotos da galeria com src/alt trocados (correção instruída ao usuário). Causa do "senha incorreta" local: sem backend rodando. Melhorias: backend tolerante a MongoDB ausente no seed, backend serve o site estático na porta 8001 (uma só porta no teste local), mensagem de erro do portão diferencia senha errada × servidor ausente, Snoockersalto/backend + LEIA-ME com passo a passo local. Preview validado: login FlavioSnoocker2026 = 200; senha errada = 401 com mensagem explicativa.

## Backlog
- P1: Backend (FastAPI + Mongo) para campeonatos dinâmicos + painel admin protegido por senha (hoje os campeonatos são um bloco HTML fácil de editar, marcado com comentário).
- P1: Incorporar vídeos/lives reais do canal (ex.:últimos vídeos via YouTube API).
- P2: Galeria com mais fotos e filtros; depoimentos de clientes.
