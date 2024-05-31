#!/bin/bash
# curl -fsSL get.hassbox.cn/hassbox-notify | bash
set -e

export LC_ALL=en_US.UTF-8

RED_COLOR='\033[0;31m'
GREEN_COLOR='\033[0;32m'
GREEN_YELLOW='\033[1;33m'
NO_COLOR='\033[0m'

declare haPath
declare -a paths=(
    "$PWD"
    "$PWD/config"
    "/config"
    "$HOME/.homeassistant"
    "/usr/share/hassio/homeassistant"
)

function info () { echo -e "${GREEN_COLOR}INFO: $1${NO_COLOR}";}
function warn () { echo -e "${GREEN_YELLOW}WARN: $1${NO_COLOR}";}
function error () { echo -e "${RED_COLOR}ERROR: $1${NO_COLOR}";}

function checkRequirement () {
    if [ -z "$(command -v "$1")" ]; then
        warn "'$1' 未安装，准备安装..."
        apt install $1
    fi
}

info "检查依赖项"

checkRequirement "wget"
checkRequirement "unzip"

for path in "${paths[@]}"; do
    if [ -n "$haPath" ]; then
        break
    fi

    if [ -f "$path/.HA_VERSION" ]; then
        haPath="$path"
    fi
done

if [ -z "$haPath" ]; then
    echo
    error "找不到 Home Assistant 根目录"
    exit 1
fi

cd "$haPath"
if [ ! -d "$haPath/custom_components" ]; then
    mkdir "$haPath/custom_components"
fi

cd "$haPath/custom_components"

info "检查依赖项 ok"

info "下载 HassBox通知报警 安装包"
wget "https://get.hassbox.cn/hassbox_notify.zip" >/dev/null 2>&1
info "下载 HassBox通知报警 安装包 ok"

info "HassBox通知报警 安装包解压"

if [ -d "$haPath/custom_components/hassbox_notify" ]; then
    rm -R "$haPath/custom_components/hassbox_notify"
fi
mkdir "$haPath/custom_components/hassbox_notify"
unzip "$haPath/custom_components/hassbox_notify.zip" -d "$haPath/custom_components/hassbox_notify" >/dev/null 2>&1
rm "$haPath/custom_components/hassbox_notify.zip"
info "HassBox通知报警 安装包解压 ok"

info "安装成功！请重启 Home Assistant！如需其他帮助，可至 HassBox 微信公众号联系客服"
