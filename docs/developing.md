# Developing Guide

## Developing riscv-pvp

riscv-pvp provide a python package, we should use `--editable` option while
`pip install` to allow developing.

```bash
pip install --editable .
```

## Debugging with VSCode

The above configuration is used for developers to debugging rvpvp self in
VSCode.

After python extension is installed, we could place this into
`.vscode/launch.json` then launch debugging.

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "rvpvp gen",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/rvpvp/main.py",
            "args": [
                "gen",
            ],
            "cwd": "${workspaceFolder}/targets/spike-rv64gcv",
            "console": "integratedTerminal"
        },
        {
            "name": "rvpvp run",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/rvpvp/main.py",
            "args": [
                "run",
            ],
            "cwd": "${workspaceFolder}/targets/spike-rv64gcv",
            "console": "integratedTerminal"
        }
    ]
}
```