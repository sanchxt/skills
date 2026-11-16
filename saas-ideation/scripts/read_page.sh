#!/usr/bin/env bash
# Read the rendered text of a URL through the user's own Chrome (chrome-devtools CLI),
# in a background tab that is closed afterwards. Read-only.
# Usage: read_page.sh <url> [max_chars=12000] [js_expression_returning_value]
set -u
export NODE_NO_WARNINGS=1
URL="$1"; MAX="${2:-12000}"; EXPR="${3:-}"
chrome-devtools status >/dev/null 2>&1 || chrome-devtools start --autoConnect >/dev/null 2>&1
before=$(chrome-devtools list_pages 2>/dev/null | grep -oE '^[0-9]+:' | tr -d ':' | sort -n)
chrome-devtools new_page "$URL" --background true --timeout 30000 >/dev/null 2>&1
after=$(chrome-devtools list_pages 2>/dev/null | grep -oE '^[0-9]+:' | tr -d ':' | sort -n)
PID=$(comm -13 <(echo "$before") <(echo "$after") | tail -1)
if [ -z "$PID" ]; then echo "ERROR: could not open tab (is Chrome remote debugging on? chrome://inspect/#remote-debugging)"; exit 1; fi
if [ -z "$EXPR" ]; then EXPR="document.body.innerText"; fi
chrome-devtools evaluate_script --pageId "$PID" --waitForStableDom true \
  "async () => { await new Promise(r=>setTimeout(r,1500)); const v = await (async()=>($EXPR))(); const s = typeof v==='string'? v : JSON.stringify(v); return ('URL: '+location.href+'\nTITLE: '+document.title+'\n\n'+s).slice(0,$MAX); }" 2>/dev/null \
  | grep -v -i "update available\|Run \`npm"
chrome-devtools close_page "$PID" >/dev/null 2>&1
