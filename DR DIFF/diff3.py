
old_path = 'PROD.txt'
new_path = 'DR.txt'

old_lines = file(old_path).read().split('\n')
new_lines = file(new_path).read().split('\n')

old_lines_set = set(old_lines)
new_lines_set = set (new_lines)

old_added = old_lines_set - new_lines_set
old_removed = new_lines_set - old_lines_set

for line in old_lines:
        if line in old_added:
                print '-', line.strip()
        elif line in old_removed:
                print '+', line.strip()

for line in new_lines:
        if line in old_added:
                print '-', line.strip()
        elif line in old_removed:
                print '+', line.strip()
