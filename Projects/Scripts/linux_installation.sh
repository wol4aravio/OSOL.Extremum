#!/bin/bash

# Installing Anaconda Python
mkdir Downloads
wget https://repo.anaconda.com/archive/Anaconda3-5.1.0-Linux-x86_64.sh -O ./Downloads/anaconda.sh # yes to all except of MS tools
chmod +x ./Downloads/anaconda.sh
./Downloads/anaconda.sh
rm ./Downloads/anaconda.sh
source ~/.bashrc
python --version

# Downloading sources
sudo apt-get install unzip
wget https://github.com/wol4aravio/OSOL.Extremum/archive/master.zip -O ~/OSOL.Extremum.zip
unzip ~/OSOL.Extremum.zip
rm ~/OSOL.Extremum.zip
mv OSOL.Extremum-master/ OSOL.Extremum

# Installing PyTools
cd OSOL.Extremum/PyTools/
python OSOL_Extremum/setup.py install
cd ~

# Installing dotnet
wget -q packages-microsoft-prod.deb https://packages.microsoft.com/config/ubuntu/16.04/packages-microsoft-prod.deb -O ./Downloads/microsoft.deb
sudo dpkg -i ./Downloads/microsoft.deb
rm ./Downloads/microsoft.deb
sudo apt-get install apt-transport-https
sudo apt-get update
sudo apt-get install dotnet-sdk-2.1.200
dotnet --version

# Installing java + sbt
sudo apt-get install openjdk-8-jdk
java -version

wget https://piccolo.link/sbt-1.1.2.zip -O ./Downloads/sbt.zip
unzip ./Downloads/sbt.zip
rm ./Downloads/sbt.zip
mv sbt/ /usr/bin/sbt
echo $"export PATH=\"/usr/bin/sbt/bin:\$PATH\"" >> ~/.bashrc
source ~/.bashrc
sbt --version

# Building Runner Apps
cd OSOL.Extremum/Apps/DotNet/Runner/
dotnet publish -c Release -o runner
mv runner ~/DotNetRunner
cd ~

cd OSOL.Extremum/Apps/JVM/Runner/
sbt clean && sbt assembly
mkdir ~/JVM_Runner
mv target/scala-2.12/OSOL.Extremum.Apps.JVM.Runner.jar ~/JVM_Runner/OSOL.Extremum.Apps.JVM.Runner.jar
cd ~
