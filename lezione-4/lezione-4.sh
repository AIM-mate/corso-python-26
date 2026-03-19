# Questa e' una lista dei comandi che segue quanto riportato nelle slides.
# Non va inteso come vero script (molti comandi sono ridondanti)
# ma solo come lista dei comandi per riprodurre l'output visto a lezione

rm -rf workdir
mkdir workdir
cd workdir

mkdir pyaim
cd pyaim

cat <<EOF > aimmodule.py
def hello_world():
    print("Hello World!")
EOF

cat <<EOF > main.py
import aimmodule
if __name__ == "__main__":
    a = 1
    print("dir():", dir())
    print("dir(aimmodule):", dir(aimmodule))
    print("type(aimmodule):", type(aimmodule))
    aimmodule.hello_world()
EOF

python main.py

mkdir subaimpkg
touch subaimpkg/__init__.py

cat <<EOF > subaimpkg/subaimmodule.py
def hello_world():
    print("Hello World from Sub AIM Module!")
EOF


python -c "import sys; print('sys.path:', sys.path)"
echo "PYTHONPATH=$PYTHONPATH"
export PYTHONPATH=/tmp
echo "PYTHONPATH=$PYTHONPATH"
python -c "import sys; print('sys.path:', sys.path)"


cat <<EOF > main.py
import subaimpkg
print('dir(subaimpkg):', dir(subaimpkg))
print('subaimpkg.__path__:', subaimpkg.__path__)
import subaimpkg.subaimmodule
subaimpkg.subaimmodule.hello_world()
EOF

python main.py

ls -lah $(python3 -m site --user-site)

echo $PWD
ls

rm main.py
touch __init__.py

cd ..
mkdir src
mv pyaim src
mkdir pyaim
mv src pyaim

cd pyaim
touch README.md

cat <<EOF > pyproject.toml
[build-system]
# These are the tools needed to actually turn your code into a package.
requires = ["setuptools", "wheel"] 
# This tells pip which 'engine' to use to run the build.
build_backend = "setuptools.build_meta"
[project]
# The name of your package (how it will appear on PyPI).
name = "pyaim" 
# Use Semantic Versioning (Major.Minor.Patch).
version = "3.1.4" 
# A short tagline for your project.
description = "A small project that does big things."
# Who to blame (or thank) for the code.
authors = [{name = "Your Name", email = "you@example.com"}]
# The minimum Python version required to run your code.
requires-python = ">=3.8"
# External libraries your code depends on, with version requirement.
dependencies = ["pandas"]
[project.optional-dependencies]
# Extra packages installed via pip install ".[dev]"
dev = ["pytest", "black"]
EOF

pip install -e .

cd ..
cat <<EOF > main.py
import pyaim
import pyaim.aimmodule
if __name__ == "__main__":
    print(dir(pyaim))
    pyaim.aimmodule.hello_world()
EOF
python main.py


cd pyaim/src/pyaim
cat <<EOF > __init__.py
from importlib.metadata import version
__version__ = version(__name__)
from pyaim.subaimpkg.subaimmodule import hello_world as hello_world_v2
EOF

# no need of reinstall !
cd ../../..
cat <<EOF > main.py
import pyaim
if __name__ == "__main__":
    print("VERSION:", pyaim.__version__)
    pyaim.hello_world_v2()
EOF
python main.py


cat <<EOF > pyaim/src/pyaim/aimmodule.py
def my_sum(a, b):
    return a + b
EOF

mkdir pyaim/tests
cat <<EOF > pyaim/tests/test_core.py
from pyaim.aimmodule import my_sum
def test_somma():
    assert my_sum(1, 1) == 2
EOF

cd pyaim
python -m pytest