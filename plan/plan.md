# Correção do site Snooker Club Salto na Vercel

Conserto do site publicado do Snooker Club Salto, que hoje mostra só o menu e um fundo azul escuro vazio no lugar do conteúdo.
O aviso `npm warn Unknown env config "cache-dir"` é inofensivo (vem da própria Vercel e o deploy termina como "Ready"), então não é a causa.

## Para quem é
- O dono do clube, que publica o site pela Vercel.
- Visitantes no celular que precisam ver o clube, a galeria, os campeonatos, as lives, os horários e o contato.

## O que vai ser corrigido
- **Conteúdo invisível:** as seções abaixo do menu (O Clube, Galeria, Campeonatos, Lives, Horários, Contato) precisam aparecer de novo, no celular e no computador.
- **Causas mais prováveis, a confirmar no código:**
  1. Seções com animação de "aparecer ao rolar" que ficam presas como transparentes no celular.
  2. Seções que buscam dados de um servidor que não existe na Vercel (a Vercel hospeda só a parte visual). Nesse caso, ou ficam vazias ou ficam carregando para sempre.
- **Segurança:** se os dados não carregarem, as seções mostram um conteúdo padrão em vez de um espaço vazio.
- **Aviso do npm:** fica como está. É só um aviso e não atrapalha.

## Fluxo do usuário
1. O visitante abre o link da Vercel.
2. Ele vê o topo com o título "O maior clube de Snooker da região", os botões e o logo.
3. Ao rolar, cada seção aparece com o conteúdo e as fotos.
4. Os botões do menu levam até a seção certa, e o botão do WhatsApp continua funcionando.

## Visual
O visual não muda. Continuam o tema azul-noite com dourado, a mesma tipografia e o mesmo layout. A correção mexe só no que impede o conteúdo de aparecer.

## Fases
- **Fase 1 (agora):** trazer o código do repositório `Kevin-290305/Snookerclub`, encontrar por que as seções ficam vazias, corrigir e conferir no celular e no computador. Depois disso, as mudanças são enviadas para o GitHub, e a Vercel faz o redeploy sozinha.
- **Fase 2:** se o site precisar de dados que mudam (como campeonatos e horários editáveis pelo admin), publicar o servidor em um lugar que roda o servidor junto do site, porque a Vercel sozinha não roda essa parte.
- **Fase 3:** organizar os deploys. Hoje eles saem da branch `conflict_220926_1926`, e a ideia é passar a usar uma única branch principal para não confundir prévia com produção.

## Suposições
- O código do site está no GitHub `Kevin-290305/Snookerclub` e não neste espaço de trabalho, que está vazio. É preciso conectar ou importar esse repositório.
- O topo do site aparece certo, como mostra a miniatura da Vercel, e o problema está nas seções de baixo e/ou nos dados.
- Textos, fotos e contatos atuais são mantidos. Nada novo é inventado.
- O site continua hospedado na Vercel.
