#!/bin/bash
set -e

echo "===== Building the project ====="
./gradlew clean build

echo "===== Running tests ====="
./gradlew test

echo "===== Checking for Lombok processor ====="
./gradlew -q dependencies | grep lombok

echo "===== Checking for Jakarta Persistence ====="
./gradlew -q dependencies | grep jakarta

echo "===== Project built successfully! ====="