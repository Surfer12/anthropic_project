#!/usr/bin/env python3
"""
Exemption Analyzer

This script analyzes, tracks, and reports on linting rule exemptions across the codebase.
It provides functionality to scan for exemptions, generate reports, and check for expired exemptions.

Features:
- Scans codebase for linting rule exemptions
- Tracks exemption metadata and expiration
- Generates detailed reports
- Integrates with CI/CD pipelines
- Provides metrics and analytics
"""

import argparse
import datetime
import json
import logging
import os
import re
import sys
from dataclasses import asdict, dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import yaml
from rich.console import Console
from rich.table import Table

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class ExemptionType(Enum):
    """Types of linting rule exemptions."""
    NOQA = auto()
    TYPE_IGNORE = auto()
    FMT_OFF = auto()
    SUPPRESS_WARNINGS = auto()
    NOLINT = auto()
    CLANG_FORMAT_OFF = auto()

@dataclass
class ExemptionLocation:
    """Location information for an exemption."""
    file: str
    start_line: int
    end_line: Optional[int] = None
    
@dataclass
class Exemption:
    """Represents a single linting rule exemption."""
    rule_id: str
    location: ExemptionLocation
    exemption_type: ExemptionType
    reason: Optional[str]
    approved_by: Optional[str]
    approved_date: Optional[datetime.date]
    review_date: Optional[datetime.date]
    ticket: Optional[str]
    is_active: bool = True

class ExemptionPattern:
    """Patterns for detecting exemptions in different languages."""
    PYTHON_NOQA = re.compile(r"#\s*noqa:\s*([A-Z][0-9]{3}(?:,\s*[A-Z][0-9]{3})*)")
    PYTHON_TYPE_IGNORE = re.compile(r"#\s*type:\s*ignore\[([^\]]+)\]")
    PYTHON_FMT_OFF = re.compile(r"#\s*fmt:\s*(off|on)")
    JAVA_SUPPRESS = re.compile(r"@SuppressWarnings\([\"']([^\"']+)[\"']\)")
    CPP_NOLINT = re.compile(r"//\s*NOLINT\(([^)]+)\)")
    CPP_FORMAT = re.compile(r"/\*\s*clang-format\s+(off|on)\s*\*/")

