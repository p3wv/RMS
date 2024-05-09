# from jinja2 import Environment, FileSystemLoader

# template_dir = 'app/templates'  
# env = Environment(loader=FileSystemLoader(template_dir))

# def render_template(template_name, output_file, context=None):
#     template = env.get_template(template_name)
#     output = template.render(context or {})
#     with open(output_file, 'w') as f:
#         f.write(output)

# templates_to_render = [
#     {
#         'template_name': 'base.html',
#         'output_file': 'app/templates/base.html'
#     },
#     {
#         'template_name': 'index.html',
#         'output_file': 'app/templates/index.html'
#     },

#     {
#         'template_name': '404.html',
#         'output_file': 'app/templates/404.html'
#     },
#     {
#         'template_name': '403.html',
#         'output_file': 'app/templates/403.html'
#     },
#     {
#         'template_name': '500.html',
#         'output_file': 'app/templates/500.html'
#     },
#     {
#         'template_name': 'cart.html',
#         'output_file': 'app/templates/cart.html'
#     },
#     {
#         'template_name': 'edit_profile.html',
#         'output_file': 'app/templates/edit_profile.html'
#     },
#     {
#         'template_name': 'menu.html',
#         'output_file': 'app/templates/menu.html'
#     },
#     {
#         'template_name': 'order_confirmation.html',
#         'output_file': 'app/templates/order_confirmation.html'
#     },
#     {
#         'template_name': 'ordered.html',
#         'output_file': 'app/templates/ordered.html'
#     },
#     {
#         'template_name': 'RMS_index.html',
#         'output_file': 'app/templates/RMS_index.html'
#     },
#     {
#         'template_name': 'user.html',
#         'output_file': 'app/templates/user.html'
#     },
#     {
#         'template_name': 'previous_orders.html',
#         'output_file': 'app/templates/previous_orders.html'
#     },
#     {
#         'template_name': 'change_email.html',
#         'output_file': 'app/templates/auth/change_email.html'
#     },
#     {
#         'template_name': 'change_password.html',
#         'output_file': 'app/templates/auth/change_password.html'
#     },
#     {
#         'template_name': 'login.html',
#         'output_file': 'app/templates/auth/login.html'
#     },
#     {
#         'template_name': 'register.html',
#         'output_file': 'app/templates/auth/register.html'
#     },
#     {
#         'template_name': 'reset_password.html',
#         'output_file': 'app/templates/auth/reset_password.html'
#     },
#     {
#         'template_name': 'bootstrap4/form.html',
#         'output_file': 'app/templates/bootstrap4/form.html'
#     }
# ]

# for template_info in templates_to_render:
#     template_name = template_info['template_name']
#     output_file = template_info['output_file']
#     render_template(template_name, output_file)

# print("Templates rendered successfully.")
