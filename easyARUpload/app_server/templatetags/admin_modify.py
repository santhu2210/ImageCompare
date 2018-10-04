
from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row
# or 
# original_submit_row = submit_row

@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    ctx = original_submit_row(context)
    # print "ctx--->", ctx
    ctx.update({
        'show_save_and_add_another': False ,#context.get('show_save_and_add_another', ctx['show_save_and_add_another']),
        'show_save_and_continue': False
        })                                                                  
    return ctx