class ExemptionAnalyzer:
    """Analyzes and tracks linting rule exemptions in the codebase."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.exemptions: List[Exemption] = []
        self.registry_path = workspace_root / ".linting" / "exemption_registry.yaml"
        self.console = Console()
        
    def load_registry(self) -> None:
        """Load existing exemption registry."""
        if not self.registry_path.exists():
            logger.info("No existing exemption registry found")
            return
            
        try:
            with open(self.registry_path) as f:
                data = yaml.safe_load(f)
                if not data:
                    return
                    
                for entry in data.get("exemptions", []):
                    location = ExemptionLocation(
                        file=entry["file"],
                        start_line=entry["lines"][0],
                        end_line=entry["lines"][-1] if len(entry["lines"]) > 1 else None
                    )
                    
                    self.exemptions.append(Exemption(
                        rule_id=entry["rule_id"],
                        location=location,
                        exemption_type=ExemptionType[entry["type"]],
                        reason=entry.get("reason"),
                        approved_by=entry.get("approved_by"),
                        approved_date=datetime.datetime.strptime(entry["approved_date"], "%Y-%m-%d").date()
                        if "approved_date" in entry else None,
                        review_date=datetime.datetime.strptime(entry["review_date"], "%Y-%m-%d").date()
                        if "review_date" in entry else None,
                        ticket=entry.get("ticket"),
                        is_active=entry.get("is_active", True)
                    ))
        except Exception as e:
            logger.error(f"Error loading exemption registry: {e}")
            raise
            
    def save_registry(self) -> None:
        """Save current exemptions to registry."""
        try:
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "exemptions": [
                    {
                        "rule_id": e.rule_id,
                        "file": e.location.file,
                        "lines": [e.location.start_line] if e.location.end_line is None 
                               else list(range(e.location.start_line, e.location.end_line + 1)),
                        "type": e.exemption_type.name,
                        "reason": e.reason,
                        "approved_by": e.approved_by,
                        "approved_date": e.approved_date.strftime("%Y-%m-%d") if e.approved_date else None,
                        "review_date": e.review_date.strftime("%Y-%m-%d") if e.review_date else None,
                        "ticket": e.ticket,
                        "is_active": e.is_active
                    }
                    for e in self.exemptions
                ]
            }
            
            with open(self.registry_path, "w") as f:
                yaml.safe_dump(data, f, sort_keys=False)
                
        except Exception as e:
            logger.error(f"Error saving exemption registry: {e}")
            raise
            
    def scan_file(self, file_path: Path) -> List[Exemption]:
        """Scan a single file for exemptions."""
        exemptions: List[Exemption] = []
        
        try:
            with open(file_path) as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines, 1):
                # Python exemptions
                if file_path.suffix in {".py", ".pyi"}:
                    if match := ExemptionPattern.PYTHON_NOQA.search(line):
                        for rule in match.group(1).split(","):
                            exemptions.append(Exemption(
                                rule_id=rule.strip(),
                                location=ExemptionLocation(
                                    file=str(file_path.relative_to(self.workspace_root)),
                                    start_line=i
                                ),
                                exemption_type=ExemptionType.NOQA,
                                reason=None,
                                approved_by=None,
                                approved_date=None,
                                review_date=None,
                                ticket=None
                            ))
                            
                    if match := ExemptionPattern.PYTHON_TYPE_IGNORE.search(line):
                        exemptions.append(Exemption(
                            rule_id=f"type-ignore[{match.group(1)}]",
                            location=ExemptionLocation(
                                file=str(file_path.relative_to(self.workspace_root)),
                                start_line=i
                            ),
                            exemption_type=ExemptionType.TYPE_IGNORE,
                            reason=None,
                            approved_by=None,
                            approved_date=None,
                            review_date=None,
                            ticket=None
                        ))
                        
                    if match := ExemptionPattern.PYTHON_FMT_OFF.search(line):
                        if match.group(1) == "off":
                            exemptions.append(Exemption(
                                rule_id="fmt-off",
                                location=ExemptionLocation(
                                    file=str(file_path.relative_to(self.workspace_root)),
                                    start_line=i
                                ),
                                exemption_type=ExemptionType.FMT_OFF,
                                reason=None,
                                approved_by=None,
                                approved_date=None,
                                review_date=None,
                                ticket=None
                            ))
                            
                # Java exemptions
                elif file_path.suffix in {".java"}:
                    if match := ExemptionPattern.JAVA_SUPPRESS.search(line):
                        exemptions.append(Exemption(
                            rule_id=match.group(1),
                            location=ExemptionLocation(
                                file=str(file_path.relative_to(self.workspace_root)),
                                start_line=i
                            ),
                            exemption_type=ExemptionType.SUPPRESS_WARNINGS,
                            reason=None,
                            approved_by=None,
                            approved_date=None,
                            review_date=None,
                            ticket=None
                        ))
                        
                # C++ exemptions
                elif file_path.suffix in {".cpp", ".hpp", ".cc", ".h"}:
                    if match := ExemptionPattern.CPP_NOLINT.search(line):
                        exemptions.append(Exemption(
                            rule_id=match.group(1),
                            location=ExemptionLocation(
                                file=str(file_path.relative_to(self.workspace_root)),
                                start_line=i
                            ),
                            exemption_type=ExemptionType.NOLINT,
                            reason=None,
                            approved_by=None,
                            approved_date=None,
                            review_date=None,
                            ticket=None
                        ))
                        
                    if match := ExemptionPattern.CPP_FORMAT.search(line):
                        if match.group(1) == "off":
                            exemptions.append(Exemption(
                                rule_id="clang-format-off",
                                location=ExemptionLocation(
                                    file=str(file_path.relative_to(self.workspace_root)),
                                    start_line=i
                                ),
                                exemption_type=ExemptionType.CLANG_FORMAT_OFF,
                                reason=None,
                                approved_by=None,
                                approved_date=None,
                                review_date=None,
                                ticket=None
                            ))
                            
        except Exception as e:
            logger.error(f"Error scanning file {file_path}: {e}")
            
        return exemptions
        
    def scan_workspace(self) -> None:
        """Scan entire workspace for exemptions."""
        for root, _, files in os.walk(self.workspace_root):
            if ".git" in root or "node_modules" in root:
                continue
                
            root_path = Path(root)
            for file in files:
                if file.endswith((".py", ".pyi", ".java", ".cpp", ".hpp", ".cc", ".h")):
                    file_path = root_path / file
                    self.exemptions.extend(self.scan_file(file_path))
                    
    def generate_report(self) -> None:
        """Generate a detailed report of exemptions."""
        # Summary table
        summary = Table(title="Exemption Summary")
        summary.add_column("Category", style="cyan")
        summary.add_column("Count", style="magenta")
        
        type_counts = {}
        for exemption in self.exemptions:
            type_counts[exemption.exemption_type.name] = type_counts.get(exemption.exemption_type.name, 0) + 1
            
        for type_name, count in type_counts.items():
            summary.add_row(type_name, str(count))
            
        self.console.print(summary)
        
        # Detailed table
        details = Table(title="Exemption Details")
        details.add_column("File", style="cyan")
        details.add_column("Line", style="magenta")
        details.add_column("Rule", style="green")
        details.add_column("Type", style="yellow")
        details.add_column("Review Date", style="blue")
        
        for exemption in sorted(self.exemptions, key=lambda e: (e.location.file, e.location.start_line)):
            details.add_row(
                exemption.location.file,
                str(exemption.location.start_line),
                exemption.rule_id,
                exemption.exemption_type.name,
                exemption.review_date.strftime("%Y-%m-%d") if exemption.review_date else "N/A"
            )
            
        self.console.print(details)
        
    def check_expired(self) -> List[Exemption]:
        """Check for expired exemptions."""
        today = datetime.date.today()
        expired = []
        
        for exemption in self.exemptions:
            if exemption.review_date and exemption.review_date < today:
                expired.append(exemption)
                
        if expired:
            table = Table(title="Expired Exemptions")
            table.add_column("File", style="cyan")
            table.add_column("Line", style="magenta")
            table.add_column("Rule", style="green")
            table.add_column("Review Date", style="red")
            
            for exemption in expired:
                table.add_row(
                    exemption.location.file,
                    str(exemption.location.start_line),
                    exemption.rule_id,
                    exemption.review_date.strftime("%Y-%m-%d") if exemption.review_date else "N/A"
                )
                
            self.console.print(table)
            
        return expired
        
    def export_json(self, output_path: Path) -> None:
        """Export exemptions to JSON format."""
        data = {
            "exemptions": [asdict(e) for e in self.exemptions],
            "generated_at": datetime.datetime.now().isoformat()
        }
        
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2, default=str)
            
def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Analyze and track linting rule exemptions")
    parser.add_argument("--scan", action="store_true", help="Scan workspace for exemptions")
    parser.add_argument("--report", action="store_true", help="Generate exemption report")
    parser.add_argument("--check-expired", action="store_true", help="Check for expired exemptions")
    parser.add_argument("--export", type=str, help="Export exemptions to JSON file")
    
    args = parser.parse_args()
    
    try:
        workspace_root = Path.cwd()
        analyzer = ExemptionAnalyzer(workspace_root)
        
        if args.scan:
            analyzer.load_registry()
            analyzer.scan_workspace()
            analyzer.save_registry()
            logger.info("Workspace scan completed")
            
        if args.report:
            analyzer.load_registry()
            analyzer.generate_report()
            
        if args.check_expired:
            analyzer.load_registry()
            expired = analyzer.check_expired()
            if expired:
                logger.warning(f"Found {len(expired)} expired exemptions")
                sys.exit(1)
                
        if args.export:
            analyzer.load_registry()
            output_path = Path(args.export)
            analyzer.export_json(output_path)
            logger.info(f"Exemptions exported to {output_path}")
            
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    main() 