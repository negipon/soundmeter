# SoundMeter
## on Raspberry pi

Raspbian 2018-3-13

### 参考
https://github.com/shichao-an/soundmeter


### USBサウンドカードの優先度を上げる

```
sudo apt-get update
sudo apt-get upgrade
```

#### soundmeter
```
sudo apt-get install portaudio19-dev python-dev alsa-utils -y
```

```
sudo reboot
```

### python package install
```
pip install soundmeter --allow-all-external --allow-unverified pyaudio
```

```
git clone https://github.com/shichao-an/soundmeter.git
```

```
cd soundmeter/
```

### git install
```
sudo python setup.py install
```

```
sudo apt-get install ffmpeg
```
### gain
```
alsamixer
```

```
$ python3 soundmeter.py
```