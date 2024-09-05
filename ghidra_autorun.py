#! /usr/bin/python
import json
import os
import subprocess
import click


GHIDRA_CONFIG_PATH = os.path.expanduser("~/.ghidra_config.json")


def load_ghidra_path():
    if os.path.exists(GHIDRA_CONFIG_PATH):
        with open(GHIDRA_CONFIG_PATH, "r") as f:
            config = json.load(f)
            return config.get("ghidra_path")
    return None


def save_ghidra_path(ghidra_path):
    config = {"ghidra_path": ghidra_path}
    with open(GHIDRA_CONFIG_PATH, "w") as f:
        json.dump(config, f)


def create_and_import_project(ghidra_path, project_path, binary_path):
    analyze_headless_path = os.path.join(ghidra_path, "support", "analyzeHeadless")

    
    subprocess.run([
        analyze_headless_path, project_path, os.path.basename(project_path), "-import", binary_path
    ], check=True)


def open_in_ghidra(ghidra_path, project_path):
    ghidra_run_path = os.path.join(ghidra_path, "ghidraRun")
    project_file = os.path.join(project_path, f"{os.path.basename(project_path)}.gpr")
    subprocess.run([ghidra_run_path, project_file], check=True)


def create_project_in_current_dir(binary_name):
    current_dir = os.getcwd()  
    project_path = os.path.join(current_dir, binary_name + "_ghidra_project")  

    
    if not os.path.exists(project_path):
        os.makedirs(project_path)

    return project_path


def run_file_and_checksec(binary_path):
    
    file_cmd = subprocess.run(["file", binary_path], capture_output=True, text=True)
    click.secho("\n[file command output]:", fg="green")
    click.secho(file_cmd.stdout, fg="cyan")

    
    checksec_cmd = subprocess.run(["checksec", "--file", binary_path], capture_output=True, text=True)
    click.secho("\n[checksec command output]:", fg="green")
    click.secho(checksec_cmd.stdout, fg="cyan")


@click.command()
@click.argument('binary_path', type=click.Path(exists=True))
def main(binary_path):
    
    binary_name = os.path.splitext(os.path.basename(binary_path))[0]

    ghidra_path = load_ghidra_path()

    
    if not ghidra_path:
        ghidra_path = click.prompt("Enter the path to Ghidra installation", type=click.Path(exists=True))
        save_ghidra_path(ghidra_path)

    
    ghidra_run_path = os.path.join(ghidra_path, "ghidraRun")
    if not os.path.exists(ghidra_run_path):
        click.echo(f"Invalid Ghidra path: {ghidra_run_path}")
        return

    
    project_path = create_project_in_current_dir(binary_name)

    
    create_and_import_project(ghidra_path, project_path, binary_path)

    
    open_in_ghidra(ghidra_path, project_path)

    
    run_file_and_checksec(binary_path)

if __name__ == '__main__':
    main()
