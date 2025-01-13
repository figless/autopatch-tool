import os
import re
from enum import Enum
from tempfile import NamedTemporaryFile
from pathlib import Path

from tools.logger import logger
from tools.tools import run_command

rpmspec_definition = {
    "__python3": "/usr/bin/python3",
    "ldconfig_scriptlets(n:)": "%{nil}",
}

class PatchDirectiveType(Enum):
    CLASSIC = 0
    UPPER_P_W_SPACE = 1
    KERNEL = 2
    GRUB2 = 3
    AUTOSETUP = 4
    UPPER_P_N_SPACE = 5

class DirectiveType(Enum):
    PATCH = "Patch"
    SOURCE = "Source"

class RPMSpecFileParsingError(Exception):
    """Raised when there is an error parsing RPM spec file"""

def is_spec_comment(line: str) -> bool:
    return line.startswith("#")

def is_changelog(line: str) -> bool:
    return "%changelog" == line.strip('\n \t')

def is_release(line: str) -> bool:
    return line.startswith("Release:")

def spec_contains_autochangelog(spec_info: list[str]) -> bool:
    return "%autochangelog" in spec_info

def spec_contains_autosetup(spec_info: list[str]) -> bool:
    for line in spec_info:
        if "%autosetup" in line:
            return True
    return False


def prepare_spec_file_data_with_rpmspec(spec_info: list[str], spec_file_path) -> list[str]:
    """
    Read a spec file with updated release attribute using rpmspec utility.
    Parameters
    ----------
    spec_info : list of str
        all changelog_info of spec-file.
    Returns
    -------
    list of str
    """
    try:
        repo_path = Path(spec_file_path)
        source_path = repo_path.parent
        if repo_path.parent.name == "SPECS":
            source_path = repo_path.parent.parent / "SOURCES"

        definitions = ["--define", f"_sourcedir {source_path}"]

        for key, value in rpmspec_definition.items():
            definitions.extend(["--define", f"{key} {value}"])

        with NamedTemporaryFile("w", delete=False) as tmp_file:
            tmp_file.write("\n".join(spec_info))
            tmp_file.flush()
            tmp_file_path = tmp_file.name
        result = run_command(["rpmspec", "--parse", tmp_file_path, *definitions])
        os.remove(tmp_file_path)
        
        return list(map(lambda s: f"{s}\n", result.stdout.splitlines()))

    except Exception as err:
        raise RPMSpecFileParsingError("Failed to parse spec data with rpmspec") from err

def get_version_information(spec_info: list[str]) -> tuple[str, ...]:
    """
    Gets epoch, version and release (last in the file).
    Parameters
    ----------
    spec_info : list of str
        all changelog_info of spec-file.
    Returns
    -------
    tuple of str
        EVR of package.
    """
    try:
        epoch, version, release = None, None, None
        for i, line in enumerate(spec_info):
            if epoch is None and line.startswith("Epoch:"):
                epoch = line.rstrip().split()[-1]
            if version is None and line.startswith("Version:"):
                version = line.rstrip().split()[-1]
            if release is None and line.startswith("Release:"):
                release = spec_info[i].rstrip().split()[-1]
        if release:
            release = _analyze_string(release, spec_info)
        if version:
            version = _analyze_string(version, spec_info)
        return epoch, version, release
    except Exception as err:
        raise RPMSpecFileParsingError("Failed to parse epoch/version/release") from err


def _analyze_string(s: str, spec_info: list[str]) -> str:
    """
    Parses variable (ignores %{?.*}, recursively finds value of %{.*}).
    Parameters
    ----------
    s : str
        value of variable from spec-file.
    spec_info : list of str
        all changelog_info of spec-file.
    Returns
    -------
    str
        real value of variable (without other variables).
    """
    i = 0
    answer = ""
    while i < len(s):
        if s[i] == "%":
            i += 2
            variable = ""
            if s[i] == "?":
                counter = 1
                while counter != 0:
                    if s[i] == "{":
                        counter += 1
                    if s[i] == "}":
                        counter -= 1
                    i += 1
            else:
                while s[i] != "}":
                    variable += s[i]
                    i += 1
            if variable:
                answer += _get_value_from_variable(variable, spec_info)
                i += 1
        else:
            answer += s[i]
            i += 1
    return answer


