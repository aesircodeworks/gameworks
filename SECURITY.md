# Security Policy

## Supported Versions

Only the `main` branch receives security fixes.

## Reporting a Vulnerability

**Do not report security vulnerabilities through public GitHub issues.**

Use GitHub's private vulnerability reporting on the upstream project when the issue originates there:

**[Report a vulnerability →](https://github.com/Donchitos/Claude-Code-Game-Studios/security/advisories/new)**

For Aesir-specific packaging, hooks, or Hermes integration issues, report privately to the Aesir Gameworks maintainers with reproduction steps and impact. Do not include secrets.

## What Is In Scope

Aesir Gameworks installs shell hooks and skills that run on the user's machine.

### High Severity

- Hooks that execute undisclosed commands
- Skills that exfiltrate environment variables, API keys, or secrets
- Prompt injection via skill or agent definitions
- Contributions that silently alter destructive behavior

Distribution packages must never ship `.env`, `auth.json`, memories, sessions, or state databases.
