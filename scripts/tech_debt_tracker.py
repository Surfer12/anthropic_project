#!/usr/bin/env python
"""
Technical Debt Tracker

This script analyzes code for TODO comments and other technical debt markers,
categorizes them, and generates a prioritized report based on a scoring matrix.

Usage:
    python tech_debt_tracker.py [--export FORMAT] [path]
"""

import argparse
import os
import re
import json
import csv
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any


class DebtCategory(Enum):
    """Categories of technical debt."""
    PERFORMANCE = "performance"
    SECURITY = "security"
    ARCHITECTURE = "architecture"
    CORRECTNESS = "correctness"
    USABILITY = "usability"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    MAINTAINABILITY = "maintainability"
    UNKNOWN = "unknown"


class DebtPriority(Enum):
    """Priority levels for technical debt items."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    TRIVIAL = "trivial"
    UNKNOWN = "unknown"


@dataclass
class DebtItem:
    """Represents a technical debt item."""
    file_path: str
    line_number: int
    content: str
    category: DebtCategory = DebtCategory.UNKNOWN
    priority: DebtPriority = DebtPriority.UNKNOWN
    ticket: Optional[str] = None
    estimated_effort: Optional[str] = None
    score: float = 0.0


def extract_debt_items(file_path: str) -> List[DebtItem]:
    """Extract technical debt markers from a file."""
    debt_items = []
    
    # Define regex patterns
    todo_pattern = re.compile(r'#\s*TODO:?\s*(.*)', re.IGNORECASE)
    fixme_pattern = re.compile(r'#\s*FIXME:?\s*(.*)', re.IGNORECASE)
    hack_pattern = re.compile(r'#\s*HACK:?\s*(.*)', re.IGNORECASE)
    
    # Special pattern for enhanced TODO format with metadata
    enhanced_todo_pattern = re.compile(
        r'#\s*TODO\[([^\]]+)\]:?\s*(.*)', re.IGNORECASE
    )
    
    # Pattern for ticket references
    ticket_pattern = re.compile(r'([A-Z]+-\d+)')
    
    # Pattern for estimated effort
    effort_pattern = re.compile(r'(\d+[dhwm])')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines):
            line_number = i + 1
            content = line.strip()
            
            # Check for enhanced TODO format first
            enhanced_match = enhanced_todo_pattern.search(content)
            if enhanced_match:
                metadata = enhanced_match.group(1)
                message = enhanced_match.group(2)
                
                # Extract priority and category from metadata
                category = DebtCategory.UNKNOWN
                priority = DebtPriority.UNKNOWN
                
                for item in metadata.split(','):
                    key_value = item.strip().split(':')
                    if len(key_value) == 2:
                        key, value = key_value
                        if key.upper() == 'PRIORITY':
                            try:
                                priority = DebtPriority(value.lower())
                            except ValueError:
                                pass
                        elif key.upper() == 'CATEGORY':
                            try:
                                category = DebtCategory(value.lower())
                            except ValueError:
                                pass
                
                # Extract ticket if present
                ticket_match = ticket_pattern.search(message)
                ticket = ticket_match.group(1) if ticket_match else None
                
                # Extract estimated effort if present
                effort_match = effort_pattern.search(message)
                estimated_effort = effort_match.group(1) if effort_match else None
                
                debt_items.append(DebtItem(
                    file_path=file_path,
                    line_number=line_number,
                    content=content,
                    category=category,
                    priority=priority,
                    ticket=ticket,
                    estimated_effort=estimated_effort
                ))
                continue
            
            # Check for standard formats
            for pattern, default_priority in [
                (todo_pattern, DebtPriority.MEDIUM),
                (fixme_pattern, DebtPriority.HIGH),
                (hack_pattern, DebtPriority.HIGH)
            ]:
                match = pattern.search(content)
                if match:
                    message = match.group(1)
                    
                    # Extract ticket if present
                    ticket_match = ticket_pattern.search(message)
                    ticket = ticket_match.group(1) if ticket_match else None
                    
                    # Extract estimated effort if present
                    effort_match = effort_pattern.search(message)
                    estimated_effort = effort_match.group(1) if effort_match else None
                    
                    # Infer category from content
                    category = infer_category(message)
                    
                    debt_items.append(DebtItem(
                        file_path=file_path,
                        line_number=line_number,
                        content=content,
                        category=category,
                        priority=default_priority,
                        ticket=ticket,
                        estimated_effort=estimated_effort
                    ))
                    break
    
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
    
    return debt_items


def infer_category(message: str) -> DebtCategory:
    """Infer debt category from the message content."""
    message_lower = message.lower()
    
    # Keywords for different categories
    category_keywords = {
        DebtCategory.PERFORMANCE: [
            'performance', 'optimize', 'efficiency', 'slow', 'fast', 'speed',
            'latency', 'throughput', 'memory', 'cpu', 'resource'
        ],
        DebtCategory.SECURITY: [
            'security', 'vulnerability', 'auth', 'encrypt', 'decrypt', 'hash',
            'sensitive', 'injection', 'xss', 'csrf', 'sanitize'
        ],
        DebtCategory.ARCHITECTURE: [
            'architecture', 'design', 'structure', 'refactor', 'pattern',
            'dependency', 'coupling', 'cohesion', 'interface', 'abstraction'
        ],
        DebtCategory.CORRECTNESS: [
            'bug', 'fix', 'issue', 'incorrect', 'error', 'fault', 'defect',
            'wrong', 'broken', 'logic', 'calculation'
        ],
        DebtCategory.USABILITY: [
            'usability', 'ux', 'ui', 'user', 'experience', 'interaction',
            'interface', 'accessibility', 'a11y', 'workflow'
        ],
        DebtCategory.DOCUMENTATION: [
            'document', 'doc', 'comment', 'explain', 'describe', 'readme',
            'wiki', 'guide', 'tutorial', 'instruction'
        ],
        DebtCategory.TESTING: [
            'test', 'coverage', 'assert', 'verify', 'validation', 'check',
            'mock', 'stub', 'unit', 'integration', 'e2e', 'spec'
        ],
        DebtCategory.MAINTAINABILITY: [
            'clean', 'readability', 'maintainable', 'technical debt', 'complex',
            'simplify', 'hardcoded', 'magic number', 'duplication'
        ]
    }
    
    # Check for each category
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in message_lower:
                return category
    
    return DebtCategory.UNKNOWN


def calculate_score(debt_item: DebtItem) -> float:
    """Calculate priority score based on the prioritization matrix."""
    # Base weights for different factors
    weights = {
        'category': 0.35,  # Performance issues weighted higher
        'has_ticket': 0.25,  # Items with tickets are more actionable
        'has_effort': 0.25,  # Items with effort estimates are more actionable
        'priority': 0.15,  # Explicit priority
    }
    
    # Score for category (performance and security highest)
    category_scores = {
        DebtCategory.PERFORMANCE: 10,
        DebtCategory.SECURITY: 10,
        DebtCategory.CORRECTNESS: 8,
        DebtCategory.ARCHITECTURE: 7,
        DebtCategory.MAINTAINABILITY: 6,
        DebtCategory.TESTING: 5,
        DebtCategory.USABILITY: 4,
        DebtCategory.DOCUMENTATION: 3,
        DebtCategory.UNKNOWN: 1,
    }
    
    # Score for priority
    priority_scores = {
        DebtPriority.CRITICAL: 10,
        DebtPriority.HIGH: 8,
        DebtPriority.MEDIUM: 5,
        DebtPriority.LOW: 3,
        DebtPriority.TRIVIAL: 1,
        DebtPriority.UNKNOWN: 3,  # Default is medium
    }
    
    # Calculate scores for each factor
    category_score = category_scores.get(debt_item.category, 1) * weights['category']
    priority_score = priority_scores.get(debt_item.priority, 3) * weights['priority']
    ticket_score = 10 * weights['has_ticket'] if debt_item.ticket else 0
    effort_score = 10 * weights['has_effort'] if debt_item.estimated_effort else 0
    
    # Calculate total score (0-10 scale)
    total_score = category_score + priority_score + ticket_score + effort_score
    normalized_score = min(10, total_score)
    
    return normalized_score


def scan_directory(directory: str) -> List[DebtItem]:
    """Recursively scan a directory for files and extract technical debt items."""
    debt_items = []
    
    # Define file extensions to check
    extensions = {'.py', '.java', '.mojo', '.c', '.cpp', '.h', '.hpp', '.js', '.ts', '.jsx', '.tsx'}
    
    for root, _, files in os.walk(directory):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext in extensions:
                file_path = os.path.join(root, file)
                debt_items.extend(extract_debt_items(file_path))
    
    return debt_items


def generate_report(debt_items: List[DebtItem]) -> None:
    """Generate a report of technical debt items."""
    if not debt_items:
        print("No technical debt items found.")
        return
    
    # Sort by score (descending)
    debt_items.sort(key=lambda x: x.score, reverse=True)
    
    # Group by category
    by_category = {}
    for item in debt_items:
        category = item.category.value
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(item)
    
    # Print summary
    total = len(debt_items)
    print(f"\nFound {total} technical debt items")
    
    print("\nTop 10 highest priority items:")
    for i, item in enumerate(debt_items[:10]):
        rel_path = os.path.relpath(item.file_path)
        ticket_info = f" [{item.ticket}]" if item.ticket else ""
        effort_info = f" ({item.estimated_effort})" if item.estimated_effort else ""
        priority_info = f"[{item.priority.value.upper()}]" if item.priority != DebtPriority.UNKNOWN else ""
        
        print(f"{i+1}. {rel_path}:{item.line_number}{ticket_info}{effort_info} {priority_info}")
        print(f"   {item.content.strip()}")
        print(f"   Score: {item.score:.1f}, Category: {item.category.value}")
        print()
    
    print("\nBreakdown by category:")
    for category, items in by_category.items():
        avg_score = sum(item.score for item in items) / len(items)
        print(f"  {category}: {len(items)} items (avg score: {avg_score:.1f})")


def export_to_json(debt_items: List[DebtItem], output_file: str) -> None:
    """Export debt items to a JSON file."""
    # Convert to serializable format
    serializable_items = []
    for item in debt_items:
        serializable_item = {
            'file_path': item.file_path,
            'line_number': item.line_number,
            'content': item.content,
            'category': item.category.value,
            'priority': item.priority.value,
            'ticket': item.ticket,
            'estimated_effort': item.estimated_effort,
            'score': item.score
        }
        serializable_items.append(serializable_item)
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'generated_at': datetime.now().isoformat(),
            'total_items': len(debt_items),
            'items': serializable_items
        }, f, indent=2)
    
    print(f"Exported {len(debt_items)} items to {output_file}")


def export_to_csv(debt_items: List[DebtItem], output_file: str) -> None:
    """Export debt items to a CSV file."""
    # Define fields
    fields = [
        'file_path', 'line_number', 'content', 'category', 
        'priority', 'ticket', 'estimated_effort', 'score'
    ]
    
    # Prepare rows
    rows = []
    for item in debt_items:
        row = {
            'file_path': item.file_path,
            'line_number': item.line_number,
            'content': item.content,
            'category': item.category.value,
            'priority': item.priority.value,
            'ticket': item.ticket or '',
            'estimated_effort': item.estimated_effort or '',
            'score': f"{item.score:.1f}"
        }
        rows.append(row)
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Exported {len(debt_items)} items to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Track and prioritize technical debt")
    parser.add_argument("path", nargs="?", default=".", help="Path to analyze")
    parser.add_argument("--export", choices=["json", "csv"], help="Export format")
    parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    path = args.path
    if not os.path.exists(path):
        print(f"Error: Path {path} does not exist")
        return 1
    
    # Scan for debt items
    if os.path.isfile(path):
        debt_items = extract_debt_items(path)
    else:
        debt_items = scan_directory(path)
    
    # Calculate scores
    for item in debt_items:
        item.score = calculate_score(item)
    
    # Generate report
    generate_report(debt_items)
    
    # Export if requested
    if args.export:
        output_file = args.output
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"tech_debt_{timestamp}.{args.export}"
        
        if args.export == "json":
            export_to_json(debt_items, output_file)
        elif args.export == "csv":
            export_to_csv(debt_items, output_file)
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 