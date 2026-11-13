import os
from pathlib import Path
import sys

def parse_env_file(file_path):
    config = {}
    if not file_path.exists():
        return config
    for line in file_path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            key, val = line.split('=', 1)
            config[key.strip()] = val.strip()
    return config

def audit_environment(target_dir):
    target_path = Path(target_dir)
    env_path = target_path / '.env'
    example_path = target_path / '.env.example'

    print(f"[*] Auditing configuration in: {target_path.resolve()}\n")

    if not env_path.exists():
        print("[!] ERROR: Missing .env file in target directory.")
        return False

    if not example_path.exists():
        print("[!] WARNING: Missing .env.example template file for comparison.")

    env_vars = parse_env_file(env_path)
    example_vars = parse_env_file(example_path)

    missing_keys = [k for k in example_vars if k not in env_vars]
    extra_keys = [k for k in env_vars if k not in example_vars]

    print("=== CONFIGURATION AUDIT REPORT ===")
    print(f"  Total keys in .env: {len(env_vars)}")
    print(f"  Total keys in template: {len(example_vars)}")

    if missing_keys:
        print(f"\n[!] MISSING KEYS (Present in template, absent in .env):")
        for k in missing_keys:
            print(f"    - {k}")
    else:
        print("\n[+] All template keys are present in .env.")

    if extra_keys:
        print(f"\n[i] EXTRA KEYS (Present in .env, absent in template):")
        for k in extra_keys:
            print(f"    + {k}")

    # Security heuristic checks
    print("\n=== SECURITY HEURISTIC CHECKS ===")
    security_warnings = []
    
    for k, v in env_vars.items():
        if 'password' in k.lower() and v in ['password', '123456', 'admin', 'root']:
            security_warnings.append(f"Insecure default password detected for key '{k}': '{v}'")
        if 'secret' in k.lower() and len(v) < 10:
            security_warnings.append(f"Weak or short secret value detected for key '{k}' (length < 10)")

    if security_warnings:
        for warning in security_warnings:
            print(f"  [ALERT] {warning}")
    else:
        print("  No obvious credential vulnerabilities flagged.")

    return len(missing_keys) == 0 and len(security_warnings) == 0

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'sample_project'
    success = audit_environment(target)
    sys.exit(0 if success else 1)