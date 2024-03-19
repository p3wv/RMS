from jinja2 import Environment, FileSystemLoader
import os

template_dir = 'app/templates'  
env = Environment(loader=FileSystemLoader(template_dir))

def render_template(template_name, output_file, context=None):
    template = env.get_template(template_name)
    output = template.render(context or {})
    with open(output_file, 'w') as f:
        f.write(output)

templates_to_render = [
    {
        'template_name': 'base.html',
        'output_file': 'public/templates/base.html'
    },
    {
        'template_name': 'index.html',
        'output_file': 'public/templates/index.html'
    },

    {
        'template_name': '404.html',
        'output_file': 'public/templates/404.html'
    },
    {
        'template_name': '403.html',
        'output_file': 'public/templates/403.html'
    },
    {
        'template_name': '500.html',
        'output_file': 'public/templates/500.html'
    },
    {
        'template_name': 'cart.html',
        'output_file': 'public/templates/cart.html'
    },
    {
        'template_name': 'edit_profile.html',
        'output_file': 'public/templates/edit_profile.html'
    },
    {
        'template_name': 'menu.html',
        'output_file': 'public/templates/menu.html'
    },
    {
        'template_name': 'order_confirmation.html',
        'output_file': 'public/templates/order_confirmation.html'
    },
    {
        'template_name': 'ordered.html',
        'output_file': 'public/templates/ordered.html'
    },
    {
        'template_name': 'RMS_index.html',
        'output_file': 'public/templates/RMS_index.html'
    },
    {
        'template_name': 'user.html',
        'output_file': 'public/templates/user.html'
    }    
]

for template_info in templates_to_render:
    template_name = template_info['template_name']
    output_file = template_info['output_file']
    render_template(template_name, output_file)

print("Templates rendered successfully.")
