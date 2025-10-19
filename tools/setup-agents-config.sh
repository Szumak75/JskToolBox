#!/bin/bash
# -*- coding: utf-8 -*-
"""
Setup AGENTS.md configuration for a new Python project

This script helps configure AGENTS.md from AGENTS-PYTEMPLATE.md
by replacing template variables with actual project values.

Usage:
    ./setup-agents-config.sh

Author: Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
"""

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================"
echo "  AGENTS.md Configuration Setup for Python"
echo "================================================"
echo ""

# Check if AGENTS-PYTEMPLATE.md exists
if [ ! -f "AGENTS-PYTEMPLATE.md" ]; then
    echo -e "${RED}Error: AGENTS-PYTEMPLATE.md not found!${NC}"
    echo "Please run this script from the JskToolBox repository root."
    exit 1
fi

# Prompt for project details
echo -e "${YELLOW}Enter project details (press Enter to skip optional fields):${NC}"
echo ""

read -p "Project Name (e.g., MyAwesomeProject): " PROJECT_NAME
while [ -z "$PROJECT_NAME" ]; do
    echo -e "${RED}Project name is required!${NC}"
    read -p "Project Name: " PROJECT_NAME
done

read -p "Package Name (e.g., myproject): " PACKAGE_NAME
while [ -z "$PACKAGE_NAME" ]; do
    echo -e "${RED}Package name is required!${NC}"
    read -p "Package Name: " PACKAGE_NAME
done

read -p "Author Name (e.g., Jan Kowalski): " AUTHOR_NAME
while [ -z "$AUTHOR_NAME" ]; do
    echo -e "${RED}Author name is required!${NC}"
    read -p "Author Name: " AUTHOR_NAME
done

read -p "Author Email (e.g., jan@example.com): " AUTHOR_EMAIL
while [ -z "$AUTHOR_EMAIL" ]; do
    echo -e "${RED}Author email is required!${NC}"
    read -p "Author Email: " AUTHOR_EMAIL
done

read -p "Python Version (default: 3.10+): " PYTHON_VERSION
PYTHON_VERSION=${PYTHON_VERSION:-"3.10+"}

read -p "Test Directory (default: tests): " TEST_DIR
TEST_DIR=${TEST_DIR:-"tests"}

read -p "Docs Directory (default: docs): " DOCS_DIR
DOCS_DIR=${DOCS_DIR:-"docs"}

read -p "Examples Directory (optional, press Enter to skip): " EXAMPLES_DIR
EXAMPLES_DIR=${EXAMPLES_DIR:-"examples"}

# Output directory
read -p "Output directory (default: current directory): " OUTPUT_DIR
OUTPUT_DIR=${OUTPUT_DIR:-"."}

# Create output file path
OUTPUT_FILE="${OUTPUT_DIR}/AGENTS.md"

echo ""
echo -e "${YELLOW}Configuration summary:${NC}"
echo "  Project Name:      $PROJECT_NAME"
echo "  Package Name:      $PACKAGE_NAME"
echo "  Author:            $AUTHOR_NAME <$AUTHOR_EMAIL>"
echo "  Python Version:    $PYTHON_VERSION"
echo "  Test Directory:    $TEST_DIR"
echo "  Docs Directory:    $DOCS_DIR"
echo "  Examples Directory: $EXAMPLES_DIR"
echo "  Output File:       $OUTPUT_FILE"
echo ""

read -p "Proceed with configuration? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "Configuration cancelled."
    exit 0
fi

# Copy template and perform replacements
echo ""
echo -e "${GREEN}Creating AGENTS.md...${NC}"

cp AGENTS-PYTEMPLATE.md "$OUTPUT_FILE"

# Replace variables
sed -i "s/{PROJECT_NAME}/${PROJECT_NAME}/g" "$OUTPUT_FILE"
sed -i "s/{PACKAGE_NAME}/${PACKAGE_NAME}/g" "$OUTPUT_FILE"
sed -i "s/{AUTHOR_NAME}/${AUTHOR_NAME}/g" "$OUTPUT_FILE"
sed -i "s/{AUTHOR_EMAIL}/${AUTHOR_EMAIL}/g" "$OUTPUT_FILE"
sed -i "s/{PYTHON_VERSION}/${PYTHON_VERSION}/g" "$OUTPUT_FILE"
sed -i "s/{TEST_DIR}/${TEST_DIR}/g" "$OUTPUT_FILE"
sed -i "s/{DOCS_DIR}/${DOCS_DIR}/g" "$OUTPUT_FILE"
sed -i "s/{EXAMPLES_DIR}/${EXAMPLES_DIR}/g" "$OUTPUT_FILE"

# Get current date
CURRENT_DATE=$(date +%Y-%m-%d)
sed -i "s/2024-XX-XX/${CURRENT_DATE}/g" "$OUTPUT_FILE"

echo -e "${GREEN}✓ AGENTS.md created successfully!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Review the generated file: $OUTPUT_FILE"
echo "2. Remove the template comment section at the top"
echo "3. Customize project-specific sections"
echo "4. Remove/modify JskToolBox sections if not using the library"
echo "5. Commit to your repository: git add AGENTS.md && git commit -m 'docs: add AI agent configuration'"
echo ""
echo -e "${GREEN}Done!${NC}"
