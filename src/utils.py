from difflib import unified_diff
from termcolor import colored
def write_to_file(path, content, mode=None):       
    dir = os.path.dirname(path)
    
    if dir and not os.path.exists(dir):
        os.makedirs(dir)
        
        
    if mode:
        os.chmod(path, mode)
        return list(set(raw_list).difference(spec.match_files(raw_list)))
    
def diff_file(old_file, new_file):
    if old_file['path']:
        print_str = 'diff --git a/%s b/%s\n' % (old_file['path'], old_file['path'])
    else:
        print_str = 'diff --git a/%s b/%s\n' % (new_file['path'], new_file['path'])
    
    if old_file['mode'] == new_file['mode']:
        print_str += 'index %.7s..%.7s %04o\n' % (old_file['sha1'], new_file['sha1'], new_file['mode']) 
        
    elif not old_file['mode']:
        print_str += 'new file mode %04o\n' % (new_file['mode'])
        print_str += 'index %.7s..%.7s\n' % (old_file['sha1'], new_file['sha1'])
    
    elif not new_file['mode']:
        print_str += 'deleted file mode %04o\n' % (old_file['mode'])
        print_str += 'index %.7s..%.7s\n' % (old_file['sha1'], new_file['sha1'])
             
    else:
        print_str += 'old mode %04o\n' % (old_file['mode'])
        print_str += 'new mode %04o\n' % (new_file['mode'])
        print_str += 'index %.7s..%.7s\n' % (old_file['sha1'], new_file['sha1'])
       
    from_file = 'a/%s' % old_file['path'] if old_file['path'] else '/dev/null'
    to_file = 'b/%s' % new_file['path'] if new_file['path'] else '/dev/null'
    for i, line in enumerate(unified_diff(old_file['content'].splitlines(), new_file['content'].splitlines(), fromfile=from_file , tofile=to_file)):
        str = '%s\n' % line.strip('\n')
        if line.startswith('@@'):
            print_str += colored(str, 'cyan')
        elif line.startswith('+') and i >= 2:
            print_str += colored(str, 'green')
        elif line.startswith('-') and i >= 2:
            print_str += colored(str, 'red')
        else:
            print_str += str
    return print_str