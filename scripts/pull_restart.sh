#!/bin/bash
systemctl stop t25.service
git clone https://github.com/aquaforge/T25.git 
systemctl start t25.service
