# -*- coding: utf-8 -*-
{
    'name': "POS Closing Sales Report",
    'version': '18.0.1.0.0',
    'category': 'Point of Sale',
    'summary': "Email automatique à la clôture d'une session POS : ventes caisse "
               "+ ventes normales + pièce jointe PDF",
    'description': """
POS Closing Sales Report (v18 — build non testée en production)
=================================================================

Cette version cible Odoo 18.0. Le code est identique à la version 17.0
(aucune API utilisée par ce module n'a changé entre les deux séries selon
la documentation officielle), mais elle n'a pas encore été validée sur une
instance Odoo 18 réelle. Testez en environnement de recette avant mise en
production.

POS Closing Sales Report
=========================

À chaque clôture d'une session de Point de Vente, ce module envoie
automatiquement un email récapitulatif contenant :

- Le total des ventes réalisées en caisse (POS) sur la session clôturée.
- Le total des ventes normales : les factures clients (hors POS) émises
  le même jour, validées (postées).
- Le total global (POS + normal).
- La société, le point de vente, et la date/heure de clôture.
- Le rapport PDF "Ventes du jour" en pièce jointe.

Configuration
-------------
Le destinataire de l'email se configure depuis le menu dédié :
**Rapport de clôture caisse > Paramètres** (visible par les managers POS).

Aucune configuration technique supplémentaire n'est nécessaire : le module
détecte automatiquement chaque clôture de session, quel que soit le chemin
utilisé pour clôturer (interface caisse ou back-office).
""",
    'author': 'GARESE',
    'website': 'https://www.garese.net',
    'license': 'LGPL-3',
    'depends': ['point_of_sale', 'account', 'mail'],
    'data': [
        'data/mail_template.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
