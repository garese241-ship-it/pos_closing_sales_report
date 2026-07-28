# POS Closing Sales Report

Module Odoo qui envoie automatiquement un email récapitulatif à chaque
clôture d'une session de Point de Vente (POS).

## Fonctionnalités

- **Déclenchement automatique** : détecte le passage d'une session POS à
  l'état "clôturée", quel que soit le chemin utilisé (interface caisse ou
  back-office).
- **Ventes POS** : total des commandes de la session clôturée.
- **Ventes normales** : total des factures clients (hors POS) émises le
  même jour, en excluant automatiquement les factures déjà comptées côté POS.
- **Total global** : somme des deux.
- **Contexte complet dans l'email** : société, point de vente, date et heure
  de clôture (dans le fuseau horaire de l'entreprise).
- **Pièce jointe PDF** : le rapport standard "Ventes du jour" d'Odoo est
  automatiquement joint à l'email.
- **Destinataire configurable** : menu dédié *Rapport de clôture caisse >
  Paramètres*, sans toucher aux paramètres généraux d'Odoo.

## Compatibilité

| Série Odoo | Branche | Statut |
|---|---|---|
| 17.0 | `17.0` | Testé en production |
| 18.0 | `18.0` | Beta — à valider avant mise en production |

## Installation

1. Copier le dossier du module dans votre répertoire d'addons custom.
2. Redémarrer le service Odoo.
3. Activer le mode développeur, aller dans **Apps**, retirer le filtre
   "Apps", rechercher `pos_closing_sales_report`, installer.
4. Configurer le destinataire dans **Rapport de clôture caisse > Paramètres**.
5. Configurer un serveur de messagerie sortant si ce n'est pas déjà fait
   (**Réglages > Technique > Email > Serveurs de messagerie sortants**).

## Licence

LGPL-3. Voir https://www.gnu.org/licenses/lgpl-3.0.html

## Auteur

GARESE — https://www.garese.net

## Support

Ce module est fourni gratuitement, sans garantie de support. Les
suggestions et rapports de bug sont les bienvenus via les issues GitHub.
