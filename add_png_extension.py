import os

directory = 'img-downloads'

for filename in os.listdir(directory):
    old_file = os.path.join(directory, filename)

    if os.path.isfile(old_file):
        if not filename.lower().endswith('.png'):
            new_filename = filename + '.png'
            new_file = os.path.join(directory, new_filename)

            os.rename(old_file, new_file)
            print(f'Renamed: {old_file} to {new_file}')