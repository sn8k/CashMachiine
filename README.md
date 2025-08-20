# Goal-Based Investment Copilot — Spécification fonctionnelle v0.1.8

[![Lint](https://github.com/OpenAI/CashMachiine/actions/workflows/ci.yml/badge.svg?branch=main&job=lint)](https://github.com/OpenAI/CashMachiine/actions/workflows/ci.yml?query=branch%3Amain)
[![Tests](https://github.com/OpenAI/CashMachiine/actions/workflows/ci.yml/badge.svg?branch=main&job=test)](https://github.com/OpenAI/CashMachiine/actions/workflows/ci.yml?query=branch%3Amain)
[![Build](https://github.com/OpenAI/CashMachiine/actions/workflows/ci.yml/badge.svg?branch=main&job=build)](https://github.com/OpenAI/CashMachiine/actions/workflows/ci.yml?query=branch%3Amain)

*Date : 2025-08-20*

Consultez le [manuel utilisateur](user_manual_2025-08-20.md) pour l'installation, l'utilisation, l'architecture et le dépannage. Consultez aussi les [tâches de développement](development_tasks.md) pour la feuille de route.

## 1) Vision & cas d’usage

Construire un logiciel qui, à partir d’un **capital initial**, d’un **objectif financier** (montant cible) et d’une **date d’échéance**, génère **chaque jour** des recommandations d’actions concrètes (acheter, vendre, ajuster l’allocation, placer sur un support sécurisé, etc.), avec **historique traçable** (checklist des actions exécutées) et **surveillance continue** du retour sur investissement.

### Exemples

* Entrée : 1 000 € → 300 000 € d’ici le 01/01/2031.
* Le système produit chaque matin (TZ Europe/Paris) une liste d’actions : « Allouer 15% en ETF monde, 5% en or, 30% en momentum crypto, 50% en monétaire » ; « Déplacer 10% du portefeuille vers cash (volatilité trop élevée) » ; « Prendre 20% de profits sur BTC (TP atteint) » ; etc.

> **Garde-fous** : L’objectif peut être **irréaliste** sans horizon adapté ; le système doit **mesurer la faisabilité** et **optimiser la probabilité d’atteinte** plutôt que « promettre » un résultat.

---

## 2) Entrées & paramètres

* **Capital initial** (€, multi-devises supportées via FX).
* **Montant cible** & **date d’échéance**.
* **Tolérance au risque** (profil : prudent, équilibré, dynamique, spéculatif) + **pertes max tolérées** (ex. -20% peak-to-trough).
* **Contraintes** : univers d’actifs autorisés (actions/ETF/oblig/crypto/DeFi/CFD/…); taille min/max par position ; levier autorisé ou non ; fiscalité (pays) ; frais & slippage ; heures de trading ; ESG, exclusions.
* **Comptes & courtiers** : IBKR / Degiro / Binance / Kraken / etc. (connecteurs pluggables).

---

## 3) Sorties attendues (quotidiennes)

1. **Plan d’actions du jour** (Actionables) : liste horodatée et *cochable* (pending → done/ignored). Chaque action inclut :

   * Instrument, côté (buy/sell), taille, prix limite/market, motif (« TP atteint », « signal momentum », « réduction risque »).
   * Impact estimé sur probabilité d’atteinte de l’objectif.
2. **État de progression** : distance au but, probabilité d’atteinte (estimée), trajectoire cible vs trajectoire réelle.
3. **Alertes** : drawdown, stop-loss, sur-risque, dérive d’allocation, événement macro (optionnel).
4. **Journal complet / audit** : décisions, exécutions, écarts, PnL réalisé/non-réalisé, frais, commentaires.

---

## 4) Cœur algorithmique (goal-based investing)

* **Moteur d’objectifs** : calcule la **probabilité d’atteinte** (PoH) du but à l’échéance, compte tenu de l’allocation et des distributions de rendement/risque. Optimise la **trajectoire de risque** au fil du temps.
* **Optimisation d’allocation** (multi-approches, ensemble) :

  * Couches **core/satellite** :

    * *Core* (long terme) : MPT robuste / Black–Litterman / volatilité cible ;
    * *Satellite* (tactique) : momentum, trend-following, carry, mean-reversion, événements.
  * **Contrôle du risque** : budget de risque quotidien/hebdo, volatilité cible, **Kelly fraction** plafonnée, VaR/ES contraintes.
  * **Programmation dynamique** (optionnel) : politique de risque variable dans le temps pour maximiser PoH sous contraintes (drawdown, levier, taille).
* **Générateur d’actions** : traduit les écarts (target vs actuel) en ordres (position sizing, TP/SL, trailing stops), avec **cohérence multi-comptes** et coûts.
* **Simulation** : Monte-Carlo / bootstrap / walk-forward pour estimer PoH, PnL et drawdown avant émission des recommandations.

> Philosophie : **maximiser la probabilité d’atteindre l’objectif** sous contraintes, pas le rendement espéré brut.

---

## 5) Données & connecteurs (modulaires)

* **Prix & fondamentaux** : actions/ETF (Euronext/US), obligations, matières premières, FX, crypto.
* Fetchers Alpha Vantage pour obligations et matières premières via le bus de messages.
* **Flux crypto** : CEX (Binance/Kraken/Bybit), DEX (via indexeurs), funding, open interest (si autorisé).
* **Macro/news/sentiment** (optionnels, pondérés faiblement par défaut).
* **Courtiers / exécution** : IBKR, Degiro, Binance, Kraken… (clé API, sandbox d’abord).
* **Calendrier** : earnings, dividendes, macro (BCE/Fed), expirations dérivés.

---

## 6) Architecture technique

Voir aussi la section [Architecture](user_manual_2025-08-19.md#architecture) du manuel utilisateur.

**Monorepo** avec services conteneurisés (Docker) :

* `api-gateway` (FastAPI / NestJS) — Auth, RBAC, routes publiques, Webhook brokers.
* `orchestrator` — planifie la routine quotidienne (08:00 Europe/Paris) + jobs intraday.
* `data-ingestion` — connecteurs de marché (pull/stream), normalisation OHLCV.
* `strategy-engine` — signaux, allocations cibles, simulation Monte-Carlo.
* `risk-engine` — budget de risque, limites (VaR/ES), SL/TP, levier, détection d'anomalies.
* `execution-engine` — génération d’ordres, agrégation par broker, contrôle post-trade.
* `backtester` — backtests/forward-tests reproductibles, rapports.
* `ui` (Next.js/React + Tailwind) — Dashboard, Analytics, Wizard d’objectifs, Daily Actionables, Historique, What‑if.
* `db` — Postgres (+ Timescale pour séries), Redis pour cache/queues.
* Bus messages : NATS/RabbitMQ (événements de marché, signaux, ordres, logs).

**Observabilité** : logs structurés, metrics Prometheus, traces OpenTelemetry, tableau de bord Grafana.

---

## 7) Modèle de données (schéma simplifié)

* `users(id, email, tz, kyc_level, risk_profile, created_at)`
* `goals(id, user_id, name, start_capital, target_amount, deadline, feasibility_score, risk_bounds, created_at)`
* `accounts(id, user_id, broker, base_ccy, margin_allowed, fees_model)`
* `portfolios(id, user_id, goal_id, name)`
* `positions(id, portfolio_id, symbol, venue, qty, avg_price, leverage, created_at)`
* `orders(id, account_id, symbol, side, qty, type, limit_price, status, reason, sl, tp, created_at)`
* `executions(id, order_id, price, qty, fee, ts)`
* `prices(symbol, venue, ts, o, h, l, c, v)` (Timescale hypertable)
* `signals(id, symbol, kind, value, horizon, confidence, ts)`
* `actions(id, goal_id, day, title, details_json, status{pending|done|ignored}, created_at)`
* `risk_limits(id, portfolio_id, max_dd, max_var, vol_target, kelly_cap)`
* `metrics_daily(date, portfolio_id, nav, ret, vol, dd, var95, es97)`
* `backtests(id, cfg_json, start, end, kpis_json, report_path)`

---

## 8) Parcours utilisateur (UX)

1. **Assistant d’objectif** : saisi capital, cible, échéance, profil risque → calcul de **faisabilité** (voir §9).
2. **Sélection univers d’actifs** & brokers autorisés.
3. **Simulation initiale** (1000–5000 trajectoires) → PoH, drawdown attendu, trajectoire cible.
4. **Actionables quotidiens** : liste claire, *checkbox* → envoi des ordres (si auto‑trade activé) ou export (CSV/IBKR/…)
5. **Historique & audit** : tout est traçable, diff « recommandé vs exécuté ».
6. **What‑if** : modifier contraintes et voir impact immédiat sur PoH/KPIs.

---

## 9) Calcul de faisabilité & exigences de rendement

Évalue la **croissance nécessaire** pour atteindre l’objectif :

* Facteur requis : $F = \frac{Cible}{Initial}$.
* **CAGR** requis (sur N années) : $(F)^{1/N} - 1$.
* **Rendement journalier** (sur D jours ouvrés ou calendaires) : $(F)^{1/D} - 1$.

> Exemple rapide (illustratif) : passer de **1 000 €** à **300 000 €** en **5 ans** (\~1826 jours calendaires) requiert un facteur **300×** :
>
> * CAGR ≈ $300^{1/5}-1 ≈ 3.72$ → **+372%/an**, irréaliste sans risques extrêmes.
> * Journalier ≈ (300^{1/1826}-1 ≈ 0.19%/jour\*\*, déjà très agressif avec constance improbable\*\*.
>
> Conclusion : le moteur doit **réviser le plan** (augmenter durée, apports périodiques, prendre plus de risque conscients, ou abaisser l’objectif) et mesurer la **PoH**.

Le logiciel formule **des plans alternatifs** :

* Étendre l’échéance, ou
* Ajouter des **apports réguliers** (DCA), ou
* Accepter un **taux de réussite** partiel (p.ex. 40–60%) avec contrôle de perte max, ou
* Branches « spéculatives » capées (satellite) + noyau défensif (core).

---

## 10) Gestion du risque & money management

* **Plafond de risque** journalier/hebdo (perte max, var95, ES97, stop global).
* **Volatilité cible** par portefeuille et *position sizing* \~ 1/vol.
* **Kelly limité** (ex. 0.25× Kelly) pour éviter l’overbetting.
* **Trailing stops** / **take profits** structurés (pyramiding/profit lock‑in).
* **Limiter levier** (par classe d’actifs), appels de marge simulés.
* **Blocage** des actifs illiquides lors d’événements (earnings, forks, news extrêmes).

---

## 11) Pipeline quotidien (08:00 Europe/Paris)

1. Ingestion mises à jour prix/fundamentaux → nettoyage/feature set.
2. Moteur stratégies → signaux + allocations cibles.
3. Simulation Monte‑Carlo & budget de risque → PoH actualisée.
4. Génération **Actionables** (avec raisons + estimation d’impact) → UI + notifications (email/Discord).
5. (Option) Exécution ordres → suivi + reconciliation.
6. Écriture des **metrics** & logs d’audit.

Intraday (optionnel) : réévaluation si seuils déclenchés (SL/TP, var breach, news shock).

---

## 12) API (extraits de routes)

* `POST /goals` — créer un objectif.
* `GET /goals/{id}/status` — état, PoH, trajectoire.
* `POST /allocations/target` — proposer une allocation sous contraintes.
* `GET /actions/today` — liste des actions du jour.
* `POST /actions/{id}/check` — marquer « done/ignored » + note.
* `POST /orders/preview` — impact + coûts attendus.
* `POST /backtests` — lancer un backtest (plage, univers, contraintes).

**Webhook brokers** : exécutions, rejets, fills partiels.

---

## 13) Stratégies incluses (MVP)

* **Core** :

  * ETF monde + obligations intermédiaires + or, allocation réévaluée mensuellement via risque parité/vol cible.
* **Satellite** :

  * **Trend/momentum** (12‑1, 3‑1) multi‑classes.
  * **Crypto trend** avec filtres de volatilité & funding.
  * **Mean‑reversion** faible intensité sur indices/FX (interdits si levier non autorisé).
* **Cash management** : migration automatique vers monétaire / T‑Bills synthétiques si régime de risque élevé.

Chaque stratégie expose : `signals()`, `target_weights()`, `explain()`, **tests unitaires**.

---

## 14) Backtesting & validation

* **Walk‑forward** (expanding/rolling window), coûts/frais réalistes, latence, slippage.
* **Stress tests** (2008, 2020, flash crashes, crypto winters).
* Rapports : CAGR, vol, Sharpe, Sortino, max DD, Calmar, hit‑ratio, time‑to‑recover, turnover.

---

## 15) Sécurité, conformité, éthique

* **KYC/AML** selon broker ; politique **« conseils généraux »** par défaut ;
* **Avertissements de risques** explicites ; pas de promesse de performance ;
* **RBAC**, OAuth2/OIDC (Google/GitHub), 2FA TOTP avec codes de secours, chiffrage secrets, journaux d’audit immuables ;
* Mode **paper‑trading** par défaut ; activation **opt‑in** d’auto‑exécution par objectif.

---

## 16) Stack technique (proposition)

* **Backend** : Python (FastAPI) + Pydantic ;
* **Ingestion/Workers** : Celery/Redis ou RQ + APScheduler ;
* **DB** : Postgres + Timescale ; **Cache** : Redis ; **Bus** : NATS/RabbitMQ ;
* **Frontend** : Next.js/React + Tailwind + shadcn/ui ;
* **Infra** : Docker Compose → Kubernetes (option) ; **Auth** : JWT + 2FA.

---

## 17) Exemple de pseudo‑code — planificateur quotidien

```python
# v0.1 — illustration
from datetime import date

def daily_plan(goal, portfolio, market_data):
    target = compute_target_allocation(goal, portfolio, market_data)
    sim = simulate_paths(portfolio, target, goal, n=5000)
    poh = probability_of_hitting_goal(sim, goal)
    actions = diff_to_actions(portfolio.current, target,
                              risk_budget=goal.risk_bounds,
                              costs=estimate_costs())
    return {
        "date": str(date.today()),
        "poh": poh,
        "actions": [explain_action(a) for a in actions],
        "impact": estimate_goal_impact(actions, sim)
    }
```

---

## 18) Exemple d’écran « Actions du jour »

* [ ] Réduire BTC de 2.5% → risque > budget (impact +0.7% PoH)
* [ ] Renforcer ETF Monde de 3% (impact +0.3% PoH)
* [ ] Placer 10% en monétaire (volatilité > seuil)
* [ ] Prendre profits sur ETH (+15% depuis entrée)

Chaque ligne → bouton « Justification » (signal, simulation, coûts).

---

## 19) Livrables MVP (contenu)

* Service `feasibility-calculator` (API + UI) : saisie objectif → PoH, CAGR requis, plans alternatifs.
* `strategy-engine` avec 1 core + 2 satellites + risk-engine (vol cible, SL/TP).
* `actions` UI avec checklist + export ordres (CSV/IBKR/…) ;
* Backtester de base + rapport HTML.

---

## 20) Notes finales

* Un objectif « 1 000 € → 300 000 € » demande **des horizons très longs** ou **des risques extrêmes** ; le système ne vend **aucune garantie**.
* Le but du logiciel est d’**augmenter la probabilité d’atteindre votre objectif** via une discipline, une gestion du risque rigoureuse et des décisions traçables.

---

### Annexe A — Formules utiles

* **CAGR**: `((target / initial) ** (1/years)) - 1`
* **Rendement journalier**: `((target / initial) ** (1/days)) - 1`
* **Position sizing \~ 1/vol**: `w_i ∝ 1/σ_i` (normalisé)
* **Kelly capé**: `f = cap * (μ/σ²)` avec `cap ∈ [0.1, 0.3]`

### Annexe B — Statuts d’action

* `pending` → `done` | `ignored` (avec commentaire obligatoire).
* Tout changement écrit en *audit log* (horodatage, user, IP, hash).
