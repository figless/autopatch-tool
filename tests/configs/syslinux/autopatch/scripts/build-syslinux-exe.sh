#!/bin/bash
set -e
set -o pipefail

CONTAINER_TAG=almalinux:10-kitten
PKGS="cpio rpm-build make git python3 python3-setuptools python3-pip dnf-plugins-core"
[ -d files ] || mkdir files
echo syslinux64.exe > files/syslinux64.exe
