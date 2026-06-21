import argparse
import os
import shutil
import subprocess
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)


def _python_candidates(preferred=None):
    if preferred:
        return [preferred]

    candidates = [sys.executable]
    venv_bin_dir = os.path.join(PROJECT_ROOT, ".venv", "bin")
    candidates.extend(
        [
            os.path.join(venv_bin_dir, "python"),
            os.path.join(venv_bin_dir, "python3"),
            os.path.join(venv_bin_dir, f"python{sys.version_info.major}.{sys.version_info.minor}"),
        ]
    )

    unique_candidates = []
    seen = set()
    for candidate in candidates:
        if candidate and candidate not in seen:
            seen.add(candidate)
            unique_candidates.append(candidate)
    return unique_candidates


def _python_has_easyeda2kicad(python_exec):
    try:
        subprocess.run(
            [python_exec, "-c", "import easyeda2kicad"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def resolve_path(path):
    path = os.path.expanduser(path)
    if os.path.isabs(path):
        return path
    return os.path.abspath(os.path.join(PROJECT_ROOT, path))

def run_easyeda2kicad_from_file(input_file, output_dir="./lib/lcsc", python_exec=None):
    input_file = resolve_path(input_file)
    output_dir = resolve_path(output_dir)

    if not os.path.isfile(input_file):
        print(f"Error: File not found: {input_file}")
        return 2

    python_candidates = _python_candidates(python_exec)

    selected_python = None
    for candidate in python_candidates:
        if _python_has_easyeda2kicad(candidate):
            selected_python = candidate
            break

    if selected_python is None:
        fallback_python = os.path.join(PROJECT_ROOT, ".venv", "bin", "python")
        print(
            f"❌ Missing dependency: easyeda2kicad is not installed for '{python_candidates[0]}'. "
            f"Install it with '{python_candidates[0]} -m pip install easyeda2kicad' or run the script from a virtual environment that has it installed, such as '{fallback_python}'."
        )
        return 4

    if selected_python != (python_exec or sys.executable):
        print(f"Using Python executable with easyeda2kicad installed: {selected_python}")

    python_exec = selected_python

    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        # ignore blank lines and comments
        lines = [line.strip() for line in f if line.strip() and not line.lstrip().startswith("#")]

    if not lines:
        print("No LCSC IDs found in input file.")
        return 0

    for idx, lcsc_id in enumerate(lines, start=1):
        cmd = [
            python_exec,
            "-m", "easyeda2kicad",
            "--full",
            f"--lcsc_id={lcsc_id}",
            f"--output={output_dir}",
        ]
        print(f"[{idx}/{len(lines)}] Running: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error processing {lcsc_id}: {e}")
        except FileNotFoundError as e:
            print(f"❌ Executable not found: {e}")
            return 3

    print("✅ All commands completed.")
    return 0

def main(argv=None):
    parser = argparse.ArgumentParser(description="Run easyeda2kicad for a list of LCSC IDs.")
    parser.add_argument("input_file", nargs="?", default="./lib/lcsc.txt", help="Path to file with one LCSC ID per line")
    parser.add_argument("output_dir", nargs="?", default="./lib/lcsc", help="Output directory")
    parser.add_argument("--python", dest="python_exec", default=None,
                        help="Python executable to use (default: the current interpreter)")
    args = parser.parse_args(argv)

    return_code = run_easyeda2kicad_from_file(args.input_file, args.output_dir, args.python_exec)
    sys.exit(return_code if isinstance(return_code, int) else 0)

if __name__ == "__main__":
    main()