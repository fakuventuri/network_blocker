#!/usr/bin/env bash
repopath=$(realpath .)

if [ ! -d "/system" ]; then
  tmp="/tmp/network-blocker"

  # download latest version
  rm -rf "$tmp/"
  git clone https://github.com/fakuventuri/network_blocker "$tmp/"
  cp -R "$tmp/." "$repopath/" 2>/dev/null # suppress git overwrite errors
fi