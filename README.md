### Configuration File Format

#### 1. actions (Main Block)

##### 1.1 replace_string – String Replacement

- **Description**: Replaces a specified strings with anothers.
- **Fields**:
  - `target`: Path to the file or “spec” (indicates the spec file). Glob patterns are supported.
  - `find`: String to search for (supports multi-lines).
  - `replace`: String to replace with (supports multi-lines).
  - `count`: Number of replacements (default is -1, which replaces all occurrences).

**Example**:
```yaml
  - replace_string:
    - target: "*.conf"
      find: "RHEL"
      replace: "AlmaLinux"
      count: 1
    - target: "spec"
      find: |
            %if 0%{?rhel}
            RHEL
      replace: |
            %if 0%{?almalinux}
            AlmaLinux
```

##### 1.2 delete_line – Line Deletion

- **Description**: Deletes specified lines.
- **Fields**:
  - `target`: Path to the file or “spec”. Does not support glob patterns.
  - `lines`:  List of lines to delete (supports multi-lines).

**Example**:
```yaml
  - delete_line:
    - target: "README.md"
      lines:
        - "line1"
        - |
            hello world
            additional line
```

##### 1.3 modify_release – Release Number Modification

- **Description**: Adds a suffix to the release number.
- **Fields**:
  - `suffix`: Suffix to append to the release number.
  - `enabled`: Enables or disables the modification (default is true).

**Example**:
```yaml
  - modify_release:
    - suffix: ".mycustom.1"
      enabled: true
```

##### 1.4 changelog_entry – Adding Changelog Entries

- **Description**: Adds entries to the changelog.
- **Fields**:
  - `name`: Author’s name.
  - `email`: Author’s email.
  - `line`: Lines to add to the changelog (also used as commit messages).

**Example**:
```yaml
  - changelog_entry:
    - name: "eabdullin"
      email: "eabdullin@almalinux.org"
      line:
        - "Updated branding to AlmaLinux"
        - "Fixed a typo in the README"
```

##### 1.5 add_files – Adding Files

- **Description**: Adds source files or patches.
- **Fields**:
  - `type`: File type (patch or source).
  - `name`: File name. Should be placed in the `files` directory of the autopatch namespace repository.
  - `number`: Patch/file number or “Latest” (default is “Latest”).

**Example**:
```yaml
  - add_files:
    - type: "patch"
      name: "my_patch.patch"
      number: "Latest"
    - type: "source"
      name: "additional_source.tar.gz"
      number: 1000
```

##### 1.6 delete_files – Deleting Files

- **Description**: Deletes files from the repository.
- **Fields**:
  - `file_name`: File name to delete.

**Example**:
```yaml
    - delete_files:
      - file_name: "file1.txt"
      - file_name: "file2"
```

##### 1.7. run_custom_scripts - Running Custom Scripts

- **Description**: Executes user-defined scripts to prepare the package before performing other actions (e.g., creating symbolic links).
- **Fields**: 
  - `script`: script name. Should be placed in the `scripts` directory of autopatch namespace repository
  - `cwd`: "rpms" or "autopatch" ('rpms' by default).

**Example**:
```yaml
- run_script:
    - script: "custom_script.sh"
      cwd: "rpms"

```
