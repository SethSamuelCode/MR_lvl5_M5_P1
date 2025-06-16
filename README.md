# MR_lvl5_M5_P1 - DataSeeder CLI Tool

A CLI tool for seeding MongoDB with auction item data. Supports adding individual items, bulk imports, and data management.

## Prerequisites

- Python 3.x
- MongoDB instance (local or remote)
- Required Python packages (install via pip):
  ```bash
  pip install -r requirements.txt
  ```

## Initial Setup

Before using the tool, you need to configure your MongoDB connection:

```bash
python dataSeeder.py setup
```

This will prompt you for:
1. MongoDB connection string
2. Collection name

Your credentials will be stored securely using the system keyring.

## Usage

```console
$ dataSeeder [OPTIONS] COMMAND [ARGS]...
```

### Options
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

## Available Commands

### Add Single Item
```console
$ dataSeeder add [OPTIONS] TITLE DESCRIPTION START_PRICE RESERVE_PRICE
```

Add a single auction item to the MongoDB collection.

**Arguments**:
* `TITLE`: [required]
* `DESCRIPTION`: [required]
* `START_PRICE`: [required]
* `RESERVE_PRICE`: [required]

### Import from File
```console
$ dataSeeder importFile [OPTIONS]
```

Bulk import auction items from the dataToInput.json file. The JSON file should contain an 'auction_items' array with objects having the following structure:
```json
{
    "title": "string",
    "description": "string",
    "start_price": "integer",
    "reserve_price": "integer"
}
```

### View All Items
```console
$ dataSeeder getAll [OPTIONS]
```

Display all auction items stored in the MongoDB collection, including their MongoDB-generated _id.

### Update Settings
```console
$ dataSeeder setup [OPTIONS]
```

**Options**:
* `--getsettings / --no-getsettings`: If True, displays current connection settings instead of setting new ones [default: no-getsettings]

### Delete Items
```console
$ dataSeeder delete [OPTIONS] FIELD VALUE
```

Delete auction items from the MongoDB collection based on a field match.

**Arguments**:
* `FIELD`: The field name to match for deletion [required]
* `VALUE`: The value to match for deletion [required]

**Options**:
* `-m, --multi`: If True, deletes all matching documents instead of just the first one

## Example Usage

1. Add a single item:
```bash
python dataSeeder.py add "Vintage Watch" "A beautiful antique timepiece" 100 150
```

2. Import multiple items from file:
```bash
python dataSeeder.py importFile
```

3. Delete an item by title:
```bash
python dataSeeder.py delete title "Vintage Watch"
```

4. Delete multiple items with the same price:
```bash
python dataSeeder.py delete start_price 100 --multi
```

## Data Format

When using the `importFile` command, your `dataToInput.json` should follow this structure:

```json
{
    "auction_items": [
        {
            "title": "Item 1",
            "description": "Description of item 1",
            "start_price": 100,
            "reserve_price": 150
        },
        {
            "title": "Item 2",
            "description": "Description of item 2",
            "start_price": 200,
            "reserve_price": 250
        }
    ]
}
```