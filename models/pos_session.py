# -*- coding: utf-8 -*-
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)

DATETIME_DISPLAY_FORMAT = '%d/%m/%Y à %H:%M'


class PosSession(models.Model):
    _inherit = 'pos.session'

    x_pos_sales_total = fields.Monetary(
        string="Total ventes POS",
        currency_field='currency_id',
        readonly=True,
        copy=False,
        help="Total des ventes réalisées en caisse (POS) pour cette session, "
             "figé au moment de la clôture.",
    )
    x_normal_sales_total = fields.Monetary(
        string="Total ventes normales (factures)",
        currency_field='currency_id',
        readonly=True,
        copy=False,
        help="Total des factures clients (hors POS) émises le jour de la clôture "
             "de cette session, figé au moment de la clôture.",
    )
    x_grand_total = fields.Monetary(
        string="Total global",
        currency_field='currency_id',
        readonly=True,
        copy=False,
    )
    x_closing_datetime_display = fields.Char(
        string="Date et heure de clôture (affichage)",
        readonly=True,
        copy=False,
        help="Date et heure de clôture formatées dans le fuseau horaire de "
             "l'entreprise, figées au moment de l'envoi du rapport.",
    )

    def write(self, vals):
        # On repère AVANT le super().write() les sessions qui vont passer à
        # l'état 'closed', afin de pouvoir déclencher l'envoi du mail juste après.
        sessions_closing = self.env['pos.session']
        if vals.get('state') == 'closed':
            sessions_closing = self.filtered(lambda s: s.state != 'closed')

        result = super().write(vals)

        for session in sessions_closing:
            try:
                session._send_closing_sales_report()
            except Exception:
                _logger.exception(
                    "Echec de l'envoi du rapport de clôture de caisse pour la "
                    "session POS %s (id=%s)", session.name, session.id,
                )

        return result

    def _get_pos_sales_total(self):
        self.ensure_one()
        valid_orders = self.order_ids.filtered(
            lambda o: o.state in ('paid', 'done', 'invoiced')
        )
        return sum(valid_orders.mapped('amount_total'))

    def _get_normal_sales_total(self, close_date):
        """Total des factures clients (hors POS) émises le jour de clôture."""
        self.ensure_one()
        domain = [
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('invoice_date', '=', close_date),
            ('company_id', '=', self.company_id.id),
        ]
        invoices = self.env['account.move'].search(domain)
        if not invoices:
            return 0.0

        # On exclut les factures générées depuis une commande POS pour ne pas
        # les compter à la fois dans "ventes POS" et "ventes normales".
        pos_linked_invoice_ids = self.env['pos.order'].search([
            ('account_move', 'in', invoices.ids),
        ]).mapped('account_move').ids
        invoices = invoices.filtered(lambda inv: inv.id not in pos_linked_invoice_ids)

        return sum(invoices.mapped('amount_total'))

    def _compute_sales_totals(self):
        self.ensure_one()
        close_date = (self.stop_at or fields.Datetime.now()).date()
        pos_total = self._get_pos_sales_total()
        normal_total = self._get_normal_sales_total(close_date)
        return pos_total, normal_total

    def _get_closing_datetime_display(self):
        """Formate stop_at (stocké en UTC) dans le fuseau horaire de l'entreprise."""
        self.ensure_one()
        close_dt_utc = self.stop_at or fields.Datetime.now()
        tz_name = self.company_id.partner_id.tz or 'UTC'
        close_dt_local = fields.Datetime.context_timestamp(
            self.with_context(tz=tz_name), close_dt_utc
        )
        return close_dt_local.strftime(DATETIME_DISPLAY_FORMAT)

    def _send_closing_sales_report(self):
        self.ensure_one()

        pos_total, normal_total = self._compute_sales_totals()
        grand_total = pos_total + normal_total
        closing_datetime_display = self._get_closing_datetime_display()

        # On fige les totaux et la date d'affichage sur la session (utile pour
        # l'historique et pour le template d'email).
        super(PosSession, self).write({
            'x_pos_sales_total': pos_total,
            'x_normal_sales_total': normal_total,
            'x_grand_total': grand_total,
            'x_closing_datetime_display': closing_datetime_display,
        })

        icp = self.env['ir.config_parameter'].sudo()
        recipient_user_id = icp.get_param('pos_closing_sales_report.recipient_user_id')
        if not recipient_user_id:
            _logger.warning(
                "Rapport de clôture POS : aucun destinataire configuré "
                "(Point de Vente > Configuration > Paramètres)."
            )
            return

        recipient_user = self.env['res.users'].sudo().browse(int(recipient_user_id))
        if not recipient_user.exists() or not recipient_user.email:
            _logger.warning(
                "Rapport de clôture POS : le destinataire configuré (id=%s) "
                "n'existe pas ou n'a pas d'adresse email valide.", recipient_user_id,
            )
            return

        template = self.env.ref(
            'pos_closing_sales_report.mail_template_pos_closing_sales',
            raise_if_not_found=False,
        )
        if not template:
            _logger.error(
                "Rapport de clôture POS : le template d'email est introuvable "
                "(pos_closing_sales_report.mail_template_pos_closing_sales)."
            )
            return

        template.sudo().send_mail(
            self.id,
            force_send=True,
            email_values={'email_to': recipient_user.email},
        )
