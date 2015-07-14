'''
This file will contain all the custom template tags for the
MUO app.
'''

from django.contrib.admin.templatetags.admin_modify import *
from base.templatetags.admin_modify import submit_row as original_submit_row
from django import template


register = template.Library()


@register.inclusion_tag('admin/report/report_submit_line.html', takes_context=True)
def report_submit_row(context):
    ctx = original_submit_row(context)

    model_object = ctx.get('original')  # For add form model_object will be None
    user_object = context.get('user')

    # Get the default status of the buttons
    show_save_and_continue = ctx.get('show_save_and_continue')
    show_save_as_new = ctx.get('show_save_as_new')
    show_save = ctx.get('show_save')
    show_delete_link = ctx.get('show_delete_link')

    ctx.update({
        # Do not show save and add another button
        'show_save_and_add_another': False,

        # Always show save and delete buttons on the add form if the default status of the buttons say so
        # Show save and delete buttons on the change form only if the muo is created by the current user
        # and it is in 'draft' state and the default status is also True
        'show_save_and_continue': show_save_and_continue and
                                  (model_object is None or
                                  (model_object and
                                  model_object.status == 'draft' and
                                  (user_object == model_object.created_by or user_object.has_perm('report.can_edit_all')))),
        'show_save': show_save and
                     (model_object is None or
                     (model_object and
                     model_object.status == 'draft' and
                     (user_object == model_object.created_by or user_object.has_perm('report.can_edit_all')))),


        # Show submit for review button only to the creator of the report  and if its in draft state
        'show_submit_for_review': model_object and
                                  model_object.status == 'draft' and
                                  (user_object == model_object.created_by or user_object.has_perm('report.can_edit_all')),

        # Show edit button only to the creator of the report and if its either in in_review or rejected state
        'show_edit': model_object and
                     model_object.status in ('in_review', 'rejected') and
                     (user_object == model_object.created_by or user_object.has_perm('report.can_edit_all')),

        # Show approve button only to the user if he/she has the can_approve permission and the state of
        # report is in in_review
        'show_approve': model_object and
                        model_object.status == 'in_review' and
                        user_object.has_perm('report.can_approve'),

        # Show reject button only to the user if he/she has the can_reject permission and the state of the
        # report is in in_review or approved state
        'show_reject': model_object and
                       model_object.status in ('in_review', 'approved') and
                       user_object.has_perm('report.can_reject'),

        'show_delete_link': show_delete_link and
                            (model_object is None or
                            (model_object and
                            model_object.status in ('draft', 'rejected') and
                            (user_object == model_object.created_by or user_object.has_perm('report.can_edit_all')))),


    })

    return ctx
