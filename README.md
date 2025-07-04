# Multilingual Genetics Website - Organized Structure

## Overview
This repository contains a multilingual educational website about genetics and DNA research, focusing on "Scientific Adam and Scientific Eve" content. The codebase has been reorganized for better maintainability and clarity.

## New Directory Structure

```
├── src/                    # Main source code
│   ├── pages/             # All HTML pages organized by language/type
│   │   ├── english/       # English content (ENT*.html, T*.html, etc.)
│   │   ├── chinese/       # Chinese Traditional content (CHT*.html)
│   │   ├── bilingual/     # Chinese-English bilingual content (CH-EN*.html)
│   │   └── shared/        # Shared pages (index, welcome, etc.)
│   └── assets/            # All assets and supporting files
│       ├── images/        # Standalone image files (JPG, PNG, GIF)
│       └── shared/        # Shared assets, CSS, and utility directories
├── scripts/               # Python utility scripts
├── docs/                  # Documentation and reference materials
├── backups/               # Backup files and legacy content
├── temp/                  # Temporary and corrupted files
├── vercel.json           # Deployment configuration
└── package.json          # Project metadata

```

## Content Organization

### Language-Specific Pages
- **English Pages**: Located in `src/pages/english/`
  - ENT series (ENT1-P1.html through ENT6-P3.html)
  - T series (T4-P1.html through T18E-7HUMAN.html)
  - Educational content (ENGLISH.html, CONTACT.html, DUTY series, etc.)
  - Each page has associated `*_files` directories containing assets

- **Chinese Pages**: Located in `src/pages/chinese/`
  - CHT series (CHT1-P1.html through CHT10-P4.html)
  - Each page has associated `*_files` directories containing assets

- **Bilingual Pages**: Located in `src/pages/bilingual/`
  - CH-EN series (CH-EN7-P1.html through CH-EN11-P4.html)
  - Combined Chinese-English content

- **Shared Pages**: Located in `src/pages/shared/`
  - Index files (index.html, indexEN.html, etc.)
  - Welcome and informational pages
  - General content files (.htm files)

### Assets
- **Images**: All standalone images moved to `src/assets/images/`
- **Shared Assets**: CSS, configuration files, and utility directories in `src/assets/shared/`

### Utility Scripts
Located in `scripts/` directory:
- `update_filenames.py`: Script to handle Chinese filename encoding issues
- `test_chinese_encodings.py`: Testing script for character encoding
- `test_specific_file.py`: File-specific testing utilities
- `recover_index_html.py`: Recovery utility for index files
- `deploy.sh`: Deployment script

## Key Features

### Multilingual Support
- Traditional Chinese (CHT)
- English (ENT)
- Bilingual Chinese-English (CH-EN)

### Content Topics
- Scientific Adam and Scientific Eve research
- DNA coding and genetics
- Educational materials and tutorials
- Video content and multimedia resources

### Technical Notes
- Built for static hosting (Vercel configuration included)
- Legacy Microsoft Word HTML output (some files retain Word-specific formatting)
- Character encoding issues handled by utility scripts
- Asset directories follow consistent naming patterns

## Development

### File Naming Conventions
- **English content**: `ENT#-P#.html` (where # represents chapter/page numbers)
- **Chinese content**: `CHT#-P#.html`
- **Bilingual content**: `CH-EN#-P#.html`
- **Asset directories**: `[filename]_files/` (matches the HTML file name)

### Character Encoding
This project deals with Chinese character encoding issues. Use the scripts in the `scripts/` directory to handle filename conversions and encoding problems.

## Deployment
The site is configured for Vercel deployment using the included `vercel.json` configuration file.

## Historical Note
This reorganization was performed to improve the maintainability of a multilingual educational genetics website that was previously organized with all files in the root directory. The new structure separates content by language and type while preserving all original functionality.