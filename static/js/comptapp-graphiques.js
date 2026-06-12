/* ============================================================
   ComptApp Platform — Graphiques
   Helpers Chart.js alignés sur le design system (couleurs, polices).
   Chaque page expose ses données via une balise {{ ...|json_script }}
   puis appelle la fonction de création correspondante.
   ============================================================ */

const GRAPHIQUE_COULEURS = {
  recette: '#277f65',
  recetteFond: 'rgba(22, 219, 204, 0.22)',
  depense: '#fc7900',
  depenseFond: 'rgba(252, 121, 0, 0.14)',
  solde: '#1814f3',
  soldeFond: 'rgba(24, 20, 243, 0.12)',
  rouge: '#fe5c73',
  texte: '#718ebf',
  grille: '#eef1f6',
  palette: ['#1814f3', '#16dbcc', '#fc7900', '#fa00ff', '#fe5c73', '#41d4a8', '#343c6a', '#718ebf'],
};

if (window.Chart) {
  Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
  Chart.defaults.font.size = 12;
  Chart.defaults.color = GRAPHIQUE_COULEURS.texte;
  Chart.defaults.plugins.legend.labels.usePointStyle = true;
  Chart.defaults.plugins.legend.labels.boxWidth = 8;
  Chart.defaults.plugins.legend.labels.boxHeight = 8;
  Chart.defaults.plugins.legend.labels.padding = 16;
}

/* Lit les données injectées par le filtre Django |json_script. */
function lireDonneesGraphique(id) {
  return JSON.parse(document.getElementById(id).textContent);
}

/*
 * Initialise un graphique en isolant les erreurs : si l'un échoue
 * (fonction absente, données manquantes…), les autres se dessinent quand même.
 * `fn` est la fonction de création, `idCanvas` le <canvas>, `idDonnees` la balise json_script.
 */
function initGraphique(fn, idCanvas, idDonnees) {
  try {
    if (typeof window.Chart === 'undefined') {
      throw new Error('Chart.js non chargé');
    }
    if (typeof fn !== 'function') {
      throw new Error('fonction de graphique introuvable (cache JS obsolète ?)');
    }
    if (!document.getElementById(idCanvas)) {
      return; // canvas absent (état vide) : rien à dessiner
    }
    fn(idCanvas, lireDonneesGraphique(idDonnees));
  } catch (e) {
    console.error('[ComptApp] Graphique "' + idCanvas + '" non affiché :', e);
  }
}

function formaterFCFA(valeur) {
  return new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 0 }).format(valeur) + ' FCFA';
}

/* Format court pour les axes : 1,2 M, 350 k... */
function formaterCompact(valeur) {
  return new Intl.NumberFormat('fr-FR', { notation: 'compact', maximumFractionDigits: 1 }).format(valeur);
}

/* Dégradé vertical utilisé sous les courbes (effet "area"). */
function _degradeVertical(canvas, couleurHaut) {
  const ctx = canvas.getContext('2d');
  const gradient = ctx.createLinearGradient(0, 0, 0, canvas.parentNode.clientHeight || 300);
  gradient.addColorStop(0, couleurHaut);
  gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
  return gradient;
}

function _axesMonetaires() {
  return {
    x: { grid: { display: false }, border: { display: false } },
    y: {
      beginAtZero: true,
      border: { display: false },
      grid: { color: GRAPHIQUE_COULEURS.grille },
      ticks: { callback: (v) => formaterCompact(v), maxTicksLimit: 6 },
    },
  };
}

function _infobulle() {
  return {
    backgroundColor: '#343c6a',
    padding: 12,
    cornerRadius: 10,
    displayColors: false,
    titleFont: { family: "'Sora', sans-serif", weight: '700' },
    callbacks: {
      label: (ctx) => {
        const valeur = (ctx.parsed && typeof ctx.parsed === 'object') ? ctx.parsed.y : ctx.parsed;
        const prefixe = ctx.dataset.label ? ctx.dataset.label + ' : ' : '';
        return ' ' + prefixe + formaterFCFA(valeur);
      },
    },
  };
}

