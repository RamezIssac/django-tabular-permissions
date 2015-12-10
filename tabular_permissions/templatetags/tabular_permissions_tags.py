from django import template
from django.template.defaulttags import register


def get_permission_full_name(parser, token):
    tag_name, response, print_settings = token.split_contents()

    return GetPermissionFullName(response, print_settings)
    # return '%s_%s' % (perm,obj.__class__.__name__.lower())


class GetPermissionFullName(template.Node):
    def __init__(self, model, perm_name):
        super(GetPermissionFullName, self).__init__()
        self.model = template.Variable(model)
        self.perm_name = template.Variable(perm_name)

    def render(self, context):
        perm_name = self.perm_name.resolve(context)
        model = self.model.resolve(context)
        # pdb.set_trace()
        model_name = model['model'].__name__.lower()
        context['current_perm'] = '%s_%s' % (perm_name, model_name)
        return ''


register.tag('get_permission_full_name', get_permission_full_name)


@register.filter
def keyvalue(dict, key):
    if dict:
        if key in dict:
            return dict[key]

    return ''

    # def get_permission_id(parser, token):
    #     tag_name, perm_name = token.split_contents()
    #
    #     return GetPermissionFullName(perm_name, perm_dict)
    #
    #
    #
    # class GetPermissionID(template.Node):
    #
    #     def __init__(self, perm_name, perm_dict):
    #         super(GetPermissionID, self).__init__()
    #         self.perm_name = template.Variable(perm_name)
    #         self.perm_dict = template.Variable(perm_dict)
    #
    #     def render(self, context):
    #         perm_name = self.perm_name.resolve(context)
    #         perm_dict = self.perm_dict.resolve(context)
    #         # pdb.set_trace()
    #         model_name = model['model'].__name__.lower()
    #         context['current_perm'] = '%s_%s' % (perm_name, model_name)
    #         return ''
    #
    #
    # register.tag('get_permission_id', get_permission_id)
