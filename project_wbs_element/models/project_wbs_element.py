# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models, api


class ProjectWbsElement(models.Model):
    _name = "project.wbs_element"
    _description = "Project WBS Element"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    code = fields.Char(string='Code')
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
        required=True,
        copy=True
    )
    task_ids = fields.One2many(
        comodel_name='project.task',
        inverse_name='wbs_element_id',
        string='Tasks',
        copy=True
    )
    nbr_tasks = fields.Integer(string='Number of Tasks',
                               compute='_count_tasks')
    color = fields.Integer(string='Color Index')

    @api.depends('task_ids')
    def _count_tasks(self):
        for record in self:
            record.nbr_tasks = len(self.task_ids)

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.code:
                name = '[' + record.code + '] ' + name
            res.append((record.id, name))
        return res