def _get_value_from_variable(variable: str, spec_info: list[str]) -> str:
    """
    Gets real value of variable.
    Parameters
    ----------
    variable : str
        value of variable from spec-file.
    spec_info : list of str
        all changelog_info of spec-file.
    Returns
    -------
    str
        real value of variable (without other variables).
    """
    for line in spec_info:
        if variable in line and (line.startswith("%define") or line.startswith("%global")):
            if "shortcommit" in line:
                continue
            # check full name alignment
            if line.split()[1] != variable:
                continue
            # recursion
            value = _analyze_string(line.split()[-1], spec_info)
            return value
    raise Exception(f"Variable {variable} is used but not defined in specfile")


def find_last_directive(spec_info: list[str], directive_type: DirectiveType):
    last_directive_number = None
    last_directive_index = None  # To track the last directive regardless of block
    directives_without_numbers = False

    in_conditional = False
    last_endif_index = None

    for i, line in enumerate(spec_info):
        # Track conditional blocks
        if re.match(r"^%endif\b", line):
            in_conditional = True
            last_endif_index = i - 1
        elif re.match(r"^%if*", line) and in_conditional:
            in_conditional = False
        
        # Track the last directive
        if (result := re.match(rf"{directive_type.value}([0-9]*):", line)):
            if not in_conditional:
                last_directive_index = i
            if result.group(1):
                last_directive_number = int(result.group(1))
            else:
                # Directive is used in unnumbered way
                last_directive_number = 0
                directives_without_numbers = True
            break

    # Adjust the position to be after the last %endif if needed
    if last_directive_index is None and last_endif_index is not None:
        last_directive_index = last_endif_index

    if last_directive_number is None:
        if directive_type == DirectiveType.PATCH:
            logger.warning(f"No {directive_type} directives found in spec file, creating a new block")
            return find_last_directive(spec_info, DirectiveType.SOURCE)
        else:
            raise RPMSpecFileParsingError(f"No {directive_type} directives found in spec file")
        
    return (last_directive_number, last_directive_index, directives_without_numbers)

def find_almalinux_block(spec_info: list[str], directive_type: str):
    for i, line in enumerate(spec_info):
        if re.match(rf"^# AlmaLinux {directive_type}*$", line, re.IGNORECASE):
            return True
    return False

def get_patch_directive_type(line: str) -> PatchDirectiveType:
    if re.match(r"^%patch[0-9]{1,5}", line):
        return PatchDirectiveType.CLASSIC
    if re.match(r"^%patch\s+-P\s+[0-9]{1,5}", line):
        return PatchDirectiveType.UPPER_P_W_SPACE
    if re.match(r"^%patch\s+-P[0-9]{1,5}", line):
        return PatchDirectiveType.UPPER_P_N_SPACE
    return None

def generate_patch_apply_line(patch_number: str, patch_stem: str, patch_directive_type: PatchDirectiveType) -> str:
    if patch_directive_type == PatchDirectiveType.CLASSIC:
        return f"""%patch{patch_number} -p1 -b .{patch_stem}"""
    elif patch_directive_type == PatchDirectiveType.UPPER_P_W_SPACE:
        return f"""%patch -P {patch_number} -p1 -b .{patch_stem}"""
    elif patch_directive_type == PatchDirectiveType.UPPER_P_N_SPACE:
        return f"""%patch -P{patch_number} -p1 -b .{patch_stem}"""
    else:
        raise RPMSpecFileParsingError("Unknown patch directive type")

def define_type_patch_directive_type(spec_info: list[str], package_name: str,) -> PatchDirectiveType:
    if package_name == 'kernel':
        return PatchDirectiveType.KERNEL
    if package_name == 'grub2':
        return PatchDirectiveType.GRUB2 
    if spec_contains_autosetup(spec_info):
        return PatchDirectiveType.AUTOSETUP
    for line in spec_info:
        directive_type = get_patch_directive_type(line)
        if directive_type is not None:
            return directive_type
    return None


