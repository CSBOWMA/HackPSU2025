#!/usr/bin/env python3
"""
Upload all files from a directory to the assignments API.
Each file will be created as a separate assignment with metadata.
"""

import os
import sys
import json
import base64
import argparse
import mimetypes
from pathlib import Path
from datetime import datetime, timedelta
import requests
from typing import Optional, Dict, Any

# Default configuration
DEFAULT_API_BASE_URL = "https://YOUR_API_ENDPOINT/dev"
DEFAULT_USER_ID = "user123"

class AssignmentUploader:
    def __init__(self, api_base_url: str, user_id: str, class_id: Optional[str] = None):
        self.api_base_url = api_base_url.rstrip('/')
        self.user_id = user_id
        self.class_id = class_id or "default-class"
        self.class_name = "Imported Documents"
        
    def get_file_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from file."""
        file_stat = file_path.stat()
        file_type, _ = mimetypes.guess_type(str(file_path))
        
        return {
            'file_name': file_path.name,
            'file_size': file_stat.st_size,
            'file_type': file_type or 'application/octet-stream',
            'modified_time': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
        }
    
    def read_file_content(self, file_path: Path, file_type: str) -> tuple[str, Optional[str]]:
        """
        Read file content and determine encoding.
        Returns (content, encoding) where encoding is 'base64' or None for text.
        """
        # Text-based files
        text_types = [
            'text/', 'application/json', 'application/xml',
            'application/javascript', 'application/x-yaml'
        ]
        
        is_text = any(file_type.startswith(t) for t in text_types)
        
        if is_text:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return content, None
            except UnicodeDecodeError:
                # Fallback to binary if text decode fails
                pass
        
        # Binary files
        with open(file_path, 'rb') as f:
            binary_content = f.read()
            encoded_content = base64.b64encode(binary_content).decode('utf-8')
            return encoded_content, 'base64'
    
    def create_assignment(
        self,
        file_path: Path,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        status: str = 'pending',
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create an assignment with file upload."""
        
        metadata = self.get_file_metadata(file_path)
        
        # Read file content
        file_content, encoding = self.read_file_content(file_path, metadata['file_type'])
        
        # Prepare assignment data
        assignment_data = {
            'title': title or file_path.stem,
            'description': description or f"Uploaded from {file_path.name}",
            'class_id': self.class_id,
            'class_name': self.class_name,
            'due_date': due_date or (datetime.now() + timedelta(days=7)).isoformat(),
            'status': status,
            'notes': notes or f"File size: {metadata['file_size']} bytes\nModified: {metadata['modified_time']}",
            'file_content': file_content,
            'file_name': metadata['file_name'],
            'file_type': metadata['file_type']
        }
        
        if encoding:
            assignment_data['file_encoding'] = encoding
        
        # Make API request
        url = f"{self.api_base_url}/users/{self.user_id}/assignments"
        
        print(f"Uploading {file_path.name}... ", end='', flush=True)
        
        try:
            response = requests.post(
                url,
                json=assignment_data,
                headers={'Content-Type': 'application/json'},
                timeout=60
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"✓ Success (ID: {result.get('id', 'unknown')})")
                return result
            else:
                print(f"✗ Failed (Status: {response.status_code})")
                print(f"  Error: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Error: {str(e)}")
            return None
    
    def upload_directory(
        self,
        directory: Path,
        recursive: bool = False,
        file_extensions: Optional[list] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Upload all files from a directory."""
        
        if not directory.is_dir():
            raise ValueError(f"{directory} is not a directory")
        
        # Get all files
        if recursive:
            files = [f for f in directory.rglob('*') if f.is_file()]
        else:
            files = [f for f in directory.glob('*') if f.is_file()]
        
        # Filter by extensions if specified
        if file_extensions:
            files = [f for f in files if f.suffix.lower() in file_extensions]
        
        print(f"\nFound {len(files)} file(s) to upload")
        print(f"API Endpoint: {self.api_base_url}")
        print(f"User ID: {self.user_id}")
        print(f"Class ID: {self.class_id}")
        print("-" * 60)
        
        if dry_run:
            print("\n[DRY RUN MODE - No files will be uploaded]\n")
            for file_path in files:
                metadata = self.get_file_metadata(file_path)
                print(f"Would upload: {file_path.name}")
                print(f"  Type: {metadata['file_type']}")
                print(f"  Size: {metadata['file_size']} bytes")
            return {'dry_run': True, 'file_count': len(files)}
        
        # Upload files
        results = {
            'successful': [],
            'failed': [],
            'total': len(files)
        }
        
        for i, file_path in enumerate(files, 1):
            print(f"[{i}/{len(files)}] ", end='')
            
            result = self.create_assignment(file_path)
            
            if result:
                results['successful'].append({
                    'file': str(file_path),
                    'assignment_id': result.get('id'),
                    'title': result.get('title')
                })
            else:
                results['failed'].append(str(file_path))
        
        # Summary
        print("\n" + "=" * 60)
        print("UPLOAD SUMMARY")
        print("=" * 60)
        print(f"Total files: {results['total']}")
        print(f"Successful: {len(results['successful'])}")
        print(f"Failed: {len(results['failed'])}")
        
        if results['failed']:
            print("\nFailed uploads:")
            for failed_file in results['failed']:
                print(f"  - {failed_file}")
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description='Upload files from a directory to assignments API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload all files from a directory
  python upload_directory_to_assignments.py ./documents

  # Upload with custom API endpoint and user
  python upload_directory_to_assignments.py ./documents \\
    --api-url https://api.example.com/dev \\
    --user-id user456

  # Upload only PDF files recursively
  python upload_directory_to_assignments.py ./documents \\
    --recursive \\
    --extensions .pdf

  # Dry run (don't actually upload)
  python upload_directory_to_assignments.py ./documents --dry-run

  # Upload with custom class
  python upload_directory_to_assignments.py ./documents \\
    --class-id cs101 \\
    --class-name "Computer Science 101"
        """
    )
    
    parser.add_argument(
        'directory',
        type=str,
        help='Directory containing files to upload'
    )
    
    parser.add_argument(
        '--api-url',
        type=str,
        default=os.environ.get('API_BASE_URL', DEFAULT_API_BASE_URL),
        help='API base URL (default: from API_BASE_URL env var or hardcoded default)'
    )
    
    parser.add_argument(
        '--user-id',
        type=str,
        default=os.environ.get('USER_ID', DEFAULT_USER_ID),
        help='User ID (default: from USER_ID env var or hardcoded default)'
    )
    
    parser.add_argument(
        '--class-id',
        type=str,
        help='Class ID for assignments (default: "default-class")'
    )
    
    parser.add_argument(
        '--class-name',
        type=str,
        help='Class name for assignments (default: "Imported Documents")'
    )
    
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Upload files from subdirectories recursively'
    )
    
    parser.add_argument(
        '--extensions', '-e',
        nargs='+',
        help='Filter by file extensions (e.g., .pdf .txt .docx)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be uploaded without actually uploading'
    )
    
    parser.add_argument(
        '--output-json',
        type=str,
        help='Save results to JSON file'
    )
    
    args = parser.parse_args()
    
    # Validate directory
    directory = Path(args.directory)
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory", file=sys.stderr)
        sys.exit(1)
    
    # Create uploader
    uploader = AssignmentUploader(
        api_base_url=args.api_url,
        user_id=args.user_id,
        class_id=args.class_id
    )
    
    if args.class_name:
        uploader.class_name = args.class_name
    
    # Normalize extensions
    extensions = None
    if args.extensions:
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in args.extensions]
    
    # Upload files
    try:
        results = uploader.upload_directory(
            directory=directory,
            recursive=args.recursive,
            file_extensions=extensions,
            dry_run=args.dry_run
        )
        
        # Save results to JSON if requested
        if args.output_json and not args.dry_run:
            with open(args.output_json, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to: {args.output_json}")
        
        # Exit with error code if any uploads failed
        if results.get('failed'):
            sys.exit(1)
            
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
