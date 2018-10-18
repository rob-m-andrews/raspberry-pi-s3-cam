# Raspberry Pi Camera Amazon S3 Uploader

## Requirements
- Raspberry Pi + Camera + Network Adapter

## Initial Setup
- Ensure Raspberry Pi Camera has been enabled:
  - Running `sudo raspi-config` will get you into the settings to enable

- Install the `python3-picamera` library:
  ```
  sudo apt-get update
  sudo apt-get install python3-picamera
  ```

- Install pip3:
  ```
  sudo apt-get install python3-pip
  ```

- Install `tinys3` library: `pip3 install tinys3`
- Install `pyyaml` library: `pip3 install pyyaml`
- Update `config.yml` and provide S3 credentials as well as specify a bucket name

## Running 
`python3 s3cam.py`
