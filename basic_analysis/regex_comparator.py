import os, re, shutil
import config


def join_directories(first_directory, second_directory, target_directory):
    if not os.path.exists(os.path.join(target_directory, 'join')):
        os.mkdir(os.path.join(target_directory, 'join'))
    new_directory = os.path.join(target_directory, 'join', first_directory.split('/')[-1] + '_' + second_directory.split('/')[-1])
    if not os.path.exists(new_directory):
        os.mkdir(new_directory)
    for item in os.listdir(first_directory) and os.listdir(second_directory):
        os.symlink(os.readlink(os.path.join(first_directory, item)), os.path.join(new_directory, item))


def file_classifier(pattern_constructor_instance, origin_directory, target_directory):
    group_result = regex_group(pattern_constructor_instance, origin_directory)
    save_directory = os.path.join(target_directory, str(pattern_constructor_instance))
    if not os.path.exists(save_directory):
        os.mkdir(save_directory)
    for name, file_list in group_result.items():
        if not os.path.exists(os.path.join(save_directory, name)):
            os.mkdir(os.path.join(save_directory, name))
        for file in file_list:
            # os.symlink(os.path.join(origin_directory, file), os.path.join(save_directory, name, file))
            shutil.copyfile(os.path.join(origin_directory, file), os.path.join(save_directory, name, file))


def regex_group(pattern_constructor_instance, directory_path):
    result_filenames = {}
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if os.path.getsize(filepath):
            results = regex_extract(pattern_constructor_instance, filepath)
            if results:
                for result in results:
                    if result in result_filenames:
                        result_filenames[result].append(filename)
                    else:
                        result_filenames[result] = [filename]
            else:
                if 'unclassified' in result_filenames:
                    result_filenames['unclassified'].append(filename)
                else:
                    result_filenames['unclassified'] = [filename]

    return result_filenames


def regex_extract(pattern_constructor_instance, file_path):
    if file_path == ".DS_Store":
        return
    white_patterns, black_patterns = pattern_constructor_instance()
    result = []
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            for white_pattern in white_patterns:
                searches = re.search(white_pattern, line)
                if searches:
                    search = searches.group(0 if not searches.lastindex else searches.lastindex)
                    is_black = False
                    for black_pattern in black_patterns:
                        if re.match(black_pattern, search):
                            is_black = True
                            break
                    if not is_black:
                        result.append(search)
    return set(result)  # distinct


class _CustomedPatternConstructor:
    def __str__(self):
        return 'Customed'

    def __call__(self):
        white_patterns = []
        black_patterns = []
        key = r'Redacted Signature'
        white_patterns.append(key)
        return white_patterns, black_patterns


# timestamp="2017-05-02T14:21:36Z" version="1.1.1"
class _STIXTimestampPatternConstructor:
    def __str__(self):
        return 'STIXTimestamp'

    def __call__(self):
        white_patterns = []
        black_patterns = []
        timestamp = r'timestamp="(\d{4}-\d{2}-\d{2}).+?" version="1.1.1"'
        white_patterns.append(timestamp)
        return white_patterns, black_patterns


class _NameCodePatternConstructor:
    def __str__(self):
        return 'NameCode'

    def __call__(self):
        white_patterns = []
        black_patterns = []
        namecode = r'NameCode="[A-Za-z]+?-[A-Za-z]+?"'
        white_patterns.append(namecode)
        return white_patterns, black_patterns


class _IndustryTypePatternConstructor:
    def __str__(self):
        return 'IndustryType'

    def __call__(self):
        white_patterns = []
        black_patterns = []
        industrytype = r'IndustryType=".*?"'
        white_patterns.append(industrytype)
        return white_patterns, black_patterns


class _IpPatternConstructor:
    def __str__(self):
        return 'IP'

    def __call__(self):
        white_patterns = []
        black_patterns = []
        ip = r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
        private_ip1 = r'^10\.'
        private_ip2 = r'^172\.(?:1[6-9]|2[0-9]|3[01])\.'
        private_ip3 = r'^192\.168\.'
        local_loop_ip = r'127\.0\.0\.1'
        white_patterns.append(ip)
        black_patterns.append(private_ip1)
        black_patterns.append(private_ip2)
        black_patterns.append(private_ip3)
        black_patterns.append(local_loop_ip)
        return white_patterns, black_patterns


if __name__ == '__main__':
    directoryPath = config.DIRECTORY_PATH
    result = regex_group(_CustomedPatternConstructor(), directoryPath)
    for key in sorted(result):
        print(key)
        for t in result[key]:
            print(t)

    # directoryPath = config.DIRECTORY_PATH
    # saveDirectoryPath = config.SAVE_DIRECTORY_PATH
    # file_classifier(_IndustryTypePatternConstructor(), directoryPath, saveDirectoryPath)

    # firstDirectory = ''
    # secondDirectory = ''
    # saveDirectoryPath = ''
    # join_directories(firstDirectory, secondDirectory, saveDirectoryPath)