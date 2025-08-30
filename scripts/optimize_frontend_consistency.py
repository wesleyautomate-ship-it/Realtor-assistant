#!/usr/bin/env python3
"""
Frontend Consistency Optimization Script
Ensures all React components have consistent UX enhancements applied.
"""

import os
import re
from pathlib import Path

def check_component_consistency(file_path):
    """Check if a component has all the required UX enhancements."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # Check for required imports
    required_imports = [
        'useMediaQuery',
        'useTheme', 
        'Stack',
        'Skeleton',
        'Fade',
        'Grow'
    ]
    
    missing_imports = []
    for import_name in required_imports:
        if import_name not in content:
            missing_imports.append(import_name)
    
    if missing_imports:
        issues.append(f"Missing imports: {', '.join(missing_imports)}")
    
    # Check for responsive hooks
    if 'useMediaQuery' not in content and 'useTheme' not in content:
        issues.append("Missing responsive hooks (useMediaQuery, useTheme)")
    
    # Check for theme-based spacing
    if 'theme.spacing(' not in content and 'sx={{' in content:
        issues.append("Hardcoded spacing values found - should use theme.spacing()")
    
    # Check for loading states
    if 'CircularProgress' in content and 'Skeleton' not in content:
        issues.append("Using CircularProgress instead of Skeleton for content loading")
    
    # Check for animations
    if 'Fade' not in content and 'Grow' not in content:
        issues.append("Missing transition animations (Fade, Grow)")
    
    return issues

def optimize_component(file_path):
    """Apply consistent optimizations to a component."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Add missing imports if needed
    if 'useMediaQuery' not in content and '@mui/material' in content:
        # Find the @mui/material import line
        import_match = re.search(r'from \'@mui/material\';', content)
        if import_match:
            # Add responsive imports
            responsive_imports = [
                'useMediaQuery',
                'useTheme',
                'Stack', 
                'Skeleton',
                'Fade',
                'Grow',
                'Divider'
            ]
            
            # Get existing imports
            material_import_match = re.search(r'import \{([^}]+)\} from \'@mui/material\';', content)
            if material_import_match:
                existing_imports = [imp.strip() for imp in material_import_match.group(1).split(',')]
                
                # Add missing imports
                for imp in responsive_imports:
                    if imp not in existing_imports:
                        existing_imports.append(imp)
                
                # Replace the import line
                new_import_line = f"import {{\n  {',\n  '.join(existing_imports)}\n}} from '@mui/material';"
                content = re.sub(r'import \{[^}]+\} from \'@mui/material\';', new_import_line, content)
    
    # Add responsive hooks if missing
    if 'useMediaQuery' not in content and 'const ' in content:
        # Find the first const declaration
        const_match = re.search(r'const (\w+) = \(\) => {', content)
        if const_match:
            component_name = const_match.group(1)
            
            # Add responsive hooks after the component declaration
            responsive_hooks = f"""  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isSmallScreen = useMediaQuery(theme.breakpoints.down('sm'));
  
  """
            
            # Insert after the component declaration
            content = re.sub(
                r'(const \w+ = \(\) => {)',
                r'\1\n' + responsive_hooks,
                content,
                count=1
            )
    
    # Replace hardcoded spacing with theme-based spacing
    spacing_patterns = [
        (r'sx={{ mb: (\d+) }}', r'sx={{ mb: theme.spacing(\1) }}'),
        (r'sx={{ p: (\d+) }}', r'sx={{ p: theme.spacing(\1) }}'),
        (r'sx={{ px: (\d+) }}', r'sx={{ px: theme.spacing(\1) }}'),
        (r'sx={{ py: (\d+) }}', r'sx={{ py: theme.spacing(\1) }}'),
        (r'sx={{ mt: (\d+) }}', r'sx={{ mt: theme.spacing(\1) }}'),
        (r'sx={{ mb: (\d+) }}', r'sx={{ mb: theme.spacing(\1) }}'),
        (r'sx={{ ml: (\d+) }}', r'sx={{ ml: theme.spacing(\1) }}'),
        (r'sx={{ mr: (\d+) }}', r'sx={{ mr: theme.spacing(\1) }}'),
    ]
    
    for pattern, replacement in spacing_patterns:
        content = re.sub(pattern, replacement, content)
    
    # Replace CircularProgress with Skeleton where appropriate
    if 'CircularProgress' in content and 'loading' in content.lower():
        # This is a complex replacement that needs manual review
        pass
    
    return content != original_content, content

def main():
    """Main function to check and optimize all frontend components."""
    frontend_dir = Path("frontend/src")
    
    # Components to check
    component_files = [
        "pages/Dashboard.jsx",
        "pages/Properties.jsx", 
        "pages/Chat.jsx",
        "pages/LoginPage.jsx",
        "pages/AdminFilesNew.jsx",
        "components/Sidebar.jsx",
        "components/ErrorBoundary.jsx",
        "components/ProtectedRoute.jsx",
        "layouts/MainLayout.jsx"
    ]
    
    print("🔍 Checking frontend component consistency...")
    print("=" * 60)
    
    all_issues = []
    optimized_files = []
    
    for component_file in component_files:
        file_path = frontend_dir / component_file
        
        if not file_path.exists():
            print(f"❌ File not found: {component_file}")
            continue
        
        print(f"\n📁 Checking: {component_file}")
        
        # Check for issues
        issues = check_component_consistency(file_path)
        
        if issues:
            print(f"  ⚠️  Issues found:")
            for issue in issues:
                print(f"    - {issue}")
            all_issues.extend([f"{component_file}: {issue}" for issue in issues])
            
            # Try to optimize
            was_optimized, optimized_content = optimize_component(file_path)
            if was_optimized:
                print(f"  ✅ Auto-optimized")
                optimized_files.append(component_file)
                # Write back the optimized content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(optimized_content)
        else:
            print(f"  ✅ All good!")
    
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"  - Files checked: {len(component_files)}")
    print(f"  - Issues found: {len(all_issues)}")
    print(f"  - Files optimized: {len(optimized_files)}")
    
    if all_issues:
        print(f"\n⚠️  Issues that need manual attention:")
        for issue in all_issues:
            print(f"  - {issue}")
    
    if optimized_files:
        print(f"\n✅ Successfully optimized files:")
        for file in optimized_files:
            print(f"  - {file}")
    
    print(f"\n🎯 Frontend consistency check complete!")

if __name__ == "__main__":
    main()
