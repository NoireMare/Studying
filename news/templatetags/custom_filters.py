from django import template

register = template.Library()

censor_list = ["Урод", "урод", "хрен", "Хрен", "Дурачок", "дурачок", "Дебилы", "блин"]


@register.filter()
def censor(value):
    value = value.split()
    for i in range(len(value)):
        if isinstance(value[i], str) and value[i] in censor_list:
            value[i] = value[i][0] + "*"*(len(value[i])-1)
    return f'{" ".join(value)}'

