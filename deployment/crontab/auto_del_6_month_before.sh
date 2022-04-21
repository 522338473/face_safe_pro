#!/bin/sh

# 1. Cleaning up files 180 days ago
find /data/docker/fastdfs/files/ -mtime +180 -type f -name "*" -exec rm -rf {} \;

# 2. Cleaning up empty dictionary 180 days ago
find /data/docker/fastdfs/files/ -mtime +180 -type d -name "*" -exec rm -rf {} \;
