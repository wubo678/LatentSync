import os
import re
from pathlib import Path
from dotenv import dotenv_values
import shutil

#############################################################################
#
# in order to replace the settings enclosed in ${} in the yaml file
# with the settings in the .env file
#
#############################################################################

def load_env_vars(env_path=".env"):
    return dotenv_values(env_path)

def replace_vars_in_text(text, env_vars):
    pattern = re.compile(r"\$\{(\w+)\}")
    return pattern.sub(lambda m: env_vars.get(m.group(1), m.group(0)), text)

def process_files(source_dir, target_dir, env_vars):
    source_dir = Path(source_dir)
    target_dir = Path(target_dir)

    if target_dir.exists():
        shutil.rmtree(target_dir)

    for path in source_dir.rglob("*"):
        relative_path = path.relative_to(source_dir)
        target_path = target_dir / relative_path

        if path.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)
        else:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            new_content = replace_vars_in_text(content, env_vars)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(new_content)

def main():
    env_vars = load_env_vars(".env")
    process_files("configsOriginal", "configs", env_vars)
    print("✅ Replace Success -> configs/")

if __name__ == "__main__":
    main()
