#!/usr/bin/env python
"""
Type System Refiner

This script analyzes Python code for type-ignore directives and suggests
improvements to eliminate them through proper typing approaches.

Usage:
    python type_system_refiner.py [--analyze-only] [--fix] [path]
"""

import argparse
import ast
import os
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


class IgnoreReason(Enum):
    """Categorization of type-ignore reasons."""
    FORWARD_REFERENCE = "forward_reference"
    OPTIONAL_IMPORT = "optional_import"
    OVERLOADED_METHOD = "overloaded_method"
    DYNAMIC_ATTRIBUTE = "dynamic_attribute"
    COMPLEX_TYPE = "complex_type"
    UNKNOWN = "unknown"


@dataclass
class TypeIgnore:
    """Represents a type-ignore directive in code."""
    file_path: str
    line_number: int
    code_line: str
    ignore_reason: IgnoreReason
    suggested_fix: Optional[str] = None


def extract_type_ignores(file_path: str) -> List[TypeIgnore]:
    """Extract type-ignore directives from a file."""
    type_ignores = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines):
            line_number = i + 1
            if '# type: ignore' in line:
                # Determine the reason for the type-ignore
                reason = classify_type_ignore(file_path, line, line_number, lines)
                type_ignores.append(TypeIgnore(
                    file_path=file_path,
                    line_number=line_number,
                    code_line=line.strip(),
                    ignore_reason=reason
                ))
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
    
    return type_ignores


def classify_type_ignore(file_path: str, line: str, line_number: int, 
                         all_lines: List[str]) -> IgnoreReason:
    """Classify the reason for a type-ignore directive."""
    # Extract additional context (previous and next lines)
    context = []
    start = max(0, line_number - 3)
    end = min(len(all_lines), line_number + 2)
    for i in range(start, end):
        context.append(all_lines[i])
    
    # Check for forward references
    if '"' in line or "'" in line:
        type_annotation = re.search(r'-> (.+?):', line)
        if type_annotation and ('"' in type_annotation.group(1) or "'" in type_annotation.group(1)):
            return IgnoreReason.FORWARD_REFERENCE
    
    # Check for method overrides
    if 'def __' in line or 'override' in line.lower():
        return IgnoreReason.OVERLOADED_METHOD
    
    # Check for dynamic attributes
    if '.__getattr__' in line or '.__setattr__' in line:
        return IgnoreReason.DYNAMIC_ATTRIBUTE
        
    # Check for optional imports or complex types
    for context_line in context:
        if 'import' in context_line and ('try:' in context_line or 'except' in context_line):
            return IgnoreReason.OPTIONAL_IMPORT
    
    # Default to unknown
    return IgnoreReason.UNKNOWN


def suggest_fix(type_ignore: TypeIgnore) -> str:
    """Suggest a fix for a type-ignore directive based on its classification."""
    if type_ignore.ignore_reason == IgnoreReason.FORWARD_REFERENCE:
        return """
# Add at the top of the file:
from __future__ import annotations
"""
    elif type_ignore.ignore_reason == IgnoreReason.OPTIONAL_IMPORT:
        return """
# Use TYPE_CHECKING for conditional imports:
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from module import OptionalClass
"""
    elif type_ignore.ignore_reason == IgnoreReason.DYNAMIC_ATTRIBUTE:
        return """
# Define a Protocol for the expected interface:
from typing import Protocol, runtime_checkable

@runtime_checkable
class HasAttribute(Protocol):
    def __getattr__(self, name: str) -> Any: ...
"""
    elif type_ignore.ignore_reason == IgnoreReason.OVERLOADED_METHOD:
        return """
# Use @overload for multiple method signatures:
from typing import overload

@overload
def method(self, arg: int) -> int: ...

@overload
def method(self, arg: str) -> str: ...

def method(self, arg):
    # Implementation
"""
    else:
        return "# Consider creating a .pyi stub file for this module"


