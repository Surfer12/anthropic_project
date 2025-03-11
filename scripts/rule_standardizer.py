#!/usr/bin/env python
"""
Rule Standardizer

This script manages and verifies linting rule consistency across different
programming languages. It can generate language-specific configurations from
a unified rule definition and verify rule consistency.

Usage:
    python rule_standardizer.py [--generate] [--verify] [--fix] [config_path]
"""

import argparse
import os
import sys
import yaml
import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Any, Union


class ConfigFormat(Enum):
    """Supported configuration file formats."""
    YAML = "yaml"
    JSON = "json"
    XML = "xml"
    INI = "ini"
    TOML = "toml"


@dataclass
class LanguageConfig:
    """Configuration for a specific language."""
    name: str
    config_path: str
    format: ConfigFormat
    rules: Dict[str, Any]


def load_unified_rules(rules_path: str) -> Dict[str, Any]:
    """Load the unified rules configuration."""
    try:
        with open(rules_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading unified rules from {rules_path}: {str(e)}")
        sys.exit(1)


def generate_black_config(rules: Dict[str, Any]) -> Dict[str, Any]:
    """Generate Black configuration from unified rules."""
    config = {
        'line-length': rules['max_line_length']['python'],
        'target-version': ['py38'],
        'include': r'\.pyi?$',
        'extend-exclude': r'(\.git|\.hg|\.mypy_cache|\.tox|\.venv|_build|buck-out|build|dist)',
    }
    return config


def generate_checkstyle_config(rules: Dict[str, Any]) -> str:
    """Generate Checkstyle configuration from unified rules."""
    root = ET.Element("module", name="Checker")
    
    # File length
    file_length = ET.SubElement(root, "module", name="LineLength")
    file_length.set("max", str(rules['max_line_length']['java']))
    
    # Indentation
    tree_walker = ET.SubElement(root, "module", name="TreeWalker")
    indentation = ET.SubElement(tree_walker, "module", name="Indentation")
    indentation.set("basicOffset", str(rules['indentation']['java']))
    
    # Naming conventions
    naming = rules['naming_conventions']['java']
    for element, pattern in naming.items():
        name_module = ET.SubElement(tree_walker, "module", name="NamePattern")
        name_module.set("element", element)
        name_module.set("pattern", pattern)
    
    return ET.tostring(root, encoding='unicode', xml_declaration=True)


def generate_clang_format_config(rules: Dict[str, Any]) -> Dict[str, Any]:
    """Generate clang-format configuration from unified rules."""
    config = {
        'BasedOnStyle': 'Google',
        'ColumnLimit': rules['max_line_length']['cpp'],
        'IndentWidth': rules['indentation']['cpp'],
        'UseTab': 'Never',
        'NamespaceIndentation': 'None',
        'BreakBeforeBraces': 'Attach',
        'AllowShortFunctionsOnASingleLine': 'Empty',
        'AllowShortIfStatementsOnASingleLine': 'Never',
        'AllowShortLoopsOnASingleLine': 'false',
        'DerivePointerAlignment': 'false',
        'PointerAlignment': 'Left',
    }
    return config


def generate_mojo_format_config(rules: Dict[str, Any]) -> Dict[str, Any]:
    """Generate Mojo format configuration from unified rules."""
    config = {
        'line_length': rules['max_line_length']['mojo'],
        'indent_size': rules['indentation']['mojo'],
        'use_spaces': True,
        'naming_conventions': rules['naming_conventions']['mojo'],
    }
    return config


def generate_markdownlint_config(rules: Dict[str, Any]) -> Dict[str, Any]:
    """Generate markdownlint configuration from unified rules."""
    config = {
        'MD013': {  # Line length rule
            'line_length': rules['max_line_length']['markdown'],
            'heading_line_length': rules['max_line_length']['markdown'],
            'code_block_line_length': rules['max_line_length']['markdown'],
        },
        'MD004': {'style': 'dash'},  # Unordered list style
        'MD007': {'indent': rules['indentation']['markdown']},  # List indentation
        'MD029': {'style': 'ordered'},  # Ordered list numbering style
        'MD031': {'true'},  # Blank lines around fenced code blocks
        'MD032': {'true'},  # Lists should be surrounded by blank lines
        'MD041': {'true'},  # First line in file should be a top level heading
        'MD046': {'style': 'consistent'},  # Code block style
    }
    return config


def verify_rule_consistency(unified_rules: Dict[str, Any], configs: List[LanguageConfig]) -> List[str]:
    """Verify consistency of rules across language configurations."""
    inconsistencies = []
    
    # Check line length consistency
    line_lengths = {}
    for lang in ['python', 'java', 'cpp', 'mojo', 'markdown']:
        if lang in unified_rules['max_line_length']:
            line_lengths[lang] = unified_rules['max_line_length'][lang]
    
    # Check for large variations in line length
    avg_line_length = sum(line_lengths.values()) / len(line_lengths)
    for lang, length in line_lengths.items():
        if abs(length - avg_line_length) > 20:  # Allow 20 char variation
            inconsistencies.append(
                f"Line length for {lang} ({length}) differs significantly from average ({avg_line_length:.0f})"
            )
    
    # Check indentation consistency
    indentations = {}
    for lang in ['python', 'java', 'cpp', 'mojo']:
        if lang in unified_rules['indentation']:
            indentations[lang] = unified_rules['indentation'][lang]
    
    # Most languages should use consistent indentation
    common_indent = max(set(indentations.values()), key=list(indentations.values()).count)
    for lang, indent in indentations.items():
        if indent != common_indent and lang not in ['cpp']:  # cpp commonly uses different indentation
            inconsistencies.append(
                f"Indentation for {lang} ({indent}) differs from common indentation ({common_indent})"
            )
    
    # Check naming convention consistency
    for element in ['class', 'function', 'variable', 'constant']:
        conventions = {}
        for lang in ['python', 'java', 'mojo']:
            if lang in unified_rules['naming_conventions']:
                lang_conventions = unified_rules['naming_conventions'][lang]
                if element in lang_conventions:
                    conventions[lang] = lang_conventions[element]
        
        # Check for inconsistencies in similar languages
        similar_langs = [('python', 'mojo')]  # Languages that should have similar conventions
        for lang1, lang2 in similar_langs:
            if lang1 in conventions and lang2 in conventions:
                if conventions[lang1] != conventions[lang2]:
                    inconsistencies.append(
                        f"{element} naming convention differs between {lang1} ({conventions[lang1]}) "
                        f"and {lang2} ({conventions[lang2]})"
                    )
    
    return inconsistencies


def apply_fixes(unified_rules: Dict[str, Any], inconsistencies: List[str]) -> Dict[str, Any]:
    """Apply automatic fixes to resolve rule inconsistencies."""
    fixed_rules = unified_rules.copy()
    
    # Fix line length inconsistencies
    if any('line length' in issue.lower() for issue in inconsistencies):
        # Use most common line length as standard
        line_lengths = [
            fixed_rules['max_line_length'][lang]
            for lang in ['python', 'java', 'cpp', 'mojo', 'markdown']
            if lang in fixed_rules['max_line_length']
        ]
        common_length = max(set(line_lengths), key=line_lengths.count)
        
        # Adjust line lengths, preserving some language-specific variations
        for lang in ['python', 'java', 'cpp', 'mojo', 'markdown']:
            if lang in fixed_rules['max_line_length']:
                if lang == 'java':  # Java traditionally allows longer lines
                    fixed_rules['max_line_length'][lang] = min(100, common_length + 20)
                elif lang == 'cpp':  # C++ traditionally prefers shorter lines
                    fixed_rules['max_line_length'][lang] = min(80, common_length)
                else:
                    fixed_rules['max_line_length'][lang] = common_length
    
    # Fix indentation inconsistencies
    if any('indentation' in issue.lower() for issue in inconsistencies):
        # Use 4 spaces as standard for most languages
        for lang in ['python', 'java', 'mojo']:
            if lang in fixed_rules['indentation']:
                fixed_rules['indentation'][lang] = 4
        # Preserve C++ 2-space indentation as it's a common standard
        if 'cpp' in fixed_rules['indentation']:
            fixed_rules['indentation']['cpp'] = 2
    
    # Fix naming convention inconsistencies
    if any('naming convention' in issue.lower() for issue in inconsistencies):
        # Standardize Python and Mojo conventions
        python_conventions = fixed_rules['naming_conventions'].get('python', {})
        if python_conventions:
            fixed_rules['naming_conventions']['mojo'] = python_conventions.copy()
    
    return fixed_rules


def generate_configs(unified_rules: Dict[str, Any], output_dir: str) -> None:
    """Generate language-specific configurations from unified rules."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate Black config (pyproject.toml)
    black_config = generate_black_config(unified_rules)
    with open(os.path.join(output_dir, 'pyproject.toml'), 'w', encoding='utf-8') as f:
        f.write("[tool.black]\n")
        for key, value in black_config.items():
            f.write(f"{key} = {repr(value)}\n")
    
    # Generate Checkstyle config
    checkstyle_config = generate_checkstyle_config(unified_rules)
    with open(os.path.join(output_dir, 'checkstyle.xml'), 'w', encoding='utf-8') as f:
        f.write(checkstyle_config)
    
    # Generate clang-format config
    clang_config = generate_clang_format_config(unified_rules)
    with open(os.path.join(output_dir, '.clang-format'), 'w', encoding='utf-8') as f:
        yaml.dump(clang_config, f, sort_keys=False)
    
    # Generate Mojo format config
    mojo_config = generate_mojo_format_config(unified_rules)
    with open(os.path.join(output_dir, '.mojo-format'), 'w', encoding='utf-8') as f:
        yaml.dump(mojo_config, f, sort_keys=False)
    
    # Generate markdownlint config
    markdown_config = generate_markdownlint_config(unified_rules)
    with open(os.path.join(output_dir, '.markdownlint.yaml'), 'w', encoding='utf-8') as f:
        yaml.dump(markdown_config, f, sort_keys=False)


def main():
    parser = argparse.ArgumentParser(description="Standardize and verify linting rules")
    parser.add_argument("--rules", default=".linting/rules.yaml", help="Path to unified rules file")
    parser.add_argument("--generate", action="store_true", help="Generate language-specific configs")
    parser.add_argument("--verify", action="store_true", help="Verify rule consistency")
    parser.add_argument("--fix", action="store_true", help="Automatically fix inconsistencies")
    parser.add_argument("--output-dir", default=".linting/generated", help="Output directory for generated configs")
    
    args = parser.parse_args()
    
    # Load unified rules
    unified_rules = load_unified_rules(args.rules)
    
    # Verify rule consistency if requested
    if args.verify:
        print("Verifying rule consistency...")
        inconsistencies = verify_rule_consistency(unified_rules, [])  # Empty list for now
        
        if inconsistencies:
            print("\nFound rule inconsistencies:")
            for issue in inconsistencies:
                print(f"- {issue}")
            
            if args.fix:
                print("\nApplying fixes...")
                unified_rules = apply_fixes(unified_rules, inconsistencies)
                
                # Save fixed rules
                with open(args.rules, 'w', encoding='utf-8') as f:
                    yaml.dump(unified_rules, f, sort_keys=False)
                print(f"Fixed rules saved to {args.rules}")
        else:
            print("No inconsistencies found.")
    
    # Generate configurations if requested
    if args.generate:
        print(f"\nGenerating language-specific configurations in {args.output_dir}...")
        generate_configs(unified_rules, args.output_dir)
        print("Configuration files generated successfully.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 