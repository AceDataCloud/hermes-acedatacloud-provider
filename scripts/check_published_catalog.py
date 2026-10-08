"""Opt-in public catalog acceptance on a prepared, unmodified Hermes release.

Run with HERMES_SOURCE set and that release's Python interpreter. This checks
the public directory and Git installation; it makes no inference requests.
"""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import urllib.request


def main():
    source = Path(os.environ["HERMES_SOURCE"]).resolve()
    url = "https://hermes-agent.nousresearch.com/docs/api/plugin-catalog.json"
    with urllib.request.urlopen(url, timeout=30) as response:
        catalog = json.load(response)
    entry = next(item for item in catalog["entries"] if item["name"] == "acedatacloud")
    with tempfile.TemporaryDirectory(prefix="hermes-published-catalog-") as directory:
        profile = Path(directory)
        env = {key: value for key, value in os.environ.items() if key in {
            "PATH", "SYSTEMROOT", "LANG", "TMP", "TEMP", "HOME",
        }}
        env.update(HERMES_HOME=str(profile), PYTHONPATH=str(source))

        def run(*args):
            result = subprocess.run(
                [sys.executable, *args], cwd=profile, env=env,
                text=True, capture_output=True, timeout=180,
            )
            print(result.stdout, end="", flush=True)
            if result.stderr:
                print(result.stderr, file=sys.stderr, end="", flush=True)
            result.check_returncode()
            return result.stdout

        version = run("-m", "hermes_cli.main", "--version")
        run("-m", "hermes_cli.main", "plugins", "search", "acedatacloud")
        info = run("-m", "hermes_cli.main", "plugins", "info", "acedatacloud")
        assert entry["sha"][:8] in info
        run("-m", "hermes_cli.main", "plugins", "install", "acedatacloud", "--enable")
        installed = profile / "plugins" / "acedatacloud"
        sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=installed, text=True
        ).strip()
        assert sha == entry["sha"], (sha, entry["sha"])
        run("-m", "hermes_cli.main", "plugins", "list", "--json")
        env["ACEDATACLOUD_API_KEY"] = "test-discovery-placeholder"
        run("-c", """
from providers import get_provider_profile
from hermes_cli.models import list_available_providers
from hermes_cli.runtime_provider import resolve_runtime_provider
import json
p = get_provider_profile('acedatacloud')
assert p is not None
row = next(row for row in list_available_providers() if row['id'] == 'acedatacloud')
assert row['label'] == 'Ace Data Cloud' and row['authenticated']
runtime = resolve_runtime_provider(requested='acedatacloud', target_model='gpt-4.1-mini')
assert runtime['provider'] == 'acedatacloud'
assert runtime['api_mode'] == 'chat_completions'
assert runtime['base_url'] == 'https://api.acedata.cloud/openai'
assert set(p.fallback_models) == {'gpt-4.1-mini', 'gpt-4.1'}
print(json.dumps({'provider': row, 'models': list(p.fallback_models),
                  'base_url': runtime['base_url'], 'api_mode': runtime['api_mode']}))
""")
        print(json.dumps({"published_catalog_install": "passed", "version": version.strip(),
                          "plugin_sha": sha, "tier": entry["tier"]}), flush=True)


if __name__ == "__main__":
    main()
