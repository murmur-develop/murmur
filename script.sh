#!/bin/bash

gosu user /opt/python/bin/python3 ./run.py --voicelib_dir /opt/voicevox_core/ --runtime_dir /opt/onnxruntime/lib --host 127.0.0.1 --port 50021 &

/opt/python/bin/python3 /myapp/main.py &

wait -n

exit $?