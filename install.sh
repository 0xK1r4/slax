echo 'installing slax...'
sudo apt-get install python 3
pip3 install tabulate
pip3 install colorama
pip3 install psutil
echo 'creando alias...'
mv slax /usr/local/bin
echo 'creando permisos (775)'
chmod 775 /usr/local/bin/slax 
echo 'permisos agregador ..'
echo 'slax instalado ! '
echo 'para ejecutar escriba "slax"'
