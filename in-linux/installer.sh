#!/bin/bash

echo "1.Updating package list..."
sudo apt update -y

echo "2.Upgrading packages..."
sudo apt upgrade -y

echo "3.Installing build-essential..."
sudo apt install -y build-essential

echo "4.Verifying GCC installation..."
gcc --version

echo "5.Ready to Execute"
