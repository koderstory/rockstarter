# rockstart/commands.py
import shutil
import os
import sys
from string import Template


domain_name = sys.argv[2]
nginx_temp_pathfile = os.getcwd() + "/nginx_domain"

def copy_project_files():
    current_dir = os.path.dirname(__file__)
    template_dir = os.path.join(current_dir, 'src')
    target_dir = os.getcwd()

    try:
        if os.path.exists(template_dir):
            for item in os.listdir(template_dir):
                s = os.path.join(template_dir, item)
                d = os.path.join(target_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
            print('Project files copied successfully.')
        else:
            print(f"Template directory {template_dir} does not exist.")
    except Exception as e:
        print(f'Error: {e}')


def create_nginx_config(domain, nginx_fileconfig_path):
    # Template for the Nginx configuration
    config_template = Template("""
server {
    listen 80;
    server_name $domain;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn_$domain.sock;
    }
}
""")

    # Replace the placeholder with the actual domain
    config_content = config_template.substitute(domain=domain)

    # # Write the configuration to the specified output path
    with open(nginx_fileconfig_path, 'w') as config_file:
        config_file.write(config_content)

    # copy config file to nginx sites config
    os.system(f'sudo mv {nginx_fileconfig_path} /etc/nginx/sites-available/{domain}')

    print('setup nginx DONE')

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        copy_project_files()
    elif len(sys.argv) > 1 and sys.argv[1] == "deploy":
        try:
            create_nginx_config(domain_name, nginx_temp_pathfile)
        except IndexError:
            print("Usage: rockstarter deploy your-domain-name.com")
    else:
        print("Usage: rockstarter run")
# main()
