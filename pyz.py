import os
import sys
import shutil
import compileall
import zipfile

def paths(source):
    temp = source + ".temp"
    dest = dest = source + ".pyz"
    return (source, temp, dest) if os.path.exists(source) else (None, None, None)

def move_cache(source, dest):
    for from_dir, dirs, files in os.walk(source):
        if from_dir.endswith("__pycache__"):
            to_dir = from_dir.replace(source, dest).replace("__pycache__", "")

            if not os.path.exists(to_dir):
                os.mkdir(to_dir)
            
            for file_name in files:
                shutil.move(os.path.join(from_dir, file_name), to_dir)
                os.rename(os.path.join(to_dir, file_name), os.path.join(to_dir, file_name.split(".")[0]+".pyc"))

            os.rmdir(from_dir)

def zip_cache(source, dest):
    target_zip = zipfile.ZipFile(dest, "w")

    for from_dir, dirs, files in os.walk(source):
        for file_name in files:
            to_dir = from_dir.replace(source, "")

            target_zip.write(os.path.join(from_dir, file_name), os.path.join(to_dir, file_name))

    target_zip.close()

if __name__ == "__main__":

    origin = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    source, temp, dest = paths(origin)

    if source == None:
        print("Source path doesn't exist: " + origin)
        exit()

    print("Start from source: " + source)

    if not os.path.exists(temp): 
        os.mkdir(temp) # Make temp directory

    compileall.compile_dir(source)
    move_cache(source, temp)
    zip_cache(temp, dest)

    shutil.rmtree(temp) # Remove temp directory

    print("Done: " + dest)