#!/bin/bash

handler() {
    kill ${child_pid1}
    kill ${child_pid2}
    wait ${child_pid1}
    wait ${child_pid2}
}

trap handler SIGTERM

gosu user /opt/python/bin/python3 ./run.py --voicelib_dir /opt/voicevox_core/ --runtime_dir /opt/onnxruntime/lib --host 0.0.0.0 &
child_pid1=$!

/opt/python/bin/python3 /myapp/main.py &
child_pid2=$!

wait ${child_pid1}
wait ${child_pid2}
