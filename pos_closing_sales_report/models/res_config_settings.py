# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_closing_report_user_id = fields.Many2one(
        'res.users',
        string="Destinataire du rapport de clôture",
        config_parameter='pos_closing_sales_report.recipient_user_id',
        help="Utilisateur qui recevra l'email récapitulatif (ventes POS + ventes "
             "normales) à chaque clôture d'une session de caisse. "
             "Aucun email n'est envoyé si ce champ est vide.",
    )
