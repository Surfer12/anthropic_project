#!/bin/bash
set -e

# This script downloads the Gradle wrapper jar file

WRAPPER_JAR_URL="https://github.com/gradle/gradle/raw/v7.6.0/gradle/wrapper/gradle-wrapper.jar"
WRAPPER_JAR_PATH="/Users/ryanoates/anthropic_project/gradle/wrapper/gradle-wrapper.jar"

curl -L -o "$WRAPPER_JAR_PATH" "$WRAPPER_JAR_URL"

echo "Downloaded gradle-wrapper.jar to $WRAPPER_JAR_PATH"