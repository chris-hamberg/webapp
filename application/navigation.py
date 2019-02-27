from application.mvc.model import Category, Subject

def navbar(active):
    ''' Dynamic navbar '''
    buttons = ('Home', 'About')
    return [{
        'name':name.title(), 'url':f'{name}'.lower(), 
        'active':name.lower() == active} for name in buttons
        ]

cms = {'subject':Subject.query(), 'category':Category.query()}
