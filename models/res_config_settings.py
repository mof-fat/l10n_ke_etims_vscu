# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    l10n_ke_server_mode = fields.Selection(
        string="eTIMS Server Mode",
        related='company_id.l10n_ke_server_mode',
        readonly=False,
    )
    l10n_ke_oscu_serial_number = fields.Char(
        related='company_id.l10n_ke_oscu_serial_number',
        readonly=False,
        string='Serial Number',
    )
    l10n_ke_api_url = fields.Char(
        related='company_id.l10n_ke_api_url',
        readonly=False,
    )
    l10n_ke_control_unit = fields.Char(
        related='company_id.l10n_ke_control_unit',
        readonly=False,
        string="Control Unit ID",
    )
    l10n_ke_oscu_cmc_key = fields.Char(
        related='company_id.l10n_ke_oscu_cmc_key',
        readonly=False,
        string="CMC Key",
    )
    l10n_ke_oscu_user_help = fields.Boolean(
        related='company_id.l10n_ke_oscu_user_help',
        readonly=False,
        string="Show Help",
    )
    l10n_ke_oscu_user_agreement_is_readonly = fields.Boolean(
        compute='_compute_l10n_ke_oscu_user_agreement_is_readonly',
    )
    l10n_ke_oscu_user_agreement = fields.Boolean(
        related='company_id.l10n_ke_oscu_user_agreement',
        readonly=False,
    )
    l10n_ke_insurance_code = fields.Char(
        related='company_id.l10n_ke_insurance_code',
        readonly=False,
    )
    l10n_ke_insurance_name = fields.Char(
        related='company_id.l10n_ke_insurance_name',
        readonly=False,
    )
    l10n_ke_insurance_rate = fields.Float(
        related='company_id.l10n_ke_insurance_rate',
        readonly=False,
    )
    #TODO remove issue with Pandya
    cash_discount=fields.Float(string="Cash Discount",readonly=False)
    cheque_signatories_ids=fields.Float(string="Cash Discount",readonly=False)

    @api.depends('company_id')
    def _compute_l10n_ke_oscu_user_agreement_is_readonly(self):
        for record in self:
            record.l10n_ke_oscu_user_agreement_is_readonly = record.company_id.l10n_ke_oscu_user_agreement and record.company_id.l10n_ke_oscu_cmc_key

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if (
                vals.get('l10n_ke_server_mode') in ('prod', 'test')
                and vals.get('l10n_ke_oscu_cmc_key')
                and not (vals.get('l10n_ke_oscu_user_agreement') or self.env['res.company'].browse(vals.get('company_id')).l10n_ke_oscu_user_agreement)
            ):
                raise UserError(_("To use VSCU functionality in Odoo, please agree to the terms of use of Odoo as an VSCU service provider."))
        return super().create(vals_list)

    def action_l10n_ke_oscu_initialize(self):
        return self.company_id.action_l10n_ke_oscu_initialize()

    def action_l10n_ke_send_insurance(self):
        return self.company_id.action_l10n_ke_send_insurance()
