# -*- coding: utf-8 -*-
{
    'name': "POS Closing Sales Report Mail",
    'version': '17.0.1.1.0',
    'category': 'Point of Sale',
    'summary': "Envoi automatique d'un email récapitulatif des ventes (POS + normales) à la clôture d'une session de caisse",
    'description': """
POS Closing Sales Report Mail
==============================

À chaque clôture d'une session de Point de Vente, ce module envoie automatiquement
un email récapitulatif contenant :

- Le total des ventes réalisées en caisse (POS) sur la session clôturée.
- Le total des ventes normales : les factures clients (hors POS) émises le
  même jour, validées (postées).
- Le total global (POS + normal).

Configuration
-------------
Le destinataire de l'email se configure dans :
Point de Vente > Configuration > Paramètres > Rapport de clôture de caisse.

Auteur : GARESE - Giovanni
""",
    'author': 'GARESE',
    'depends': ['point_of_sale', 'account', 'mail'],
    'data': [
        'data/mail_template.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
