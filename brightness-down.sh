#!/bin/bash

current_brightness=$(cat /sys/class/backlight/amdgpu_bl2/brightness)

new_brightness=$((current_brightness - 20))

if [ "$new_brightness" -lt 0 ]; then
    new_brightness=0
fi

pkexec tee /sys/class/backlight/amdgpu_bl2/brightness <<< "$new_brightness"
