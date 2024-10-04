import os
import jinja2
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Generate a config file from environment variables.")
    # Option to specify the .env file path
    parser.add_argument('-e', '--env-file', type=str, help="Path to the .env file")
    return parser.parse_args()

def load_env_file(filepath):
    with open(filepath) as f:
        for line in f:
            # Ignore comments and blank lines
            if line.startswith('#') or not line.strip():
                continue
            # Split the line into key and value
            key, value = line.strip().split('=', 1)

            # Set the environment variable
            os.environ[key] = value


def render_config(template, data):
    # Create a Jinja2 template from the string
    template = jinja2.Template(template)
    return template.render(data)

def generate_config_file():
    args = parse_args()
    load_env_file(args.env_file)
    config_template_path = os.environ.get("CONFIG_TEMPLATE_PATH")
    template = ""
    with open(config_template_path, 'r', encoding='utf-8') as f:
        template = f.read()
        f.close()
    rendered_config = render_config(template, os.environ)
    # Write the rendered config to a file
    output_path = os.environ.get("OUTPUT_CONFIG_PATH")
    with open(output_path, 'w', encoding='utf-8') as config_file:
        config_file.write(rendered_config)
        config_file.close()
    print(f"Config file generated: {output_path}")

# Main execution
if __name__ == '__main__':
    generate_config_file()
