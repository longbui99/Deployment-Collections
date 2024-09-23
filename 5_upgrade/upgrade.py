import os
import sys
import argparse
import yaml



if __name__ == "__main__":
    parser = argparse.ArgumentParser("Upgrade Parser")
    parser.add_argument("-f", "--upgrade_file", help="An integer will be increased by 1 and printed.", type=str, required=True)
    parser.add_argument("-d", "--db_list", help="Database List", type=str, required=True)
    parser.add_argument("-c", "--config_path", help="Config Path", type=str, required=True)
    parser.add_argument("-e", "--execution_path", help="Odoo Bin Execution File", type=str, required=True)
    args = parser.parse_args()
    yaml_data = {}
    if os.path.exists("./upgrade.sh"):
        os.remove("./upgrade.sh")
    with open(args.upgrade_file, 'r') as f:
        try:
            yaml_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)
        f.close()

    def format_command(database):
        command = f"{args.execution_path} -c {args.config_path}"
        if 'upgrade_modules' in yaml_data:
            command += f" -u {','.join(yaml_data['upgrade_modules'])}"
        if 'install_modules' in yaml_data:
            command += f" -i {','.join(yaml_data['install_modules'])}"
        command += f" -d {database};"
        return command

    final_commands = []
    if isinstance(args.db_list, str):
        dblist = args.db_list.split(",")
    else:
        dblist = False
    if yaml_data['databases'] and dblist:
        dblist = [db for db in yaml_data['databases'] if db in dblist]
    for db in dblist:
        final_commands.append(format_command(db))
    final_bash = "\n".join(final_commands)
    print("==========Final Bash==========")
    print(final_bash)

    with open("./upgrade.sh", 'w') as f:
        f.write(final_bash)
        f.close()