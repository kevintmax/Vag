sudo apt update
sudo apt-get install -y tmux
rm -rf ~/.tmux.conf
cp ~/Vag/.tmux.conf ~/
bash ~/Vag/alias
sudo apt install virtualbox
curl -O https://releases.hashicorp.com/vagrant/2.2.9/vagrant_2.2.9_x86_64.deb
sudo apt install ./vagrant_2.2.9_x86_64.deb
