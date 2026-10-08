# Ace Data Cloud model provider for Hermes Agent

![Ace Data Cloud](assets/catalog.png)

Maintained by [Ace Data Cloud](https://acedata.cloud). This plugin adds **Ace Data
Cloud** to Hermes's model and setup pickers using its public Chat Completions API.
It requires Hermes 0.21.5 or later and is listed in the
[official Hermes plugin catalog](https://hermes-agent.nousresearch.com/docs/plugins/acedatacloud)
as a community plugin. It is installed separately and is not bundled with Hermes.

## Install and configure

```sh
hermes plugins install acedatacloud --enable
hermes model
```

Choose **Ace Data Cloud**, enter your API key, then select `gpt-4.1-mini` or
`gpt-4.1`. Get a key from your application in the
[Ace Data Cloud console](https://platform.acedata.cloud/console/applications).
Enable the required chat service on that application. Keys scoped to other
services cannot make chat requests.

For an environment-based setup, set `ACEDATACLOUD_API_KEY` in the active Hermes
profile's `.env` file. Keep credentials out of `config.yaml` and source control.
Then run:

```sh
hermes chat --provider acedatacloud --model gpt-4.1-mini --oneshot "Reply only OK"
```

The plugin supplies the base URL `https://api.acedata.cloud/openai` and the
`chat_completions` transport. No custom-provider YAML is needed. Install it in
each Hermes profile that should use it.

## Supported models

The picker offers `gpt-4.1-mini` and `gpt-4.1`. Both support text conversations,
streaming tool calls and subsequent tool-result turns. The plugin filters the
live catalog to these tested models; if the catalog is unavailable, the same
two IDs remain available in the picker. This is a picker list, not automatic
model substitution.

Ace Data Cloud's shared `/models` response also contains image-generation and
other-protocol models. They are intentionally excluded. This plugin does not
claim support for the full catalog, Responses, Messages, vision, prompt caching
or configurable reasoning. New model families will be added after validating
their Hermes transport behavior.

Calls use your Ace Data Cloud balance. See the
[current model catalog and pricing](https://platform.acedata.cloud/models) and
your application's package rate. Hermes may not have an accurate cost estimate
for this provider; the Ace Data Cloud usage and billing records are authoritative.

## Data and permissions

- Hermes sends chat messages, configured tool schemas and tool results to
  `https://api.acedata.cloud/openai/chat/completions` with your API key. Model
  discovery calls `https://api.acedata.cloud/openai/models` through Hermes's
  standard credentialed client. A user-configured base URL overrides both.
- The plugin declares only `ACEDATACLOUD_API_KEY`; Hermes manages that secret.
  It does not read other applications' credentials, write files, run shell
  commands, start background processes, install dependencies or update itself.
- It registers one model-provider profile. There are no tools, hooks,
  middleware, telemetry or automatic model fallbacks in the plugin.
- Updates installed from the Hermes catalog require a reviewed SHA pin update
  and `hermes plugins update acedatacloud`.

## Troubleshooting and support

For authentication errors, check the active profile's key and application
permissions. For quota or credit errors, inspect the application's balance.
For rate limits, retry later. The plugin leaves API errors to Hermes's standard
error handling rather than converting them into successful responses.

Report plugin issues in this repository. Account and billing support is
available through the [Ace Data Cloud console](https://platform.acedata.cloud).

## Development

Tests use a real Hermes checkout, isolated temporary homes and a local HTTP
server. CI uses Hermes's official validation action against the stable release
and a pinned main commit. With a prepared Hermes interpreter, run:

```sh
HERMES_SOURCE=/absolute/path/to/hermes-agent python -m unittest discover -s tests -v
```

Validate the installable plugin before publishing:

```sh
hermes plugins validate /absolute/path/to/hermes-acedatacloud-provider --install-deps
```

Live checks use only disposable Hermes homes and explicitly supplied test keys.
