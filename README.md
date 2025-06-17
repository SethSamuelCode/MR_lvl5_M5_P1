# MR_lvl5_M5_P1 - MongoDB Auction Item Data Seeder CLI

A command-line interface for managing auction item data in MongoDB. This tool provides secure credential management and comprehensive data operations for auction items.

## Features

- Secure credential storage using system keyring
- Single item addition
- Bulk import from JSON files
- Data retrieval and deletion
- Interactive setup for MongoDB connection

## Prerequisites

- Python 3.x
- MongoDB server (local or remote)
- Required Python packages:
  ```bash
  pip install -r requirements.txt
  ```

The following packages are required:
- typer
- pymongo
- keyring

## Initial Setup

Before using the tool, you need to configure your MongoDB connection settings:

```bash
python dataSeeder.py setup
```

You will be prompted for:
1. MongoDB connection string
2. Database name
3. Collection name

Your credentials will be stored securely in the system keyring and will not be saved in command history.

To view current settings without changing them:
```bash
python dataSeeder.py setup --getSettings
```

## Commands

### Add Single Item
```bash
python dataSeeder.py add TITLE DESCRIPTION START_PRICE RESERVE_PRICE
```

Adds a single auction item to the MongoDB collection.

**Arguments**:
* `TITLE`: The title of the auction item
* `DESCRIPTION`: A detailed description of the item
* `START_PRICE`: The starting bid price for the item
* `RESERVE_PRICE`: The minimum price that must be met for the item to be sold

**Example**:
```bash
python dataSeeder.py add "Vintage Watch" "A rare 1950s timepiece" 1000 1500
```

### Import From File
```bash
python dataSeeder.py import-file --file FILENAME
```

Bulk imports auction items from a JSON file. 

**Options**:
* `-f, --file`: Path to the JSON file containing auction items

The JSON file should contain an array of objects with the following structure:
```json
[
    {
        "title": "Item Title",
        "description": "Item Description",
        "start_price": 1000,
        "reserve_price": 1500
    },
    ...
]
```

**Example**:
```bash
python dataSeeder.py import-file -f data.json
```

### View All Items
```bash
python dataSeeder.py getAll
```

Displays all auction items stored in the MongoDB collection. Items are shown with all fields, including the MongoDB-generated _id, in the order they were added to the collection.

### Delete Items
```bash
python dataSeeder.py delete FIELD VALUE [--multi]
```

Deletes auction items from the MongoDB collection based on a field match.

**Arguments**:
* `FIELD`: The field name to match (e.g., 'title', 'description')
* `VALUE`: The value to match against the field

**Options**:
* `-m, --multi`: When True, deletes all matching documents; when False, deletes only the first match

**Examples**:
```bash
# Delete first item with matching title
python dataSeeder.py delete title "Vintage Watch"

# Delete all items with matching description
python dataSeeder.py delete description "Rare" --multi
```

## Error Handling

The tool includes comprehensive error handling:
- Validates MongoDB connection settings
- Checks for file existence during import
- Provides clear error messages for MongoDB operations
- Confirms successful operations with meaningful messages

## Security

- All MongoDB connection details are stored securely using the system keyring
- Sensitive information is never logged or saved in plain text
- Connection strings are only displayed when explicitly requested

## Exit Codes

The tool will exit with a non-zero status code if:
- MongoDB connection fails
- Required connection settings are missing
- File operations fail
- Database operations encounter errors

## Getting Help

Each command has detailed help available:

```bash
python dataSeeder.py --help           # General help
python dataSeeder.py COMMAND --help   # Command-specific help
```