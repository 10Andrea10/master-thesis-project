cd ./zk-rollup
./script.sh 1024-30 compile setup
./script.sh 1024-50 compile setup
cd ..
cd ./deregister
./script.sh 256 compilee setup
./script.sh 1024 compile setup
cd ..
cd ./zk-rollup/
./script.sh 2048-30 compile setup