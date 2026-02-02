#!/bin/sh

set -f  # disable globbing side effects

for fd in `ls /proc/self/fd`; do
  case "$fd" in
    ''|*[!0-9]*) continue ;;
  esac
  [ "$fd" -gt 2 ] && eval "exec $fd>&-" 2>/dev/null
done

exec ./broken_system
