# Development Workstation Verification

Verified on 15 September 2026 using macOS 15.6.1 (Apple silicon). The onboarding
slides use Windows commands, but the application and container are
cross-platform.

| Tool | Verification command | Installed version | Download source | Issue and solution |
| --- | --- | --- | --- | --- |
| Visual Studio Code | `code --version` | 1.129.1 | <https://code.visualstudio.com/> | The `code` shell command is not on `PATH`; verified with the command inside the installed application bundle. |
| Git | `git --version` | 2.39.5 (Apple Git-154) | Included with Apple developer tools | No issue. |
| Docker Desktop | `docker --version` | 29.7.2 | <https://www.docker.com/products/docker-desktop/> | Docker's saved Keychain credential helper failed while pulling a public image. Verification used a temporary empty Docker configuration; normal settings were not changed. |
| Docker Compose | `docker compose version` | v5.4.0 | Included with Docker Desktop | No issue. |
| Python | `.venv/bin/python --version` | 3.12.14 | Bundled Codex Python runtime | The macOS default is Python 3.9.6, so the project virtual environment was explicitly created with the available Python 3.12 runtime. |
| pip | `.venv/bin/python -m pip --version` | 25.0.1 | Included with Python | No issue. |
| Node.js | `node --version` | v24.19.0 | Existing workstation installation | No issue; Node.js is not needed by this Python service. |
| npm | `npm --version` | 11.17.0 | Included with Node.js | No issue. |

Docker was verified by building `student-agent:0.1.0`, starting a container, and
calling `/health` and `/task` successfully. The generic onboarding check is:

```powershell
docker run hello-world
```

Do not record passwords, API keys, tokens, or other secrets in this file.
