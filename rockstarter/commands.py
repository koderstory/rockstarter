# rockstart/commands.py
import shutil
import os
import sys
from string import Template

domain_name = ""
project_path = os.getcwd()
env_path = sys.prefix
nginx_temp_pathfile = os.getcwd() + "/nginx_domain"
service_temp_pathfile = os.getcwd() + "/gunicorn_domain.service"
socket_temp_pathfile = os.getcwd() + "/gunicorn_domain.socket"

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

def create_socket_config():
    # Template for the Nginx configuration
    config_template = Template("""[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn_$domain.sock

[Install]
WantedBy=sockets.target
""")

    # Replace the placeholder with the actual domain
    config_content = config_template.substitute(domain=domain_name)

    # # Write the configuration to the specified output path
    with open(socket_temp_pathfile, 'w') as config_file:
        config_file.write(config_content)

    # copy config file to systemd socket config
    os.system(f'sudo mv {socket_temp_pathfile} /etc/systemd/system/gunicorn_{domain_name}.socket')
    print('setup socket DONE')


def create_service_config():
    # Template for the Nginx configuration
    config_template = Template("""[Unit]
Description=gunicorn daemon
Requires=gunicorn_$domain.socket
After=network.target

[Service]
User=dev
Group=www-data
WorkingDirectory=$project_path
ExecStart=$env_path/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn_$domain.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
""")

    # Replace the placeholder with the actual domain
    config_content = config_template.substitute(domain=domain_name,project_path=project_path,env_path=env_path)

    # # Write the configuration to the specified output path
    with open(service_temp_pathfile, 'w') as config_file:
        config_file.write(config_content)

    # copy config file to systemd socket config
    os.system(f'sudo mv {service_temp_pathfile} /etc/systemd/system/gunicorn_{domain_name}.service')
    os.system(f'sudo systemctl start gunicorn_{domain_name}')
    os.system(f'sudo systemctl enable gunicorn_{domain_name}')
    os.system(f'sudo systemctl enable gunicorn_{domain_name}.socket')
    print('setup service DONE')




def create_nginx_config():
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
    config_content = config_template.substitute(domain=domain_name)

    # # Write the configuration to the specified output path
    with open(nginx_temp_pathfile, 'w') as config_file:
        config_file.write(config_content)

    # copy config file to nginx sites config
    os.system(f'sudo mv {nginx_temp_pathfile} /etc/nginx/sites-available/{domain_name}')
    
    os.system(f'sudo ln -s /etc/nginx/sites-available/{domain_name} /etc/nginx/sites-enabled')
    os.system(f'sudo systemctl restart nginx')
    print('setup nginx DONE')

def remove_service_and_nginx():
    """
    This method removes a systemd service, its socket, and associated NGINX configuration.
    
    :param service_name: The name of the systemd service (without .service extension) and associated NGINX site
    """
    try:
        # Stop and disable the systemd service and socket
        os.system(f"sudo systemctl stop gunicorn_{domain_name}.service")
        os.system(f"sudo systemctl disable gunicorn_{domain_name}.service")
        os.system(f"sudo systemctl stop gunicorn_{domain_name}.socket")
        os.system(f"sudo systemctl disable gunicorn_{domain_name}.socket")
        
        # Remove the service and socket files
        os.system(f"sudo rm /etc/systemd/system/gunicorn_{domain_name}.service")
        os.system(f"sudo rm /etc/systemd/system/gunicorn_{domain_name}.socket")
        
        # Reload the systemd daemon
        os.system("sudo systemctl daemon-reload")
        os.system("sudo systemctl reset-failed")
        
        # Remove the NGINX configuration
        os.system(f"sudo rm /etc/nginx/sites-available/{domain_name}")
        os.system(f"sudo rm /etc/nginx/sites-enabled/{domain_name}")
        
        # Test and reload NGINX to apply the changes
        os.system("sudo nginx -t && sudo systemctl reload nginx")
        
        print(f"Service, socket, and NGINX configuration for {domain_name} have been removed successfully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    global domain_name
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        copy_project_files()
    elif len(sys.argv) > 1 and sys.argv[1] == "drop":
        try:
            domain_name = sys.argv[2]
            remove_service_and_nginx()
        except IndexError:
            print("Usage: rockstarter drop your-domain-name.com")
    elif len(sys.argv) > 1 and sys.argv[1] == "deploy":
        try:
            domain_name = sys.argv[2]
            create_socket_config()
            create_service_config()
            create_nginx_config()
        except IndexError:
            print("Usage: rockstarter deploy your-domain-name.com")
    else:
        print("Usage: rockstarter run")


# just for testing
#main()