/* Courbe double : évolution mensuelle des recettes et des dépenses. */
function creerCourbeEvolution(idCanvas, donnees) {
  const canvas = document.getElementById(idCanvas);
  new Chart(canvas, {
    type: 'line',
    data: {
      labels: donnees.labels,
      datasets: [
        {
          label: 'Recettes',
          data: donnees.recettes,
          borderColor: GRAPHIQUE_COULEURS.recette,
          backgroundColor: _degradeVertical(canvas, GRAPHIQUE_COULEURS.recetteFond),
          fill: true,
          tension: 0.4,
          borderWidth: 3,
          pointRadius: 4,
          pointBackgroundColor: '#ffffff',
          pointBorderColor: GRAPHIQUE_COULEURS.recette,
          pointBorderWidth: 2,
        },
        {
          label: 'Dépenses',
          data: donnees.depenses,
          borderColor: GRAPHIQUE_COULEURS.depense,
          backgroundColor: _degradeVertical(canvas, GRAPHIQUE_COULEURS.depenseFond),
          fill: true,
          tension: 0.4,
          borderWidth: 3,
          pointRadius: 4,
          pointBackgroundColor: '#ffffff',
          pointBorderColor: GRAPHIQUE_COULEURS.depense,
          pointBorderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: { legend: { display: false }, tooltip: _infobulle() },
      scales: _axesMonetaires(),
    },
  });
}

/* Anneau de répartition par catégorie, avec pourcentages dans l'infobulle. */
function creerAnneau(idCanvas, donnees) {
  const infobulle = _infobulle();
  infobulle.displayColors = true;
  infobulle.callbacks.label = (ctx) => {
    const total = ctx.dataset.data.reduce((somme, v) => somme + v, 0);
    const pourcentage = total ? Math.round((ctx.parsed / total) * 100) : 0;
    return ' ' + ctx.label + ' : ' + formaterFCFA(ctx.parsed) + ' (' + pourcentage + ' %)';
  };
  new Chart(document.getElementById(idCanvas), {
    type: 'doughnut',
    data: {
      labels: donnees.labels,
      datasets: [{
        data: donnees.valeurs,
        backgroundColor: GRAPHIQUE_COULEURS.palette,
        borderColor: '#ffffff',
        borderWidth: 3,
        hoverOffset: 8,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '68%',
      plugins: {
        legend: { position: 'bottom' },
        tooltip: infobulle,
      },
    },
  });
}

/* Barres comparatives du bilan : recettes / dépenses / solde. */
function creerBarresBilan(idCanvas, donnees) {
  const couleurSolde = donnees.solde >= 0 ? GRAPHIQUE_COULEURS.solde : GRAPHIQUE_COULEURS.rouge;
  new Chart(document.getElementById(idCanvas), {
    type: 'bar',
    data: {
      labels: ['Recettes', 'Dépenses', 'Solde'],
      datasets: [{
        data: [donnees.recettes, donnees.depenses, donnees.solde],
        backgroundColor: [GRAPHIQUE_COULEURS.recette, GRAPHIQUE_COULEURS.depense, couleurSolde],
        borderRadius: 12,
        maxBarThickness: 70,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: _infobulle() },
      scales: _axesMonetaires(),
    },
  });
}

/* Barres groupées recettes / dépenses par mois (fiche partenaire). */
function creerBarresGroupees(idCanvas, donnees) {
  new Chart(document.getElementById(idCanvas), {
    type: 'bar',
    data: {
      labels: donnees.labels,
      datasets: [
        {
          label: 'Recettes',
          data: donnees.recettes,
          backgroundColor: GRAPHIQUE_COULEURS.recette,
          borderRadius: 8,
          maxBarThickness: 36,
        },
        {
          label: 'Dépenses',
          data: donnees.depenses,
          backgroundColor: GRAPHIQUE_COULEURS.depense,
          borderRadius: 8,
          maxBarThickness: 36,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'bottom' }, tooltip: _infobulle() },
      scales: _axesMonetaires(),
    },
  });
}

/* Barres verticales du solde net mensuel : vert si positif, rouge si négatif. */
function creerBarresSoldeMensuel(idCanvas, donnees) {
  const couleurs = donnees.valeurs.map(
    (v) => (v >= 0 ? GRAPHIQUE_COULEURS.recette : GRAPHIQUE_COULEURS.rouge)
  );
  new Chart(document.getElementById(idCanvas), {
    type: 'bar',
    data: {
      labels: donnees.labels,
      datasets: [{
        data: donnees.valeurs,
        backgroundColor: couleurs,
        borderRadius: 10,
        maxBarThickness: 48,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: _infobulle() },
      scales: (function () { const a = _axesMonetaires(); a.y.beginAtZero = true; return a; })(),
    },
  });
}

/* Courbe du solde de trésorerie cumulé (journal des opérations). */
function creerCourbeSolde(idCanvas, donnees) {
  const canvas = document.getElementById(idCanvas);
  const axes = _axesMonetaires();
  axes.y.beginAtZero = false;
  new Chart(canvas, {
    type: 'line',
    data: {
      labels: donnees.labels,
      datasets: [{
        label: 'Solde cumulé',
        data: donnees.valeurs,
        borderColor: GRAPHIQUE_COULEURS.solde,
        backgroundColor: _degradeVertical(canvas, GRAPHIQUE_COULEURS.soldeFond),
        fill: true,
        tension: 0.3,
        borderWidth: 3,
        pointRadius: 0,
        pointHitRadius: 14,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: { legend: { display: false }, tooltip: _infobulle() },
      scales: axes,
    },
  });
}
