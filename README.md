# 📊 Report Parser

> Transform business reports into clean, segmented marketing lists

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Python CLI and web app to rapidly create formatted and filtered tables from .xlsx files, with automatic geographic segmentation into mailing lists.

📖 **[View Full Documentation](https://yourusername.github.io/utils/)**

## ✨ Features

- 🧹 **Data Cleaning** - Remove IDs, merge phone numbers, parse addresses
- 🗺️ **Regional Segmentation** - Split contacts into PNW, CA, and GG regions
- ⚡ **Dual Interface** - CLI and interactive Streamlit web app
- ✅ **Data Validation** - Automatic validation of cities, states, and zip codes
- 📤 **Multiple Outputs** - Single file or separate regional exports

## 🚀 Quick Start

### Installation

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### Configuration

Create a `.env` file:

```bash
BASE_DIRECTORY=C:\Path\To\Your\Downloads
```

### Usage

**Command Line:**
```bash
# Process all contacts
uv run python -m utils contacts

# Segment into mailing lists (PNW, CA, GG)
uv run python -m utils contacts --segment

# Process visits
uv run python -m utils visits
```

**Web Interface:**
```bash
uv run streamlit run app.py
```

Then open http://localhost:8501 in your browser.

## 🗺️ Mailing List Regions

Contacts are segmented into three geographic regions:

| Region | States | Description |
|--------|--------|-------------|
| **PNW** | WA, OR, WY, ID, MT | Pacific Northwest |
| **CA** | CA | California |
| **GG** | NM, NV, UT, CO, AZ, LA, TX, AR, OK | Golden Gate |

## 📋 Report Types

### Contacts

Processes contact exports for marketing list uploads:

**Input:** `Contact_*.xlsx` file

**Processing:**
- Removes database UUIDs/IDs
- Combines Phone and Mobile into single column
- Parses Business Address into City, State, Zip
- Validates location data (clears invalid entries)
- Filters to allowed states only
- Optional: Segments into three regional lists

**Output Columns:**
- Name
- Account Name
- Email
- Phone
- City
- State
- Zip

**Output Files:**
- Without segmentation: `Contact_Processed_*.xlsx`
- With segmentation: `Contact_PNW_*.xlsx`, `Contact_CA_*.xlsx`, `Contact_GG_*.xlsx`

### Visits

Processes visit reports:

**Input:** `Visit.zip` containing visit data

**Processing:**
- Extracts zip file
- Removes unnecessary columns
- Cleans visit data

## 🌐 Web Interface Features

The Streamlit app provides:

- 📁 **File Upload** - Upload files directly (no Downloads folder needed)
- 🔄 **Toggle Segmentation** - Enable/disable regional splitting
- 👀 **Live Preview** - See original and processed data
- ⬇️ **Individual Downloads** - Separate download buttons for each region
- 📊 **Summary Stats** - Contact counts per region

## 🛠️ Development

### Project Structure

```
utils/
├── app.py                    # Streamlit web interface
├── utils/
│   ├── __init__.py          # Package exports
│   ├── __main__.py          # CLI entry point
│   └── processors.py        # Shared processing logic
├── docs/
│   └── index.html           # GitHub Pages documentation
├── .env                      # Configuration (gitignored)
├── pyproject.toml
└── README.md
```

### Running Tests

```bash
uv run pytest
```

## 📊 Data Processing Pipeline

1. **Clean IDs** - Remove all UUID/ID columns
2. **Merge Phones** - Combine Phone & Mobile fields
3. **Parse Address** - Extract City, State, Zip
4. **Validate Data** - Check format rules
5. **Filter States** - Keep only allowed states
6. **Segment** *(optional)* - Split into PNW, CA, GG

## ✅ Validation Rules

- **City:** Must be >2 characters, no numbers
- **State:** Must be exactly 2 letters, in allowed list
- **Zip:** Must start with 5 digits

Invalid entries are cleared (set to blank) rather than left with bad data.

## 📝 Notes

- Original source files are preserved
- Processed files use `_Processed_` or region name suffix
- Business addresses with multiple segments (suite numbers, etc.) are handled correctly
- Invalid location data is cleared rather than propagated

## 🤝 Contributing

This is an internal tool. For questions or issues, contact the development team.

## 📄 License

MIT License - See LICENSE file for details

---

**[View Full Documentation](https://yourusername.github.io/utils/)** | Built with ❤️ for efficient contact list management
