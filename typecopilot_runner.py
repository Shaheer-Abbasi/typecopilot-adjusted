import subprocess
import os

# Bitcode directory (LLVM 14, compiled with -g for debug info)
BC_DIR = "/lab/test_cases/bc"

# TypeCopilot plugin and opt binary (built against LLVM 14)
PLUGIN = "/opt/typecopilot/build/libTypeCopilot.so"
OPT    = "/usr/lib/llvm-14/bin/opt"


def print_menu():
    print("TypeCopilot")
    print("Options:")
    print("  1. Enter coreutil name to be analyzed by TypeCopilot")
    print("  exit. Exit program")


def prompt_user():
    print_menu()
    name = input("Coreutil name: ").strip()
    return name


while True:
    user_input = prompt_user()

    if user_input == "exit":
        break

    bc_file = os.path.join(BC_DIR, f"{user_input}.bc")

    if not os.path.exists(bc_file):
        print(f"Error: {bc_file} not found")
        print()
        continue

    try:
        result = subprocess.run(
            [
                OPT,
                "-load-pass-plugin", PLUGIN,
                "-passes=typecopilot",
                "-dump-type=true",
                "-type-src=comb",
                "-wl=true",
                "-baseline=false",
                "-o", "/dev/null",
                bc_file,
            ],
            capture_output=True,
            text=True,
        )

        # TypeCopilot writes type recovery output to stderr
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode != 0:
            print(f"opt exited with code {result.returncode}")

    except Exception as e:
        print("Error:", e)

    print()
