#!/bin/bash

current_brightness=$(cat /sys/class/backlight/amdgpu_bl2/brightness)
max_brightness=$(cat /sys/class/backlight/amdgpu_bl2/max_brightness)

new_brightness=$((current_brightness + 20))

if [ "$new_brightness" -gt "$max_brightness" ]; then
    new_brightness=$max_brightness
fi

pkexec tee /sys/class/backlight/amdgpu_bl2/brightness <<< "$new_brightness"
