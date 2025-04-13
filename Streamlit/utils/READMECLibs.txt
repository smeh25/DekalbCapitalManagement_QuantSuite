To build the libraries, run:

pip  install .

----------------------------------------

To rebuild after changes:

pip uninstall correlation -y

rm -rf build/ dist/ *.egg-info

... Add each library as it is built

pip install .


------------------------------------