def fix_type_ignores(type_ignores: List[TypeIgnore]) -> None:
    """Apply fixes for type-ignore directives."""
    # Group type ignores by file
    ignores_by_file = {}
    for ti in type_ignores:
        if ti.file_path not in ignores_by_file:
            ignores_by_file[ti.file_path] = []
        ignores_by_file[ti.file_path].append(ti)
    
    for file_path, file_ignores in ignores_by_file.items():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            modified = False
            
            # Check if we need to add imports
            add_future_annotations = any(ti.ignore_reason == IgnoreReason.FORWARD_REFERENCE 
                                         for ti in file_ignores)
            add_type_checking = any(ti.ignore_reason == IgnoreReason.OPTIONAL_IMPORT 
                                    for ti in file_ignores)
            add_protocol = any(ti.ignore_reason == IgnoreReason.DYNAMIC_ATTRIBUTE 
                               for ti in file_ignores)
            
            # Insert imports at the top of the file if needed
            if add_future_annotations or add_type_checking or add_protocol:
                import_lines = []
                if add_future_annotations:
                    import_lines.append("from __future__ import annotations\n")
                if add_type_checking:
                    import_lines.append("from typing import TYPE_CHECKING\n")
                if add_protocol:
                    import_lines.append("from typing import Protocol, runtime_checkable, Any\n")
                
                # Find the position to insert imports (after docstring, if any)
                insert_pos = 0
                in_docstring = False
                doc_string_delim = None
                
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    if i == 0 and stripped.startswith("#!"):
                        insert_pos = 1
                        continue
                    
                    if not in_docstring and (stripped.startswith('"""') or stripped.startswith("'''")):
                        in_docstring = True
                        doc_string_delim = stripped[:3]
                        if stripped.endswith(doc_string_delim) and len(stripped) > 3:
                            in_docstring = False
                            insert_pos = i + 1
                        continue
                    
                    if in_docstring and doc_string_delim and doc_string_delim in stripped:
                        in_docstring = False
                        insert_pos = i + 1
                        continue
                    
                    if not in_docstring and stripped and not stripped.startswith("#"):
                        insert_pos = i
                        break
                
                for line in reversed(import_lines):
                    lines.insert(insert_pos, line)
                modified = True
            
            # Create stub file if necessary
            stub_needed = any(ti.ignore_reason == IgnoreReason.UNKNOWN for ti in file_ignores)
            if stub_needed:
                stub_path = file_path.replace(".py", ".pyi")
                if not os.path.exists(stub_path):
                    with open(stub_path, 'w', encoding='utf-8') as f:
                        f.write(f"""# Type stubs for {os.path.basename(file_path)}
from typing import Any, Optional, List, Dict, Union

# Add precise type definitions here
""")
                    print(f"Created stub file: {stub_path}")
            
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                print(f"Modified {file_path}")
        
        except Exception as e:
            print(f"Error fixing {file_path}: {str(e)}")


def scan_directory(directory: str) -> List[TypeIgnore]:
    """Recursively scan a directory for Python files and extract type-ignore directives."""
    type_ignores = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                type_ignores.extend(extract_type_ignores(file_path))
    return type_ignores


def generate_report(type_ignores: List[TypeIgnore]) -> None:
    """Generate a report of type-ignore directives and suggested fixes."""
    if not type_ignores:
        print("No type-ignore directives found.")
        return
    
    total = len(type_ignores)
    reasons = {}
    for ti in type_ignores:
        reason = ti.ignore_reason.value
        if reason not in reasons:
            reasons[reason] = 0
        reasons[reason] += 1
    
    print(f"\nFound {total} type-ignore directives")
    print("\nBreakdown by reason:")
    for reason, count in reasons.items():
        print(f"  {reason}: {count} ({count/total*100:.1f}%)")
    
    print("\nSample issues:")
    shown = set()
    for reason in IgnoreReason:
        for ti in type_ignores:
            if ti.ignore_reason == reason and reason.value not in shown:
                rel_path = os.path.relpath(ti.file_path)
                print(f"\n{rel_path}:{ti.line_number}: {ti.code_line}")
                print(f"Reason: {reason.value}")
                print(f"Suggested fix:\n{suggest_fix(ti)}")
                shown.add(reason.value)
                break


def main():
    parser = argparse.ArgumentParser(description="Analyze and fix type-ignore directives")
    parser.add_argument("path", nargs="?", default=".", help="Path to analyze")
    parser.add_argument("--analyze-only", action="store_true", help="Only analyze, don't fix")
    parser.add_argument("--fix", action="store_true", help="Apply suggested fixes")
    
    args = parser.parse_args()
    
    path = args.path
    if not os.path.exists(path):
        print(f"Error: Path {path} does not exist")
        return 1
    
    if os.path.isfile(path) and path.endswith(".py"):
        type_ignores = extract_type_ignores(path)
    else:
        type_ignores = scan_directory(path)
    
    # Add suggested fixes
    for ti in type_ignores:
        ti.suggested_fix = suggest_fix(ti)
    
    generate_report(type_ignores)
    
    if args.fix and not args.analyze_only:
        print("\nApplying fixes...")
        fix_type_ignores(type_ignores)
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 