def find_index_to_insert(spec_info: list[str]) -> int:
    in_conditional = False
    conditional_start_index = None
    last_patch_apply_index = None
    for i, line in enumerate(spec_info):
        # Track if we're in a conditional block (remember we're going backwards)
        # Track only if we haven't found the last patch yet
        if last_patch_apply_index is None and re.match(r"^%endif\b", line):
            in_conditional = True
            conditional_start_index = i
        elif re.match(r"^%if*", line) and in_conditional:
            # We've reached the start of conditional block
            in_conditional = False
            if last_patch_apply_index is None:
                # If we haven't found a patch yet, this conditional block isn't relevant
                conditional_start_index = None
        # Track the last %patch directive regardless of block
        patch_directive = get_patch_directive_type(line)
        if (
            last_patch_apply_index is None and
            patch_directive is not None
        ):
            last_patch_apply_index = i
    insert_index = conditional_start_index if conditional_start_index is not None else last_patch_apply_index

    return insert_index

def find_setup_line(spec_info: list[str]) -> int:
    for i, line in enumerate(spec_info):
        if re.match(r"^%setup\b", line):
            return i
    return None


def apply_patch(
        spec_info: list[str],
        patch_name: str,
        directive_type:DirectiveType,
        package_name: str,
        patch_number: int = -1
    ) -> None:
    """
    Append changelog_info to project's specfile which apply certain patch.
    Patches are added after the last patch in the "AlmaLinux patches" block.
    If no such block exists, it will be created after the last patch directive.
    """
    spec_info.reverse()
    last_patch_number, last_patch_index, patches_without_numbers = find_last_directive(spec_info, directive_type)

    if not find_almalinux_block(spec_info, directive_type.value):
        spec_info.insert(last_patch_index, f"\n# AlmaLinux {directive_type.value}")
    # Insert new patch after the last patch
    if patches_without_numbers:
        new_patch_number = ""
    else:
        new_patch_number = str(last_patch_number + 1)
        if patch_number != -1:
            new_patch_number = str(patch_number)
    spec_info.insert(last_patch_index, f"{directive_type.value}{new_patch_number}: {patch_name}")

    patch_directive_type = define_type_patch_directive_type(spec_info, package_name)
    
    # Doesn't need to apply patch directive for autosetup package and for grub2 package
    if directive_type == DirectiveType.PATCH and patch_directive_type != PatchDirectiveType.GRUB2:
        almalinux_block_exists = False
        insert_index = find_index_to_insert(spec_info)
        logger.debug(f"Patch directive type: {patch_directive_type} and insert index: {insert_index}")

        if insert_index is not None:
            if patch_directive_type != PatchDirectiveType.AUTOSETUP and patch_directive_type != PatchDirectiveType.GRUB2:
                for i, line in enumerate(spec_info):
                    if re.match(rf"^# Applying AlmaLinux {directive_type.value}*$", line, re.IGNORECASE):
                        almalinux_block_exists = True
                if not almalinux_block_exists:
                    spec_info.insert(insert_index, f"\n# Applying AlmaLinux {directive_type.value}")

                spec_info.insert(
                    insert_index,
                    generate_patch_apply_line(
                        new_patch_number,
                        ''.join(patch_name.split('.')[:-1]),
                        patch_directive_type
                    )
                )
        else:
            if patch_directive_type != PatchDirectiveType.AUTOSETUP:
                insert_index = find_setup_line(spec_info)
                logger.debug(f"Insert index: {insert_index}")
                if insert_index is not None:
                    patch_directive_type = PatchDirectiveType.UPPER_P_W_SPACE
                    spec_info.insert(
                        insert_index, 
                        generate_patch_apply_line(
                                new_patch_number,
                                ''.join(patch_name.split('.')[:-1]),
                                patch_directive_type
                            )
                        )
                else:
                    raise RPMSpecFileParsingError("Failed to find a place to insert patch directive")
            else:
                logger.info("Skipping applying patch directive for autosetup package")

        if patch_directive_type is None:
            raise RPMSpecFileParsingError("Unknown patch directive type")
    spec_info.reverse()
